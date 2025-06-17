from fastapi import APIRouter, Depends, Form, UploadFile, File, Path, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
from ..utils.filesys import upload_files
import uuid
import os
import shutil
import json
import tempfile
from ..utils.auth import authenticate
from ..utils.paths import path_to_artifact, path_to_artifact_images, path_to_artifact_RTIs
from ..utils.relight_cli import call_relight_cli
import pathlib

# Config


authenticated_router = APIRouter(
    prefix="/artifacts",
    dependencies=[Depends(authenticate)]
)


# Endpoints


@authenticated_router.post("/")
async def create_artifact(
    request: Request,
    metadata: str = Form(None),
    images: list[UploadFile] = File(None), # TODO rename to image_files
    ptm_files: list[UploadFile] | None = File(None),
    RTIKeys: list[str] = None,
):
    # Generate a unique artifact ID
    artifact_id = str(uuid.uuid4())

    # Create directories
    artifact_dir = path_to_artifact(artifact_id)
    os.makedirs(artifact_dir)

    # Metadata
    update_metadata(artifact_id, metadata)

    # Images (still)
    update_images(artifact_id, images)
    
    # RTIs
    await update_RTIs(artifact_id, RTIKeys, request)

    #TODO upload ptm files too in future
    ptm_filenames_with_errors = []
    for ptm_file in ptm_files or []:
        os.makedirs(str(artifact_dir / "RTIs"), exist_ok=True)

        with tempfile.NamedTemporaryFile(suffix=pathlib.Path(ptm_file.filename).suffix) as temp_ptm:
            shutil.copyfileobj(ptm_file.file, temp_ptm)
            try:
                call_relight_cli(temp_ptm.name, str(artifact_dir / "RTIs" / str(uuid.uuid4())))
                print(f"Successfully converted {ptm_file.filename} file.")
            except Exception as e:
                print(f"Error while converting {ptm_file.filename} file.", e)
                ptm_filenames_with_errors.append(ptm_file.filename)

    return JSONResponse({
        "artifact_id": artifact_id, 
        "message": "Upload successful",
        "filesWithErrors": ptm_filenames_with_errors,
    })


@authenticated_router.put("/{artifact_id}")
async def update_artifact(
    request: Request,
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
    metadata: str = Form(None),
    images: list[Union[UploadFile, str]] = File(None),
    RTIKeys: list[str] = None,
):
    print("Recieved update with metadata:", metadata, "images:", images, "RTIs:", RTIKeys)

    # Check for artifact existence
    artifact_dir = path_to_artifact(artifact_id)
    if not os.path.exists(artifact_dir):
        raise HTTPException(status_code=404, detail=f"Artifact with id '{artifact_id}' not found.")

    # Metadata
    update_metadata(artifact_id, metadata)

    # Images (still)
    update_images(artifact_id, images)
    
    # RTIs
    await update_RTIs(artifact_id, RTIKeys, request)

    return JSONResponse({"artifact_id": artifact_id, "message": "Upload successful"})

@authenticated_router.delete("/{artifact_id}")
def delete_artifact(
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    artifact_dir = path_to_artifact(artifact_id)
    shutil.rmtree(artifact_dir)

    return JSONResponse({
        "artifact_id": artifact_id,
        "message": "Deleted successful"
    })


# Utils


def update_metadata(artifact_id, metadata):
    if metadata is not None:
        try:
            metadata_obj = json.loads(metadata)
            metadata_path = os.path.join(path_to_artifact(artifact_id), "metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata_obj, f, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in metadata")

def update_images(artifact_id, images):
    if images is not None:
        # Delete all previous images
        images_dir = path_to_artifact_images(artifact_id)
        try:
            shutil.rmtree(images_dir)
        except FileNotFoundError:
            pass
        os.makedirs(images_dir)
        # Upload new images
        upload_files(images_dir, images)

async def update_RTIs(artifact_id, RTIKeys, request):
    if RTIKeys is not None:
        # Delete all previous RTIs
        RTIs_dir = path_to_artifact_RTIs(artifact_id)
        try:
            shutil.rmtree(RTIs_dir)
        except FileNotFoundError:
            pass
        os.makedirs(RTIs_dir)
        # Upload new RTIs
        form = await request.form()  # For additional field such as for RTIs
        for RTIKey in RTIKeys:
            files = form.getlist(RTIKey)
            RTI_id = str(uuid.uuid4())
            RTI_dir = os.path.join(RTIs_dir, RTI_id)
            os.makedirs(RTI_dir)
            upload_files(RTI_dir, files)
