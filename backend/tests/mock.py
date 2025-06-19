import mimetypes
import os
import io
import zipfile
import json
from pathlib import Path


def create_mock_json(
    filename: str, content: dict = None
) -> tuple[str, io.BytesIO, str]:
    """Creates a tuple (filename, content, mime_type) that mocks a JSON file.
    If content is not specified, it will generate a simple JSON object with a random value for uniqueness.
    """
    if content is None:
        content = {"random": os.urandom(4).hex()}  # random hex for uniqueness

    json_bytes = json.dumps(content).encode("utf-8")
    return (filename, io.BytesIO(json_bytes), "application/json")


def create_mock_jpeg(
    filename: str, content: bytes = None
) -> tuple[str, io.BytesIO, str]:
    """Creates a tuple (filename, content, mime_type) that mocks a jpeg image file.
    If content is not specified then it will be a random byte stream to simulate uniqueness of files.
    """
    if content is None:
        content = os.urandom(8)  # 8 random bytes for uniqueness
    full_content = (
        b"\xff\xd8\xff\xe0" + content + b"\xff\xd9"
    )  # add jpeg specific header and EOF
    return (filename, io.BytesIO(full_content), "image/jpeg")


def create_mock_zip(
    filename: str, files: tuple[str, io.BytesIO, str]
) -> tuple[str, io.BytesIO, str]:
    """CReates a mozk zip that contains files specified."""
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as zf:
        for file in files:
            fname, content, _ = file
            zf.writestr(fname, content.getvalue())

    buffer.seek(0)

    return (filename, buffer, "application/zip")


def extract_mock_zip(zip: tuple[str, io.BytesIO, str]) -> list[tuple[str, io.BytesIO, str]]:
    _, zip_buffer, _ = zip
    zip_buffer.seek(0)

    extracted_files = []

    with zipfile.ZipFile(zip_buffer, "r") as zf:
        for filename in zf.namelist():
            file_bytes = zf.read(filename)
            file_io = io.BytesIO(file_bytes)
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type is None:
                mime_type = "application/octet-stream"

            extracted_files.append((filename, file_io, mime_type))

    zip_buffer.seek(0)
    return extracted_files


def create_mock_webrtis(n: int) -> list[tuple[str, io.BytesIO, str]]:
    zips = []
    for i in range(n):
        mock_zip_content = [
            create_mock_json("info.json"),
            *[create_mock_jpeg(f"plane_{i}.jpg") for i in range(6)],
        ]
        mock_zip = create_mock_zip(f"webrti_{i}.zip", mock_zip_content)
        zips.append(mock_zip)
    return zips


def compare_content(path: Path, bytes: io.BytesIO):
    return path.read_bytes() == bytes.getvalue()


def pretty_print_mock_zip(mock_zip):
    filename, buffer, mime_type = mock_zip
    # Move to start of buffer to read size
    buffer.seek(0, 2)  # seek to end
    size = buffer.tell()
    buffer.seek(0)  # rewind

    print(f"Mock zip file: {filename}")
    print(f"MIME type: {mime_type}")
    print(f"Size: {size} bytes")

    import zipfile

    with zipfile.ZipFile(buffer) as zf:
        print("Contents:")
        for name in zf.namelist():
            print(f" - {name}")
    buffer.seek(0)
