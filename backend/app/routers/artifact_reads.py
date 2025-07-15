import math

from fastapi import APIRouter, Path, Query, Request

from ..schemas.model import ArtifactResponse, ArtifactsResponse
from ..utils.io_loaders import load_artifact, load_artifact_previews
from ..utils.paths import get_artifacts_root, path_to_artifact

router = APIRouter(
    prefix="/artifacts",
    tags=["View"],
)


@router.get("/")
async def read_artifacts(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, description="Number of artifacts per page"),
) -> ArtifactsResponse:
    try:
        sorted_entries = sorted(
            [p for p in get_artifacts_root().iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_ctime,  # Sort by creation time
            reverse=True,
        )
        
        total_pages = math.ceil(len(sorted_entries) / page_size)
        valid_page = min(page, total_pages)
        
        start = (valid_page - 1) * page_size
        end = start + page_size
        sorted_paged_entries = sorted_entries[start:end]
    except FileNotFoundError:
        return ArtifactResponse(artifact=[], page=page, pages=0)

    artifacts = load_artifact_previews(sorted_paged_entries, request)

    return ArtifactsResponse(
        artifacts=artifacts,
        page=valid_page,
        pages=total_pages,
    )


@router.get("/{id}")
async def read_artifact(
    request: Request,
    id: str = Path(..., pattern=r"^[\w\-]+$"),
) -> ArtifactResponse:
    artifact_path = path_to_artifact(id)
    artifact = load_artifact(artifact_path, request)

    return ArtifactResponse(
        artifact=artifact,
    )
