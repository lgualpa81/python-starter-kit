import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status
from app.core.constants import MEDIA_DIR

ALLOWED_MIMETYPES = ["image/jpeg", "image/png"]
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "3"))
CHUNKS = 1024 * 1024


def ensure_media_dir():
    os.makedirs(MEDIA_DIR, exist_ok=True)


def save_uploaded_image(file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}"
        )
    ensure_media_dir()
    ext = file.filename.rsplit(".", maxsplit=1)[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(MEDIA_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, length=CHUNKS)
    size = os.path.getsize(file_path)
    if size > MAX_MB * CHUNKS:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"File too large ({size} MB)"
        )
    return {
        "filename": filename,
        "content_type": file.content_type,
        "url": f"/media/{filename}",
        "size": size,
    }
