import pytest
from app.main import app
from app.utils.auth import authenticate
from app.utils.paths import get_path_to_webrtis, path_to_artifact
from fastapi.testclient import TestClient

from .mock import (
    create_mock_jpeg,
    create_mock_webrtis,
    extract_mock_zip,
)


@pytest.fixture
def client_with_temp_upload(tmp_path, monkeypatch):
    def override_auth():
        return {"username": "testuser"}
    app.dependency_overrides[authenticate] = override_auth

    # persistent_dir = Path(__file__).parent / "test_uploads"
    # persistent_dir.mkdir(exist_ok=True)
    
    monkeypatch.setattr("app.utils.paths.ARTIFACTS_DIR", tmp_path)

    yield TestClient(app), tmp_path


def test_upload_image(client_with_temp_upload):
    """Test that when uploading, images get put into correct folder structure with correct content.
    
    They should be in the upload directory under: `/artifacts/<id>/images/<file.jpg>`
    """
    client, tmp_path = client_with_temp_upload

    mock_images = [
        create_mock_jpeg("file1.jpg"),
        create_mock_jpeg("file2.jpg"),
    ]

    files = [("images", f) for f in mock_images]

    response = client.post("/artifacts", files=files)
    print(response.json())
    assert response.status_code == 200

    artifact_id = response.json()["artifact_id"]

    # Validate that the uploaded files exist and match content
    for filename, original_content, _ in mock_images:
        uploaded_image = tmp_path / artifact_id / "images" / filename
        assert uploaded_image.exists()
        uploaded_bytes = uploaded_image.read_bytes()
        assert uploaded_bytes == original_content.getvalue()


def test_upload_webrti(client_with_temp_upload):
    """Test that when uploading, webrtis get put into correct folder structure with correct content.
    
    They should be in the upload directory under: `/artifacts/<id>/rtis/web/<rti_id>/<file.jpg>`
    """
    client, tmp_path = client_with_temp_upload

    mock_zips = create_mock_webrtis(4)
    files = [("webrtis", mock_zip) for mock_zip in mock_zips]

    response = client.post("/artifacts", files=files)

    artifact_id = response.json()["artifact_id"]
    webrti_ids = response.json()["webrti_ids"]
    print("ids", webrti_ids)
    a_path = path_to_artifact(artifact_id)

    # Validate that the uploaded files exist and match content
    for i, mock_zip in enumerate(mock_zips):
        for filename, original_content, _ in extract_mock_zip(mock_zip):
            uploaded_file = get_path_to_webrtis(a_path) / webrti_ids[i] / filename
            assert uploaded_file.exists()
            uploaded_bytes = uploaded_file.read_bytes()
            assert uploaded_bytes == original_content.getvalue()

