from unittest.mock import patch

import pytest
from backend.src.main import app
from fastapi.testclient import TestClient


# Mock the GCSConfigService for tests
@pytest.fixture(autouse=True)
def mock_gcs_config_service():
    with patch('backend.src.services.gcs_service.GCSConfigService') as MockGCSConfigService:
        mock_instance = MockGCSConfigService.return_value
        # Default mock config
        mock_instance.load_config.return_value = {
            "confluence_config": {
                "enabled": True,
                "schedule": "0 10 * * 1",
                "confluence_url": "https://test.confluence.com",
                "slack_channel": "C12345"
            },
            "on_call_config": {
                "enabled": True,
                "schedule": "0 18 * * 5",
                "slack_channel": "C67890"
            },
            "on_call_schedule": {
                "current_index": 0,
                "roster": []
            }
        }
        yield mock_instance

@pytest.fixture
def client():
    # Use TestClient for FastAPI application
    return TestClient(app)

def test_get_app_config_success(client, mock_gcs_config_service):
    response = client.get("/api/config")

    assert response.status_code == 200
    assert response.json()["confluence_config"]["confluence_url"] == "https://test.confluence.com"
    mock_gcs_config_service.load_config.assert_called_once()

def test_put_app_config_success(client, mock_gcs_config_service):
    new_config_data = {
        "confluence_config": {
            "enabled": False,
            "schedule": "0 10 * * 1",
            "confluence_url": "https://new.confluence.com",
            "slack_channel": "C98765"
        },
        "on_call_config": {
            "enabled": False,
            "schedule": "0 18 * * 5",
            "slack_channel": "C54321"
        },
        "on_call_schedule": {
            "current_index": 0,
            "roster": []
        }
    }

    response = client.put("/api/config", json=new_config_data)

    assert response.status_code == 200
    assert response.json()["confluence_config"]["confluence_url"] == "https://new.confluence.com"
    mock_gcs_config_service.save_config.assert_called_once()
    args, kwargs = mock_gcs_config_service.save_config.call_args
    assert args[0]["confluence_config"]["confluence_url"] == "https://new.confluence.com"

def test_put_app_config_validation_error(client):
    invalid_config_data = {
        "confluence_config": {
            "enabled": True,
            "schedule": "invalid_cron", # Invalid schedule
            "confluence_url": "https://test.confluence.com",
            "slack_channel": "C12345"
        },
        "on_call_config": {
            "enabled": True,
            "schedule": "0 18 * * 5",
            "slack_channel": "C67890"
        },
        "on_call_schedule": {
            "current_index": 0,
            "roster": []
        }
    }

    response = client.put("/api/config", json=invalid_config_data)

    assert response.status_code == 422 # Pydantic validation error
    assert "value is not a valid cron expression" in response.json()["detail"][0]["msg"]
