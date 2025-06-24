from fastapi import APIRouter, Path, Request

from ..schemas.model import ArtifactResponse, ArtifactsResponse
from ..utils.io_loaders import load_artifact, load_artifact_previews
from ..utils.paths import get_artifacts_root, path_to_artifact

router = APIRouter(
    prefix="/artifacts",
)


@router.get("/")
async def read_artifacts(
    request: Request,
) -> ArtifactsResponse:
    artifacts = load_artifact_previews(get_artifacts_root(), request)

    return ArtifactsResponse(
        artifacts=artifacts,
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
