from fastapi import UploadFile, Request
from pathlib import Path
from .paths import ARTIFACTS_DIR
import shutil
import os
import json


def find_first_in(dir: Path, filename: str) -> Path | None: # TODO rewrite so that it aceopts a list of filenames and tries in order until first match is found
    for thumb_path in dir.rglob(filename):
        return thumb_path

def upload_files(dest: str, files: list[UploadFile]):
    for file in files:
        file_path = os.path.join(dest, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            print(f"Added: {file.filename}")


def get_url_for(path: Path, request: Request):
    return request.url_for("artifacts", path=str(path.relative_to(ARTIFACTS_DIR)))


def read_metadata(artifact_path: Path):
    metadata_path = artifact_path / "metadata.json"
    try:
        return json.loads(metadata_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def read_images(artifact_path: Path, request: Request):
    try:
        return [str(get_url_for(img_path, request)) for img_path in (artifact_path / "images").iterdir() if img_path.is_file()]
    except FileNotFoundError:
        return []


def read_RTIs(artifact_path: Path, request: Request):
    RTIs_path = artifact_path / "RTIs"

    RTIs = []

    try:
        sorted_entries = sorted(
            RTIs_path.iterdir(),
            key=lambda p: p.stat().st_ctime,  # Sort by creation time
            reverse=True
        )
    except FileNotFoundError:
        return RTIs

    for rti_dir_path in sorted_entries:
        file_URLs = [str(get_url_for(rti_file_path, request)) for rti_file_path in rti_dir_path.iterdir()]
        info_URL = next((url for url in file_URLs if url.endswith("info.json")), None)

        RTIs.append({
            "id": rti_dir_path.name,
            "url": info_URL,
            "files": file_URLs,
        })
    
    return RTIs
