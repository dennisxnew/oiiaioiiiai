from unittest.mock import MagicMock, patch

import pytest
from backend.src.services.gcs_service import GCSConfigService, get_gcs_config_service


@pytest.fixture
def mock_gcs_client():
    with patch('google.cloud.storage.Client') as MockClient:
        mock_client_instance = MockClient.return_value
        yield mock_client_instance

@pytest.fixture
def mock_gcs_bucket(mock_gcs_client):
    mock_bucket = MagicMock()
    mock_gcs_client.bucket.return_value = mock_bucket
    return mock_bucket

@pytest.fixture
def mock_gcs_blob(mock_gcs_bucket):
    mock_blob = MagicMock()
    mock_gcs_bucket.blob.return_value = mock_blob
    return mock_blob

def test_gcs_config_service_init(mock_gcs_client, mock_gcs_bucket, mock_gcs_blob):
    service = GCSConfigService("test-bucket", "test-path.json")
    mock_gcs_client.bucket.assert_called_with("test-bucket")
    mock_gcs_bucket.blob.assert_called_with("test-path.json")
    assert service.bucket_name == "test-bucket"
    assert service.config_file_path == "test-path.json"

def test_load_config_success(mock_gcs_blob):
    mock_gcs_blob.download_as_text.return_value = '{"key": "value"}'
    service = GCSConfigService("test-bucket", "test-path.json")
    config = service.load_config()
    assert config == {"key": "value"}
    mock_gcs_blob.download_as_text.assert_called_once()

def test_load_config_file_not_found(mock_gcs_blob):
    mock_gcs_blob.download_as_text.side_effect = Exception("File not found")
    service = GCSConfigService("test-bucket", "test-path.json")
    config = service.load_config()
    assert config == {} # Should return empty dict on error
    mock_gcs_blob.download_as_text.assert_called_once()

def test_save_config_success(mock_gcs_blob):
    service = GCSConfigService("test-bucket", "test-path.json")
    config_data = {"new_key": "new_value"}
    service.save_config(config_data)
    mock_gcs_blob.upload_from_string.assert_called_once_with('{"new_key": "new_value"}', content_type="application/json")

def test_save_config_failure(mock_gcs_blob):
    mock_gcs_blob.upload_from_string.side_effect = Exception("Upload failed")
    service = GCSConfigService("test-bucket", "test-path.json")
    config_data = {"new_key": "new_value"}
    with pytest.raises(Exception, match="Upload failed"):
        service.save_config(config_data)
    mock_gcs_blob.upload_from_string.assert_called_once()

@patch('os.getenv')
def test_get_gcs_config_service_initialization(mock_getenv, mock_gcs_client):
    mock_getenv.side_effect = lambda x: "test-bucket" if x == "GCS_BUCKET_NAME" else "config.json"
    service = get_gcs_config_service()
    assert isinstance(service, GCSConfigService)
    assert service.bucket_name == "test-bucket"
    mock_gcs_client.assert_called_once() # Client should be initialized
    assert get_gcs_config_service() is service # Should return same instance on subsequent calls

@patch('os.getenv')
def test_get_gcs_config_service_no_bucket_name(mock_getenv):
    mock_getenv.side_effect = lambda x: None if x == "GCS_BUCKET_NAME" else "config.json"
    with pytest.raises(ValueError, match="GCS_BUCKET_NAME environment variable not set."):
        get_gcs_config_service()
