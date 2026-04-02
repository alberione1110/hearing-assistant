from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings


class FileStoreService:
    def __init__(self) -> None:
        self.base_dir = Path(settings.upload_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, upload_file: UploadFile) -> str:
        suffix = Path(upload_file.filename).suffix if upload_file.filename else ".wav"
        file_path = self.base_dir / f"{uuid4().hex}{suffix}"

        content = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return str(file_path)

    def delete_file(self, file_path: str) -> None:
        path = Path(file_path)
        if path.exists():
            path.unlink()