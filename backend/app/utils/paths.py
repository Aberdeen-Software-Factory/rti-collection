from pathlib import Path


# ARTIFACTS_DIR = join("uploads", "artifacts")
ARTIFACTS_DIR = Path("uploads", "artifacts")

def path_to_artifact(id: str) -> Path:
    """Returns the path to file directory containing the artifact with the specified ID."""
    return ARTIFACTS_DIR / id

def path_to_artifact_images(id: str) -> Path:
    """Returns the path to file directory containing the artifact images for the specified ID."""
    return path_to_artifact(id) / "images"

def path_to_artifact_RTIs(id: str) -> Path:
    """Returns the path to file directory containing the artifact RTIs for the specified ID."""
    return path_to_artifact(id) / "RTIs"