from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uuid
from bot.processor import process_excel

app = FastAPI()

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"temp/{file_id}.xlsx"
    output_path = f"temp/{file_id}_out.xlsx"
    json_path = f"temp/{file_id}.json"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    process_excel(input_path, output_path, json_path)

    return {
        "excel_url": f"/download/{file_id}_out.xlsx",
        "json_url": f"/download/{file_id}.json"
    }

@app.get("/download/{filename}")
async def download_file(filename: str):
    path = f"temp/{filename}"
    return FileResponse(path, filename=filename)