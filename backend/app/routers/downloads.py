import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..utils.auth import authenticate

from ..utils.paths import get_artifacts_root

router = APIRouter(
    tags=["Download"],
    dependencies=[Depends(authenticate)]
)


def stream_directory_as_zip(directory: Path, zip_name: str) -> StreamingResponse:
    if not directory.exists() or not directory.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    tmp = NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path = tmp.name

    shutil.make_archive(zip_path.replace(".zip", ""), "zip", directory)

    def iterfile():
        with open(zip_path, mode="rb") as file_like:
            yield from file_like
        os.unlink(zip_path)

    return StreamingResponse(
        iterfile(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={zip_name}.zip"},
    )


@router.get("/artifacts/download")
def download_all_artifacts():
    return stream_directory_as_zip(get_artifacts_root(), "artifacts")


@router.get("/artifacts/{id}/download")
def download_single_artifact(id: str):
    artifact_path = get_artifacts_root() / id
    return stream_directory_as_zip(artifact_path, id)


@router.get("/artifacts/{artifact_id}/rtis/{rti_id}/download")
def download_webrti(
    artifact_id: str,
    rti_id: str,
):
    relight_web_path = get_artifacts_root() / artifact_id / "rtis" / "web" / rti_id
    return stream_directory_as_zip(relight_web_path, rti_id)