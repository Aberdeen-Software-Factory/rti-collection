import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import artifacts, authenticated_artifacts, ptm_to_rti
from .utils.paths import get_artifacts_root

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://aberdeen-software-factory.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=100,
)

app.include_router(artifacts.router)
app.include_router(authenticated_artifacts.authenticated_router)
app.include_router(ptm_to_rti.router)


os.makedirs(get_artifacts_root(), exist_ok=True)
app.mount(
    "/uploads/artifacts", StaticFiles(directory=get_artifacts_root()), name="artifacts"
)
