import os
from pathlib import Path

import aiofiles
from fastapi import UploadFile


def safe_preview(text: str, limit: int = 240) -> str:
    return text[:limit].replace("\n", " ").strip()


async def save_upload(upload: UploadFile, upload_dir: str) -> tuple[str, str, str]:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(upload_dir, upload.filename)

    content = await upload.read()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    decoded = content.decode("utf-8", errors="ignore")
    return upload.filename, file_path, decoded
