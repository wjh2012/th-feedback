from fastapi import FastAPI, File, UploadFile, Form
from pathlib import Path
from datetime import datetime

app = FastAPI()

# 파일을 저장할 디렉토리 경로
SAVE_DIRECTORY = Path("./uploads")
SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)  # 디렉토리가 없으면 생성


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), data: str = Form(...)
):
    # 현재 시간을 접두사로 추가
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"{current_time}_{file.filename}"
    text_filename = f"{current_time}_uploaded_text.txt"

    # 이미지 파일 저장 경로 설정
    image_path = SAVE_DIRECTORY / image_filename
    with image_path.open("wb") as buffer:
        buffer.write(await file.read())

    # 텍스트 파일 저장 경로 설정
    text_path = SAVE_DIRECTORY / text_filename
    with text_path.open("w") as text_file:
        text_file.write(data)

    return {"message": "File and text saved successfully"}
