import uuid
from fastapi import APIRouter, File, UploadFile
from app.services.file_storage import save_uploaded_image

router = APIRouter(prefix="/upload", tags=["uploads"])


@router.post("/bytes")
async def upload_bytes(file: bytes = File(...)) -> dict:
    return {
        "filename": str(uuid.uuid4().hex),
        "size_bytes": len(file),
    }


@router.post("/file")
async def upload_file(file: UploadFile = File(...)) -> dict:
    # print(file)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }


@router.post("/save")
async def save_file(file: UploadFile = File(...)) -> dict:
    saved = save_uploaded_image(file)
    return {
        "filename": saved.get("filename"),
        "content_type": saved.get("content_type"),
        "url": saved.get("url"),
    }
