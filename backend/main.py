import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core_logic import process_document, query_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str
    collection_name: str


@app.get("/")
def read_root():
    return {"message": "Parsec AI API is running"}


@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        collection_name = process_document(file_path)

        return {"message": "File processed successfully", "collection_name": collection_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/query/")
async def handle_query(request: QueryRequest):
    try:
        answer = query_document(request.question, request.collection_name)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
