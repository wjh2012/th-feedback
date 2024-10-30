from fastapi import FastAPI, File, UploadFile, Form, Request
from pathlib import Path
from datetime import datetime

app = FastAPI()

BASE_DIRECTORY = Path("./uploads")  # 기본 저장 경로

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
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    client_ip = request.client.host  # 클라이언트 IP 주소 가져오기

    # 이미지와 텍스트 파일 이름에 시간과 IP 주소를 접두사로 추가
    image_filename = f"{current_time}_{client_ip}_{file.filename}"
    text_filename = f"{current_time}_{client_ip}_uploaded_text.txt"

    # 이미지 파일 저장 경로 설정
    image_path = save_directory / image_filename
    with image_path.open("wb") as buffer:
        buffer.write(await file.read())

    # 텍스트 파일 저장 경로 설정
    text_path = save_directory / text_filename
    with text_path.open("w") as text_file:
        text_file.write(data)

    return {"message": "File and text saved successfully"}
