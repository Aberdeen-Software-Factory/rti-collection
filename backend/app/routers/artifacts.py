from fastapi import APIRouter, Path, Request
from fastapi.responses import JSONResponse
from ..utils.paths import ARTIFACTS_DIR
from ..utils.filesys import find_first_in, read_metadata, read_images, read_RTIs
import os


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

    try:
        sorted_entries = sorted(
            ARTIFACTS_DIR.iterdir(),
            key=lambda p: p.stat().st_ctime,  # Sort by creation time
            reverse=True
        )
    except FileNotFoundError:
        return artifacts
    
    for artifact_path in sorted_entries:
        print("checking", artifact_path.name)
        
        metadata = read_metadata(artifact_path)

        # num_images = count_items_in_dir(os.path.join(artifact_dir, "images"))
        # num_rtis = count_items_in_dir(os.path.join(artifact_dir, "RTIs"))  # TODO rename rti to rtis

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

    return JSONResponse({
        "artifacts": artifacts
    })


@router.get("/{artifact_id}")
async def read_artifact(
    request: Request,
    artifact_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    artifact_path = ARTIFACTS_DIR / artifact_id

    metadata = read_metadata(artifact_path)
    images = read_images(artifact_path, request)
    RTIs = read_RTIs(artifact_path, request)

    artifact = {
        "id": artifact_id,
        **metadata,
        "imageURLs": images,
        "RTIs": RTIs,
    }
    
    return JSONResponse({
        "artifact": artifact
    })


# Utils


def count_items_in_dir(dir):
    try:
        with os.scandir(dir) as entries:
            return sum(1 for _ in entries)
    except FileNotFoundError:
        return 0
