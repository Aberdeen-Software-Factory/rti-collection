from fastapi import APIRouter, Path, Request

from ..model.model import ArtifactResponse, ArtifactsResponse
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


@router.get("/{artifact_id}")
async def read_artifact(
    request: Request,
    artifact_id: str = Path(..., pattern=r"^[\w\-]+$"),
) -> ArtifactResponse:
    artifact_path = path_to_artifact(artifact_id)
    artifact = load_artifact(artifact_path, request)

    return ArtifactResponse(
        artifact=artifact,
    )
