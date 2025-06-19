from pathlib import Path

from fastapi import Request

from .paths import relative_to_artifacts_dir


def get_static_file_url(request: Request, path: Path) -> str:
    if path is None:
        return ""
    path_without_artifacts_dir = relative_to_artifacts_dir(path)
    return str(request.url_for("artifacts", path=str(path_without_artifacts_dir)))
