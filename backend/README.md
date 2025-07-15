## Overview

This RESTful API enables external systems to query artifact data stored in the file system. Supported operations include:
- Paginated listing of artifacts
- Query of single artifact by ID
- Creating, editing, and deleting artifacts
- Converting `.ptm` files to the Relight Web format using the [Relight Lab CLI](https://github.com/cnr-isti-vclab/relight)

The API is built with [FastAPI](https://fastapi.tiangolo.com)

## Install

1. The [Relight Lab CLI](https://github.com/cnr-isti-vclab/relight) must be installed and available on the host system for file conversion endpoints to work. (The API will still function without it, but conversion will be disabled.)
1. Set the following environment variables:
    - `API_USERNAME` and `API_PASSWORD` for [HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/) on write operations.
    - `ARTIFACTS_DIR` (optional, defaults to `uploads/artifacts`), the root directory for all artifact data.
1. Set up a [virtual Python environment](https://docs.python.org/3/library/venv.html) and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    # When done
    deactivate
    ```

## Run Locally

From the `/backend` directory, start the development server with:
```
fastapi dev app/main.py
```
Make sure the required environment variables are set beforehand. (e.g. `export API_USERNAME="..."`)

## Run with Docker

The [Dockerfile](/backend/Dockerfile) uses a multi-stage build:
- Build stage: installs dependencies for compiling the Relight CLI.
- Run stage: installs only the required dependencies to run the API and CLI.

Build the Docker image::
```
docker build -t fastapi-relight .
```

Run the container with volume and environment configuration:
```
docker run -d \
    -v ./uploads/:/uploads \
    -e API_USERNAME="" \
    -e API_PASSWORD="..." \
    -p 8000:8000 \
    fastapi-relight
```

## Deploy

TODO once uni server hosting is set up

## Test

Run the tests from directory `/backend`:
```
pytest
```

## File structure

The `ARTIFACTS_DIR` (default: `uploads/artifacts`) is the root directory for artifact data, structured as follows:

```
artifacts/
└── [id]/
    ├── metadata.json
    ├── images/
    │   ├── image_1.jpg
    │   └── ...
    └── rtis/
        ├── web/
        │   └── [id]/
        │       ├── info.json
        │       ├── plane_0.jpg
        │       ├── plane_1.jpg
        │       └── ...
        └── ptm/
            ├── file.ptm
            └── ...
```

## Documentation

For a full API reference, visit the interactive Swagger UI generated at `/docs` when the server is running.

Additional details can be found in the source code via docstrings.

## Limitations & Future Work

Currently the file system stores all the image and relightable web format files which is ideal and probably should be kept in the future. However currently the metadata also lives in the same file structure in `metadata.json` files. Instead of this future work should try to create a database which would hold all these data with links to the actual image and other files within the filesystem. this would allow efficient sorting, filtering, searching.