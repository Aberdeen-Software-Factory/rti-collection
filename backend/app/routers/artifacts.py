from fastapi import APIRouter, Form, UploadFile, File, Path, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Union
import uuid
import os
import shutil
import json
from ..utils.paths import ARTIFACTS_DIR
from urllib.parse import urljoin
from ..utils.utils import find_first_thumbnail_in, find_first_in
from ..utils.paths import path_to_artifact_images
import pathlib

router = APIRouter(
    prefix="/artifacts",
)


# Endpoints


@router.get("/")
async def read_artifacts(
    request: Request,
    # page_number: int = Query(1, alias="page[number]"),
    # page_size: int = Query(50, alias="page[size]")
):
    artifacts = []

    if not ARTIFACTS_DIR.exists():
        return JSONResponse(content={"artifacts": []})

    sorted_entries = sorted(
        ARTIFACTS_DIR.iterdir(),
        key=lambda p: p.stat().st_ctime,
        reverse=True
    )
    
    for artifact_path in sorted_entries:
        print("checking", artifact_path.name)
        
        metadata_path = artifact_path / "metadata.json"
        try:
            metadata = json.loads(metadata_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            metadata = {}

        # num_images = count_items_in_dir(os.path.join(artifact_dir, "images"))
        # num_rtis = count_items_in_dir(os.path.join(artifact_dir, "RTIs"))  # TODO rename rti to rtis

        
        # artifact = get_artifact_preview(artifact_id, base_url=str(request.base_url))

        thumbnail_path = find_first_thumbnail_in(artifact_path)
        if thumbnail_path is None:
            thumbnail_path = find_first_in(artifact_path, "plane_0.jpg")
        if thumbnail_path is not None:
            thumbnail_path = str(request.url_for("artifacts", path=str(thumbnail_path.relative_to(ARTIFACTS_DIR)))) # TODO put this into a function to avoid repetition

        # Build the artifact JSON
        artifact = {
            "id": artifact_path.name,
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "creator": metadata.get("creator", "Unknown"),
            "date": metadata.get("date", ""),
            "copyright": metadata.get("copyright", ""),
            "tags": metadata.get("tags", []),
            # "num_images": num_images,
            # "num_rtis": num_rtis,
            # "URL": str(request.url_for("artifacts", path=str(artifact_path.relative_to(ARTIFACTS_DIR)))),
            "thumbnailURL": thumbnail_path,
        }

        artifacts.append(artifact)

    return {"artifacts": artifacts}


@router.get("/{artifact_id}")
async def get_artifact(
    request: Request,
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    artifact_path = ARTIFACTS_DIR / artifact_id

    metadata_path = artifact_path / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        metadata = {}

    # Collect all image files at root level
    try:
        images = [str(request.url_for("artifacts", path=str(img_path.relative_to(ARTIFACTS_DIR)))) for img_path in path_to_artifact_images(artifact_id).iterdir() if img_path.is_file()]
    except FileNotFoundError:
        images = []

    # Collect RTI relightable media
    relightable_media = get_relightable_images(artifact_id, request, base_url=str(request.base_url))

    artifact = {
        "id": artifact_id,
        **metadata,
        "imageURLs": images,
        "RTIs": relightable_media,
    }
    
    return { "artifact": artifact }


@router.delete("/{artifact_id}/rti/{rti_id}")
async def delete_rti(
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
    rti_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    rti_path = os.path.join(ARTIFACTS_DIR, artifact_id, "rti", rti_id)

    if not os.path.exists(rti_path):
        raise HTTPException(status_code=404, detail="RTI directory not found")

    try:
        shutil.rmtree(rti_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete RTI: {str(e)}")

    return {"detail": f"RTI {rti_id} deleted successfully"}

# Utils

def is_rti_dir(path):
    return os.path.exists(os.path.join(path, "info.json"))


def count_items_in_dir(dir):
    try:
        with os.scandir(dir) as entries:
            return sum(1 for _ in entries)
    except FileNotFoundError:
        return 0

def get_relightable_images(artifact_id, request: Request, base_url=""):
    relightable_media = []
    RTIs_dir = os.path.join(ARTIFACTS_DIR, artifact_id, "RTIs")

    if not os.path.exists(RTIs_dir) or not os.path.isdir(RTIs_dir):
        return relightable_media
    
    for subdir_name in os.listdir(RTIs_dir):
        subdir_path = os.path.join(RTIs_dir, subdir_name)
        if os.path.isdir(subdir_path) and is_rti_dir(subdir_path):
            info_url = os.path.join(subdir_path, "info.json")
            
            thumbnail_url = find_first_thumbnail_in(pathlib.Path(subdir_path))
            if thumbnail_url is None:
                thumbnail_url = find_first_in(pathlib.Path(subdir_path), "plane_0.jpg")
            if thumbnail_url is not None:
                thumbnail_url = str(request.url_for("artifacts", path=str(thumbnail_url.relative_to(ARTIFACTS_DIR)))) # TODO put this into a function to avoid repetition

            files = []
            for filename in pathlib.Path(subdir_path).iterdir():
                files.append(str(request.url_for("artifacts", path=str(filename.relative_to(ARTIFACTS_DIR)))))
            
            relightable_entry = {
                "id": subdir_name,
                "type": "relight",
                "url": urljoin(base_url, info_url),
                "files": files,
            }
            if thumbnail_url:
                relightable_entry["thumbnail"] = thumbnail_url

            relightable_media.append(relightable_entry)

    return relightable_media

