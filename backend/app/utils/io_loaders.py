from pathlib import Path

from fastapi import HTTPException, Request
from pydantic import HttpUrl, ValidationError

from ..schemas.model import Artifact, ArtifactPreview, Metadata, RTIImageBundle
from .io import find_first_in
from .url import get_static_file_url


class ArtifactNotFoundError(HTTPException):
    def __init__(self, id):
        super().__init__(404, f"Artifact with ID '{id}' cannot be found.")


def load_metadata(path: Path) -> Metadata:
    try:
        return Metadata.model_validate_json(path.read_text())
    except (ValidationError, FileNotFoundError):
        return Metadata()


def load_images(path: Path, request: Request) -> list[HttpUrl]:
    """Return a list of urls for the images contained in the directory path."""
    try:
        return [get_static_file_url(request, file) for file in path.iterdir()]
    except FileNotFoundError:
        return []


def load_webrtis(path: Path, request: Request) -> list[RTIImageBundle]:
    """Return a list of webrtis contained within the subdirectories of path."""
    try:
        return [load_webrti(subpath, request) for subpath in path.iterdir() if subpath.is_dir()]
    except FileNotFoundError:
        return []


def load_webrti(path: Path, request: Request) -> RTIImageBundle:
    """Return a webrti representing the relight web format object contained in directory path."""
    return RTIImageBundle(
        id=path.name,
        url=get_static_file_url(request, path),
        thumbnail=get_static_file_url(request, find_first_in(path, "plane_0.jpg")),
        filenames=[
            name.name for name in path.iterdir()
        ]
    )


def load_artifact(path: Path, request: Request) -> Artifact:
    if not path.is_dir():
        raise ArtifactNotFoundError(path.name)

    return Artifact(
        id=path.name,
        metadata=load_metadata(path / "metadata.json"),
        images=load_images(path / "images", request),
        rtis=load_webrtis(path / "rtis" / "web", request)
    )


def load_artifact_previews(paths: list[Path], request: Request) -> list[ArtifactPreview]:
    return [
        load_artifact_preview(artifact_path, request)
        for artifact_path in paths
    ]


def load_artifact_preview(path: Path, request: Request) -> ArtifactPreview:
    if not path.is_dir():
        raise ArtifactNotFoundError(path.name)

    metadata = load_metadata(path / "metadata.json")
    thumbnail_path = find_first_in(path, "plane_0.jpg") or find_first_in(path, "*.jpg")

    return ArtifactPreview(
        id=path.name,
        metadata=metadata,
        thumbnailURL=get_static_file_url(request, thumbnail_path),
    )
