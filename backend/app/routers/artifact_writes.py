import shutil
from secrets import token_hex

from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from slugify import slugify

from ..schemas.model import Metadata
from ..utils.auth import authenticate
from ..utils.io import cleanup, delete_contents
from ..utils.io_savers import save_artifact
from ..utils.paths import path_to_artifact

authenticated_router = APIRouter(
    prefix="/artifacts",
    tags=["Edit"],
    dependencies=[Depends(authenticate)],
)

def generate_artifact_id(name: str) -> str:
    slug = slugify(name)[:50]
    suffix = token_hex(3)
    return f"{slug}_{suffix}"


@authenticated_router.post("/")
async def create_artifact(
    metadata: str = Form(None),
    images: list[UploadFile] = File(None),  # .jpg files - still images
    webrtis: list[UploadFile] = File(None), # .zip files containing info.json+plane_*.jpg as in Relight Web Format
    ptms: list[UploadFile] = File(None),    # .ptm files that can be converted to Relight Web Format via the relight-cli
):
    try:
        metadata_obj = Metadata.model_validate_json(metadata or "{}")
        print(metadata_obj)

        # Generate a unique artifact ID
        artifact_id = generate_artifact_id(metadata_obj.name or "a")
        print("ID:", artifact_id)

        artifact_dir = path_to_artifact(artifact_id)
        artifact_dir.mkdir(parents=True)

        webrti_ids = save_artifact(
            artifact_id,
            metadata_obj,
            images or [],
            webrtis or [],
            ptms or [],
        )
    except ValidationError:
        print("Invalid metadata json string.")
        raise HTTPException(404, "Invalid metadata json string.") # TODO: wrong code probably?
    except Exception as error:
        print(error)
        cleanup(artifact_id)
        raise HTTPException(404, "Something went wrong." + str(error))

    return JSONResponse({
        "artifact_id": artifact_id, 
        "message": f"Successfully created artifact with ID: {artifact_id}",
        "webrti_ids": webrti_ids,
    })

@authenticated_router.put("/{id}")
async def update_artifact(
    id: str = Path(..., pattern=r"^[\w\-]+$"),
    metadata: str = Form(None),
    images: list[UploadFile] = File(None),
    webrtis: list[UploadFile] = File(None),
    ptms: list[UploadFile] = File(None),
):
    print("Recieved update with metadata:", metadata)

    artifact_dir = path_to_artifact(id)

    try:
        delete_contents(artifact_dir)
        save_artifact(id, Metadata.model_validate_json(metadata or "{}"), images or [], webrtis or [], ptms or [])
    except FileNotFoundError:
        raise HTTPException(404, f"Artifact with ID '{id}' not found.")
    except Exception as error:
        raise HTTPException(404, f"Error while updating artifact with ID '{id}'. {error}")

    return JSONResponse({"artifact_id": id, "message": "Upload successful"})

@authenticated_router.delete("/{id}")
def delete_artifact(
    id: str = Path(..., pattern=r"^[\w\-]+$"),
):
    artifact_dir = path_to_artifact(id)

    try:
        shutil.rmtree(artifact_dir)
    except FileNotFoundError:
        raise HTTPException(404, f"Artifact with ID {id} does not exist.")

    return JSONResponse({
        "artifact_id": id,
        "message": "Deleted successfully."
    })
