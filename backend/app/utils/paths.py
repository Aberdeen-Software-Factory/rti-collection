from os.path import join


# ARTIFACTS_DIR = join("uploads", "artifacts")
ARTIFACTS_DIR = "uploads/artifacts/"

def path_to_artifact(id):
    """Returns the path to file directory containing the artifact with the specified ID."""
    return join(ARTIFACTS_DIR, id)

def path_to_artifact_images(id):
    """Returns the path to file directory containing the artifact images for the specified ID."""
    return join(path_to_artifact(id), "images")

def path_to_artifact_RTIs(id):
    """Returns the path to file directory containing the artifact RTIs for the specified ID."""
    return join(path_to_artifact(id), "RTIs")