from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import List, Union
import uuid
import os
import json
import shutil
from fastapi.middleware.cors import CORSMiddleware
from .routers import artifacts
from .routers import secret
from .utils.paths import ARTIFACTS_DIR

app = FastAPI()

app.include_router(artifacts.router)
app.include_router(secret.authenticated_router)

# Allow requests from your Vue dev server
origins = [
    "http://localhost:5173",  # Vue dev server
    "http://localhost:3000",
    "http://127.0.0.1:60054",
    "https://zsoltkebel.github.io/",
    # add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Only allow specific dev URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def artifact_dir(id):
    return os.path.join(ARTIFACTS_DIR, id)


from fastapi.staticfiles import StaticFiles
app.mount("/uploads/artifacts", StaticFiles(directory=ARTIFACTS_DIR), name="artifacts")







@app.post("/artifact/update/")
async def remove_artifact():
    pass

@app.delete("/artifact/{id}")
async def delete_artifact(
    id: str = Path(..., regex=r"^[\w\-]+$")
):
    artifact_path = os.path.join(ARTIFACTS_DIR, id)

    if not os.path.exists(artifact_path) or not os.path.isdir(artifact_path):
        raise HTTPException(status_code=404, detail="Artifact not found")

    try:
        shutil.rmtree(artifact_path)
        return {"status": "success", "removed": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove artifact: {str(e)}")
    

@app.post("/artifact/{id}/upload-rti")
async def upload_rti(
    id: str = Path(..., regex=r"^[\w\-]+$"),
    files: list[UploadFile] = File([]),
):
    # Create directories
    rti_id = str(uuid.uuid4())
    artifact_dir = os.path.join(ARTIFACTS_DIR, id)
    images_dir = os.path.join(artifact_dir, "rti", rti_id)
    os.makedirs(images_dir, exist_ok=True)

    # Save images
    for image_file in files:
        image_path = os.path.join(images_dir, image_file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)

@app.delete("/artifact/{id}/rti/{rti_id}")
async def delete_rti(
    id: str = Path(..., regex=r"^[\w\-]+$"),  # Artifact ID
    rti_id: str = Path(..., regex=r"^[\w\-]+$"),
):
    rti_path = os.path.join(ARTIFACTS_DIR, id, "rti", rti_id)

    if not os.path.exists(rti_path) or not os.path.isdir(rti_path):
        raise HTTPException(status_code=404, detail="Artifact not found")

    try:
        shutil.rmtree(rti_path)
        return {"status": "success", "removed": rti_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove artifact rti: {str(e)}")