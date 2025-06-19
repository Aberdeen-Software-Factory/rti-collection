import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
from app.model.model import ArtifactResponse, ArtifactsResponse

@pytest.fixture
def client_with_temp_upload(tmp_path, monkeypatch):
    mock_uploads = Path(__file__).parent / "assets" / "mock_uploads"
    
    monkeypatch.setattr("app.utils.paths.ARTIFACTS_DIR", mock_uploads)

    yield TestClient(app), tmp_path

def test_read_single_artifact(client_with_temp_upload):
    client, _ = client_with_temp_upload

    response = client.get("/artifacts/id1")

    print(response.text)
    o = ArtifactResponse.model_validate_json(response.text)

    print("list", o.model_dump_json(indent=2))
    #TODO: make sure values are as excpected too

def test_read_artifacts(client_with_temp_upload):
    client, _ = client_with_temp_upload

    response = client.get("/artifacts")

    print(response.text)
    o = ArtifactsResponse.model_validate_json(response.text)
    #TODO: make sure values are as excpected too
    print(o.artifacts)
    # raise Exception()