import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import artifact_reads, artifact_writes, converter, downloads
from .utils.paths import get_artifacts_root

app = FastAPI(
    title="Artifact API",
    description="An API to manage digital artifact metadata, images, and RTI bundles.",
    version="1.0.0",
    openapi_tags=[
        {"name": "View", "description": "Endpoints for retrieving artifact data."},
        {"name": "Edit", "description": "Endpoints for creating or modifying artifacts."},
        {"name": "Download", "description": "Endpoints for downloading files."},
        {"name": "Convert", "description": "Endpoints for converting between various RTI file formats."},
    ],
)

origins = [
    "http://localhost:5173",
    "https://aberdeen-software-factory.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=100,
)

app.include_router(downloads.router)
app.include_router(artifact_reads.router)
app.include_router(artifact_writes.authenticated_router)
app.include_router(converter.router)


os.makedirs(get_artifacts_root(), exist_ok=True)
app.mount(
    "/uploads/artifacts", StaticFiles(directory=get_artifacts_root()), name="artifacts"
)
