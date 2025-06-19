import json
import shutil
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from ..model.model import Metadata
from ..utils.auth import authenticate
from ..utils.io import cleanup
from ..utils.io_savers import save_artifact
from ..utils.paths import path_to_artifact

authenticated_router = APIRouter(
    prefix="/artifacts",
    dependencies=[Depends(authenticate)]
)

@authenticated_router.post("/")
async def create_artifact(
    metadata: str = Form(None),
    images: list[UploadFile] = File(None),  # .jpg files - still images
    webrtis: list[UploadFile] = File(None), # .zip files containing info.json+plane_*.jpg as in Relight Web Format
    ptms: list[UploadFile] = File(None),    # .ptm files that can be converted to Relight Web Format via the relight-cli
):
    # Generate a unique artifact ID
    artifact_id = str(uuid.uuid4())
    print("ID:", artifact_id)

    try:
        webrti_ids = save_artifact(
            artifact_id,
            Metadata.model_validate_json(metadata or "{}"),
            images or [],
            webrtis or [],
            ptms or [],
        )
    except ValidationError:
        raise HTTPException(404, "Invalid metadata json string.") # TODO: wrong code probably?
    except Exception as error:
        cleanup(artifact_id)
        raise HTTPException(404, "Something went wrong." + str(error))

    return JSONResponse({
        "artifact_id": artifact_id, 
        "message": f"Successfully created artifact with ID: {artifact_id}",
        "webrti_ids": webrti_ids,
    })

@authenticated_router.put("/{artifact_id}")
async def update_artifact(
    artifact_id: str = Path(..., pattern=r"^[\w\-]+$"),
    metadata: str = Form(None),
    images: list[UploadFile] = File(None),
    webrtis: list[UploadFile] = File(None),
    ptms: list[UploadFile] = File(None),
):
    print("Recieved update with metadata:", metadata)

    artifact_dir = path_to_artifact(artifact_id)

    try:
        shutil.rmtree(str(artifact_dir))
        save_artifact(artifact_id, json.loads(metadata or "{}"), images, webrtis, ptms)
    except FileNotFoundError:
        raise HTTPException(404, f"Artifact with ID '{artifact_id}' not found.")
    except Exception as error:
        raise HTTPException(404, f"Error while updating artifact with ID '{artifact_id}'. {error}")

    return JSONResponse({"artifact_id": artifact_id, "message": "Upload successful"})

@authenticated_router.delete("/{artifact_id}")
def delete_artifact(
    artifact_id: str = Path(..., pattern=r"^[\w\-]+$"),
):
    artifact_dir = path_to_artifact(artifact_id)

    try:
        shutil.rmtree(artifact_dir)
    except FileNotFoundError:
        raise HTTPException(404, f"Artifact with ID {artifact_id} does not exist.")

    return JSONResponse({
        "artifact_id": artifact_id,
        "message": "Deleted successfully."
    })
