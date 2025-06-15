from fastapi import APIRouter, Form, UploadFile, File, Path, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Union
from app.utils.utils import upload_files, get_artifact_preview
import uuid
import os
import shutil
import json
from ..utils.paths import ARTIFACTS_DIR
from urllib.parse import urljoin

router = APIRouter(
    prefix="/artifacts",
)


# Endpoints


@router.get("/")
async def read_artifacts(request: Request):
    artifacts = []

    if not os.path.exists(ARTIFACTS_DIR):
        return JSONResponse(content={"artifacts": []})

    for artifact_id in os.listdir(ARTIFACTS_DIR):
        print("checking", artifact_id)
        artifact_dir = os.path.join(ARTIFACTS_DIR, artifact_id)

        if not os.path.isdir(artifact_dir):
            continue

        metadata_file = os.path.join(artifact_dir, "metadata.json")
        if not os.path.exists(metadata_file):
            continue

        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
        except json.JSONDecodeError:
            continue

        num_images = count_items_in_dir(os.path.join(artifact_dir, "images"))
        num_rtis = count_items_in_dir(os.path.join(artifact_dir, "RTIs"))  # TODO rename rti to rtis

        artifact = get_artifact_preview(artifact_id, base_url=str(request.base_url))


        # Build the artifact JSON
        # artifact = {
        #     "id": artifact_id,
        #     "title": metadata.get("title", ""),
        #     "description": metadata.get("description", ""),
        #     "creator": metadata.get("creator", "Unknown"),
        #     "date": metadata.get("date", ""),
        #     "copyright": metadata.get("copyright", ""),
        #     "tags": metadata.get("tags", []),
        #     "num_images": num_images,
        #     "num_rtis": num_rtis,
        #     "thumbnail": thumbnail_file.replace("uploads", "/files"),
        # }

        artifacts.append(artifact)

    return {"artifacts": artifacts}



@router.get("/{artifact_id}")
async def get_artifact(
    request: Request,
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    artifact_dir = os.path.join(ARTIFACTS_DIR, artifact_id)
    metadata_file = os.path.join(artifact_dir, 'metadata.json')

    # Collect all image files at root level
    images = [urljoin(str(request.base_url), img_path) for img_path in read_images(artifact_id)]

    # Collect RTI relightable media
    relightable_media = get_relightable_images(artifact_id, base_url=str(request.base_url))

    metadata = {}
    try:
        with open(metadata_file) as f:
            metadata = json.load(f)
    except json.JSONDecodeError:
        pass

    print(metadata)
    artifact = {
        "id": artifact_id,
        **metadata,
        "images": images,
        "relightableMedia": relightable_media,
    }
    
    return { "artifact": artifact }


def put_images(dir, images: list[Union[UploadFile, str]]):
    os.makedirs(dir, exist_ok=True)

    # Save images
    images_to_keep = [os.path.basename(image) for image in images if isinstance(image, str)]
    
    # Delete files
    for filename in os.listdir(dir):
        if filename not in images_to_keep:
            file_path = os.path.join(dir, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")

    # Add new image files
    for image_file in images:
        if not isinstance(image_file, str):
            image_path = os.path.join(dir, image_file.filename)
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
                print(f"Added: {image_file.filename}")




@router.post("/rti")
async def upload_relight(
    metadata: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # Generate a unique folder for this upload
    artifact_id = str(uuid.uuid4())
    rti_id = str(uuid.uuid4())
    artifact_folder = os.path.join(ARTIFACTS_DIR, artifact_id)
    relight_folder = os.path.join(artifact_folder, 'rti', rti_id)
    os.makedirs(relight_folder, exist_ok=True)

    # Save metadata JSON
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"error": "Invalid metadata JSON"})

    with open(os.path.join(artifact_folder, "metadata.json"), "w") as f:
        json.dump(metadata_dict, f, indent=2)

    # Save uploaded files
    for file in files:
        file_path = os.path.join(relight_folder, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    return {"artifact_id": artifact_id, "message": "Upload successful"}

@router.post("/{artifact_id}/rti")
async def upload_relight(
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
    metadata: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # Generate a unique folder for this upload
    rti_id = str(uuid.uuid4())
    artifact_folder = os.path.join(ARTIFACTS_DIR, artifact_id)
    relight_folder = os.path.join(artifact_folder, 'rti', rti_id)
    os.makedirs(relight_folder, exist_ok=True)

    # Save metadata JSON
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"error": "Invalid metadata JSON"})

    with open(os.path.join(artifact_folder, "metadata.json"), "w") as f:
        json.dump(metadata_dict, f, indent=2)

    # Save uploaded files
    for file in files:
        file_path = os.path.join(relight_folder, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    return {"artifact_id": artifact_id, "message": "Upload successful"}


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

def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif"])

def is_rti_dir(path):
    return os.path.exists(os.path.join(path, "info.json"))

def read_images(artifact_id):
    artifact_dir = os.path.join(ARTIFACTS_DIR, artifact_id)
    images_dir = os.path.join(artifact_dir, "images")
    images = []

    if not os.path.exists(images_dir) or not os.path.isdir(images_dir):
        return images
    
    for file_name in os.listdir(images_dir):
        file_path = os.path.join(images_dir, file_name)
        if os.path.isfile(file_path) and is_image_file(file_name):
            images.append(file_path)  # TODO how should returned url look?
    return images

def count_items_in_dir(dir):
    try:
        with os.scandir(dir) as entries:
            return sum(1 for _ in entries)
    except FileNotFoundError:
        return 0

def get_relightable_images(artifact_id, base_url=""):
    relightable_media = []
    RTIs_dir = os.path.join(ARTIFACTS_DIR, artifact_id, "RTIs")

    if not os.path.exists(RTIs_dir) or not os.path.isdir(RTIs_dir):
        return relightable_media
    
    for subdir_name in os.listdir(RTIs_dir):
        subdir_path = os.path.join(RTIs_dir, subdir_name)
        if os.path.isdir(subdir_path) and is_rti_dir(subdir_path):
            info_url = os.path.join(subdir_path, "info.json")
            
            thumbnail_path = os.path.join(subdir_path, "thumbnail.jpg")
            if os.path.exists(thumbnail_path):
                thumbnail_url = f"/files/artifacts/{artifact_id}/RTIs/{subdir_name}/thumbnail.jpg"
            else:
                fallback_thumb_path = os.path.join(subdir_path, f"{subdir_name}.jpg")
                if os.path.exists(fallback_thumb_path):
                    thumbnail_url = f"/files/artifacts/{artifact_id}/RTIs/{subdir_name}/{subdir_name}.jpg"
                else:
                    thumbnail_url = None

            files = []
            for filename in os.listdir(subdir_path):
                files.append(filename)
            
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

