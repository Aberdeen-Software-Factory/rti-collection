from pathlib import Path
import shutil

from .paths import path_to_artifact


def find_first_in(dir: Path, pattern: str) -> Path | None: # TODO rewrite so that it aceopts a list of filenames and tries in order until first match is found
    for thumb_path in dir.rglob(pattern):
        return thumb_path


def cleanup(artifact_id: str):
    try:
        shutil.rmtree(str(path_to_artifact(artifact_id)))
    except FileNotFoundError:
        return