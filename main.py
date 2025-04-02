import os
import requests
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # ファイルを一時的にRender上で保存
    file_content = await file.read()
    with open(f"temp_{file.filename}", "wb") as f:
        f.write(file_content)

    # 自宅PCにファイルを転送（自宅PCのFastAPIに送る）
    response = requests.post("http://192.168.0.132:8000/save/", files={"file": open(f"temp_{file.filename}", "rb")})
    
    if response.status_code == 200:
        return {"message": "File uploaded and saved successfully."}
    else:
        return {"error": "Failed to upload file to local server"}
