from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import os
from ..utils.relight_cli import call_relight_cli
import tempfile
import zipfile
import shutil

router = APIRouter(
    prefix="/converter",
    tags=["Convert"],
)

@router.post("/")
async def convert_ptm_to_rti(
    files: list[UploadFile] = File(None),
    background_tasks: BackgroundTasks = None,
):
    # Use only the first uploaded file
    first_file = files[0]

    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(first_file.filename)[-1]) as temp_input:
        # tempfile.TemporaryDirectory(delete=False) as temp_output_dir:
        temp_input.write(await first_file.read())
        temp_input.flush()

        temp_output_dir = Path(tempfile.mkdtemp())
        call_relight_cli(temp_input.name, temp_output_dir)

        zip_path = Path(temp_output_dir) / "relight_output.zip"

        # Zip all contents of the output directory
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in Path(temp_output_dir).rglob("*"):
                if file_path != zip_path and file_path.is_file():
                    zipf.write(file_path, arcname=file_path.relative_to(Path(temp_output_dir)))

        # Register background task to delete the zip
        background_tasks.add_task(shutil.rmtree, temp_output_dir)

        return FileResponse(zip_path, filename="relight_output.zip", media_type="application/zip")
