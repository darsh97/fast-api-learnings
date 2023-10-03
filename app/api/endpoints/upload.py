import json
import os.path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from uuid import uuid4
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as
from app.schema.schema import MetadataModel, UploadResponse
from mimetypes import MimeTypes
from typing import Dict
import dbm

router = APIRouter()

FILE_STORAGE_PATH: str = "files"
REPOSITORY_METADATA_FILE: str = "repository"


################ HELPERS ################

def get_dict_from_json(json_file: str):
    with open(json_file, "r") as _json_file:
        json_content = json.load(_json_file)
        return json_content


def get_json_from_dict(dict_content: Dict):
    return json.dumps(dict_content)


def create_file_name(req_id: str, file_name: str):
    return f"{req_id}_{file_name}.pdf"


# notes:
# fastapi cant accept Pydantic Classes directly from a multipart form data along with UploadFile, use `str`, then later on apply `pydantic` validation on it
# UploadFile is async, use await on reading the UploadFile object, make writing sync

@router.post("/upload/", response_model=dict)
async def upload_file(pdf_file: UploadFile = File(...), metadata: str = Form(...)):
    try:
        unique_req_id: str = str(uuid4())
        metadata: MetadataModel = MetadataModel.model_validate_json(metadata)

        # push the file to local temp storage
        local_file_path: str = os.path.join(FILE_STORAGE_PATH, f"{unique_req_id}_{pdf_file.filename}")
        print(local_file_path)

        with open(local_file_path, "wb") as _pdf_file:
            received_pdf_content = await pdf_file.read()
            _pdf_file.write(received_pdf_content)

        # Push to s3 instead of database
        with dbm.open(REPOSITORY_METADATA_FILE, "c") as db:
            print(f"Pushing {unique_req_id} to {str(db)}")
            db[unique_req_id] = metadata.model_dump_json()

        response_content = {
            "request_id": unique_req_id,
            "file_name": pdf_file.filename,
            "file_type": pdf_file.content_type
        }

        return JSONResponse(content=response_content, status_code=201)

    except Exception as e:
        print(e.with_traceback())
        return HTTPException(status_code=500, detail="Internal Server Error")
