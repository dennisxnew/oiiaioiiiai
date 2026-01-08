from unittest.mock import patch

import pytest
from backend.src.main import app
from backend.src.models.config import (
    AppConfig,
    ConfluenceConfig,
    OnCallConfig,
    OnCallPerson,
    OnCallSchedule,
)
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
                "roster": [
                    {"name": "Alice", "slack_user_id": "U01A"},
                    {"name": "Bob", "slack_user_id": "U01B"}
                ]
            }
        }
        yield mock_instance

# Mock the Confluence and Slack services
@pytest.fixture
def mock_confluence_service():
    with patch('backend.src.services.confluence_service.ConfluenceService') as MockConfluenceService:
        yield MockConfluenceService.return_value

@pytest.fixture
def mock_slack_service():
    with patch('backend.src.services.slack_service.SlackService') as MockSlackService:
        yield MockSlackService.return_value

@pytest.fixture
def client():
    # Use TestClient for FastAPI application
    return TestClient(app)

def test_confluence_weekly_report_trigger_success(
    client,
    mock_gcs_config_service,
    mock_confluence_service,
    mock_slack_service
):
    # Ensure config loading happens correctly
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=True,
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=True,
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(roster=[])
        )
        mock_get_app_config.return_value = mock_app_config

        # Mock service calls
        mock_confluence_service.create_weekly_report.return_value = "https://new-confluence-page.com"
        mock_slack_service.send_message.return_value = None

        response = client.post("/schedule/confluence-weekly-report")

        assert response.status_code == 202
        assert response.json() == {"message": "Confluence weekly report generation triggered."}

        # Assert service methods were called with correct arguments
        mock_confluence_service.create_weekly_report.assert_called_once_with(
            mock_app_config.confluence_config
        )
        mock_slack_service.send_message.assert_called_once_with(
            channel=mock_app_config.confluence_config.slack_channel,
            message="Confluence weekly report created: https://new-confluence-page.com"
        )

def test_confluence_weekly_report_trigger_disabled(
    client,
    mock_gcs_config_service,
    mock_confluence_service,
    mock_slack_service
):
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=False, # Disabled
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=True,
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(roster=[])
        )
        mock_get_app_config.return_value = mock_app_config

        response = client.post("/schedule/confluence-weekly-report")

        assert response.status_code == 202
        assert response.json() == {"message": "Confluence weekly report generation is disabled."}

        # Assert no service methods were called
        mock_confluence_service.create_weekly_report.assert_not_called()
        mock_slack_service.send_message.assert_not_called()

def test_confluence_weekly_report_trigger_failure(
    client,
    mock_gcs_config_service,
    mock_confluence_service,
    mock_slack_service
):
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=True,
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=True,
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(roster=[])
        )
        mock_get_app_config.return_value = mock_app_config

        # Mock a failure in the Confluence service
        mock_confluence_service.create_weekly_report.side_effect = Exception("Confluence API Error")

        response = client.post("/schedule/confluence-weekly-report")

        assert response.status_code == 500
        assert "Confluence API Error" in response.json()["detail"]

        mock_confluence_service.create_weekly_report.assert_called_once()
        # Slack message should still be sent for error
        mock_slack_service.send_message.assert_called_once_with(
            channel=mock_app_config.confluence_config.slack_channel,
            message="Error generating Confluence weekly report: Confluence API Error"
        )

# --- New tests for on-call notification ---
def test_on_call_notification_trigger_success(
    client,
    mock_gcs_config_service,
    mock_slack_service
):
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=False,
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=True,
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(
                current_index=0,
                roster=[
                    OnCallPerson(name="Alice", slack_user_id="U01A"),
                    OnCallPerson(name="Bob", slack_user_id="U01B")
                ]
            )
        )
        mock_get_app_config.return_value = mock_app_config

        # Mock on-call service logic here (will be implemented later)
        with patch('backend.src.services.oncall_service.OnCallService.notify_on_call_person') as mock_notify:
            mock_notify.return_value = {"person": "Alice", "slack_id": "U01A"}

            response = client.post("/schedule/on-call-notification")

            assert response.status_code == 202
            assert response.json() == {"message": "On-call notification triggered for Alice (U01A)."}

            mock_notify.assert_called_once_with(
                on_call_config=mock_app_config.on_call_config,
                on_call_schedule=mock_app_config.on_call_schedule
            )
            # The next index should be updated and saved
            assert mock_gcs_config_service.save_config.call_count == 1
            saved_config = mock_gcs_config_service.save_config.call_args[0][0]
            assert saved_config["on_call_schedule"]["current_index"] == 1 # Alice was 0, next is Bob at 1

def test_on_call_notification_trigger_disabled(
    client,
    mock_gcs_config_service,
    mock_slack_service
):
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=False,
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=False, # Disabled
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(roster=[])
        )
        mock_get_app_config.return_value = mock_app_config

        response = client.post("/schedule/on-call-notification")

        assert response.status_code == 202
        assert response.json() == {"message": "On-call notification is disabled."}

        # Assert no service methods were called
        mock_gcs_config_service.save_config.assert_not_called()

def test_on_call_notification_trigger_failure(
    client,
    mock_gcs_config_service,
    mock_slack_service
):
    with patch('backend.src.services.config_service.get_app_config') as mock_get_app_config:
        mock_app_config = AppConfig(
            confluence_config=ConfluenceConfig(
                enabled=False,
                schedule="0 10 * * 1",
                confluence_url="https://test.confluence.com",
                slack_channel="C12345"
            ),
            on_call_config=OnCallConfig(
                enabled=True,
                schedule="0 18 * * 5",
                slack_channel="C67890"
            ),
            on_call_schedule=OnCallSchedule(
                current_index=0,
                roster=[
                    OnCallPerson(name="Alice", slack_user_id="U01A")
                ]
            )
        )
        mock_get_app_config.return_value = mock_app_config

        # Mock a failure in the OnCallService
        with patch('backend.src.services.oncall_service.OnCallService.notify_on_call_person') as mock_notify:
            mock_notify.side_effect = Exception("Slack API Error")

            response = client.post("/schedule/on-call-notification")

            assert response.status_code == 500
            assert "Slack API Error" in response.json()["detail"]

            mock_notify.assert_called_once()
            # No config should be saved on failure
            mock_gcs_config_service.save_config.assert_not_called()
