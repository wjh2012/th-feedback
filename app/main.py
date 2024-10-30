import math

import msgspec
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from pathlib import Path
from datetime import datetime

app = FastAPI()

BASE_DIRECTORY = Path("./uploads")  # 기본 저장 경로

# 데이터 구조 정의
class RectangleData(msgspec.Struct):
    Type: str
    Rectangles: list[list[float]]
    Points: list[list[tuple[float, float]]]

class ParsedData(msgspec.Struct):
    before: list[RectangleData]
    after: list[RectangleData]

# msgspec JSON 디코더 인스턴스 생성
decoder = msgspec.json.Decoder(ParsedData)

@app.post("/upload/")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    data: str = Form(...)
):
    # 현재 날짜를 기준으로 디렉토리 생성
    current_date = datetime.now().strftime("%Y%m%d")
    save_directory = BASE_DIRECTORY / current_date
    save_directory.mkdir(parents=True, exist_ok=True)  # 디렉토리가 없으면 생성

    # 현재 시간을 밀리초 단위로 포맷팅하여 접두사로 추가
    current_time = datetime.now().strftime("%Y%m%d%H%M%S_%f")[:-2]

    # data 필드를 JSON으로 파싱
    try:
        parsed_data = decoder.decode(data)
    except msgspec.DecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {e}")


    if not parsed_data.before:
        if parsed_data.after:
            detect_type = "test"
        else:
            detect_type = "FN"
    else:
        if len(parsed_data.before) > len(parsed_data.after):
            detect_type = "FP"
        elif len(parsed_data.before) < len(parsed_data.after):
            detect_type = "FN"
        else:
            detect_type = "FIX"

    # 이미지와 텍스트 파일 이름에 시간과 IP 주소를 접두사로 추가
    image_filename = f"{current_time}_{Path(file.filename).stem}_{detect_type}{Path(file.filename).suffix}"
    json_filename = f"{current_time}_{Path(file.filename).stem}_{detect_type}.json"

    # 이미지 파일 저장 경로 설정
    image_path = save_directory / image_filename
    with image_path.open("wb") as buffer:
        buffer.write(await file.read())

    # 파싱된 데이터를 JSON 파일로 저장
    json_path = save_directory / json_filename
    with json_path.open("w") as json_file:
        json_file.write(msgspec.json.encode(parsed_data).decode())

    return {"message": "File and JSON data saved successfully"}
