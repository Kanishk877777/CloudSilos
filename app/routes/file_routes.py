from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import File as FileModel
from app.utils import generate_file_hash
from app.gcs_service import upload_to_gcs, download_from_gcs

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_data = await file.read()

    file_hash = generate_file_hash(file_data)

    existing_file = db.query(FileModel).filter(
        FileModel.file_hash == file_hash
    ).first()

    if existing_file:
        return {
            "message": "Duplicate file detected",
            "existing_file": existing_file.filename
        }

    gcs_path = upload_to_gcs(file.filename, file_data)

    new_file = FileModel(
        filename=file.filename,
        file_hash=file_hash,
        gcs_path=gcs_path,
        size=len(file_data),
        owner_id=1
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "message": "File uploaded successfully",
        "file_hash": file_hash
    }


@router.get("/files")
def list_files(db: Session = Depends(get_db)):

    files = db.query(FileModel).all()

    return files


@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):

    file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    data = download_from_gcs(file.gcs_path)

    return {
        "filename": file.filename,
        "size": len(data)
    }
