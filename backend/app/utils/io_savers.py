import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path

from fastapi import UploadFile

from ..model.model import Metadata
from .paths import (
    get_path_to_images,
    get_path_to_ptms,
    get_path_to_webrtis,
    path_to_artifact,
)
from .relight_cli import call_relight_cli


def save_files(dest: Path, files: list[UploadFile]):
    for file in files:
        save_file(dest, file)


def save_file(dest: Path, file: UploadFile):
    file_path = dest / file.filename
    with open(str(file_path), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


def save_metadata(dest: Path, data: Metadata):
    file_path = dest / "metadata.json"
    file_path.write_text(data.model_dump_json(indent=2))


def save_webrtis(dest: Path, zips: list[UploadFile]) -> list[str]:
    ids = []
    for zip in zips:
        id, files = save_webrti(dest, zip)
        ids.append(id)
    return ids


def save_webrti(dest: Path, zip: UploadFile) -> tuple[str, list[Path]]:
    rti_id = str(uuid.uuid4())
    rti_dir_path = dest / rti_id
    rti_dir_path.mkdir(parents=True)

    file_paths = []

    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        shutil.copyfileobj(zip.file, tmp)
        tmp.flush()
        tmp_path = tmp.name

        with zipfile.ZipFile(tmp_path, "r") as zip_file:
            # Discard intermediate folders and only keep specific files
            for member in zip_file.infolist():
                if member.is_dir():
                    continue

                filename = Path(member.filename).name

                if filename == "info.json" or filename.startswith("plane_"):
                    file_path = rti_dir_path / filename
                    with (
                        zip_file.open(member) as source,
                        open(str(file_path), "wb") as target,
                    ):
                        shutil.copyfileobj(source, target)
                    file_paths.append(file_path)

    return rti_id, file_paths


def save_ptm(
    dest: Path, webrti_dest: Path, file: UploadFile
) -> tuple[str, list[Path], Path]:
    """Upload a RTI file in the .ptm format and convert it to Relight Web Format."""
    rti_id = str(uuid.uuid4())

    dest.mkdir(parents=True, exist_ok=True)
    save_file(dest, file)

    webrti_path = webrti_dest / rti_id
    webrti_path.mkdir(parents=True)

    with tempfile.NamedTemporaryFile(suffix=".ptm") as temp_ptm:
        file.file.seek(0)
        shutil.copyfileobj(file.file, temp_ptm)
        temp_ptm.flush()
        try:
            call_relight_cli(temp_ptm.name, str(webrti_path))
            print(f"Successfully converted {file.filename} file.")
            file_paths = [file for file in webrti_path.iterdir()]
            return rti_id, file_paths, dest / file.filename
        except Exception as e:
            shutil.rmtree(str(webrti_path))
            (dest / file.filename).unlink()
            print(f"Error while converting {file.filename} file.", e)
            # raise e


def save_artifact(
    id: str,
    metadata: Metadata,
    images: list[UploadFile],
    webrtis: list[UploadFile],
    ptms: list[UploadFile],
) -> list[str]:
    print("saving", id, metadata, images, webrtis, ptms)
    # Create directory
    artifact_dir = path_to_artifact(id)

    # Upload artifact metadata
    save_metadata(artifact_dir, metadata)

    images_dir = get_path_to_images(artifact_dir)
    images_dir.mkdir()
    save_files(images_dir, images or [])

    webrtis_dir = get_path_to_webrtis(artifact_dir)
    webrti_ids = save_webrtis(webrtis_dir, webrtis or [])

    ptms_dir = get_path_to_ptms(artifact_dir)
    for ptm in ptms or []:
        save_ptm(ptms_dir, webrtis_dir, ptm)

    return webrti_ids
