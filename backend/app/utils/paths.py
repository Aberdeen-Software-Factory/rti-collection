import os
from pathlib import Path


# ARTIFACTS_DIR = join("uploads", "artifacts")
# ARTIFACTS_DIR = Path("uploads2", "artifacts")
ARTIFACTS_DIR = Path(os.environ.get("ARTIFACTS_DIR", "uploads2/artifacts"))

def get_artifacts_root() -> Path:
    return ARTIFACTS_DIR

def path_to_artifact(id: str) -> Path:
    """Returns the path to file directory containing the artifact with the specified ID."""
    return ARTIFACTS_DIR / id

def path_to_artifact_images(id: str) -> Path:
    """Returns the path to file directory containing the artifact images for the specified ID."""
    return path_to_artifact(id) / "images"

def path_to_artifact_RTIs(id: str) -> Path:
    """Returns the path to file directory containing the artifact RTIs for the specified ID."""
    return path_to_artifact(id) / "RTIs"


def get_path_to_metadata(path_to_artifact: Path):
    return path_to_artifact / "metadata.json"

def get_path_to_images(path_to_artiafact: Path):
    return path_to_artiafact / "images"

def get_path_to_webrtis(path_to_artifact: Path):
    return path_to_artifact / "rtis" / "web"

def get_path_to_ptms(path_to_artifact: Path):
    return path_to_artifact / "rtis" / "ptm"

def relative_to_artifacts_dir(path: Path):
    return path.relative_to(ARTIFACTS_DIR)