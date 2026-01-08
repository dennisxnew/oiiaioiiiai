from unittest.mock import patch

import pytest
from backend.src.models.config import OnCallConfig, OnCallPerson, OnCallSchedule
from backend.src.services.oncall_service import OnCallService


@pytest.fixture
def mock_slack_service():
    with patch('backend.src.services.slack_service.SlackService') as MockSlackService:
        yield MockSlackService.return_value

@pytest.fixture
def mock_app_config():
    return OnCallConfig(
        enabled=True,
        schedule="0 18 * * 5",
        slack_channel="C12345"
    )

def test_notify_on_call_person_success(mock_slack_service, mock_app_config):
    on_call_schedule = OnCallSchedule(
        current_index=0,
        roster=[
            OnCallPerson(name="Alice", slack_user_id="U01A"),
            OnCallPerson(name="Bob", slack_user_id="U01B")
        ]
    )

    service = OnCallService()
    result_person, result_schedule = service.notify_on_call_person(mock_app_config, on_call_schedule)

    assert result_person.name == "Alice"
    assert result_person.slack_user_id == "U01A"
    assert result_schedule.current_index == 1 # Index should advance
    mock_slack_service.send_message.assert_called_once_with(
        channel=mock_app_config.slack_channel,
        message="今日值班人員: Alice (<@U01A>)"
    )
    mock_slack_service.update_channel_description.assert_called_once_with(
        channel=mock_app_config.slack_channel,
        description="本週值班人員: Alice"
    )

def test_notify_on_call_person_roster_empty(mock_slack_service, mock_app_config):
    on_call_schedule = OnCallSchedule(
        current_index=0,
        roster=[]
    )

    service = OnCallService()
    with pytest.raises(ValueError, match="On-call roster is empty."):
        service.notify_on_call_person(mock_app_config, on_call_schedule)

    mock_slack_service.send_message.assert_not_called()
    mock_slack_service.update_channel_description.assert_not_called()

def test_notify_on_call_person_index_wraps_around(mock_slack_service, mock_app_config):
    on_call_schedule = OnCallSchedule(
        current_index=1,
        roster=[
            OnCallPerson(name="Alice", slack_user_id="U01A"),
            OnCallPerson(name="Bob", slack_user_id="U01B")
        ]
    )

    service = OnCallService()
    result_person, result_schedule = service.notify_on_call_person(mock_app_config, on_call_schedule)

    assert result_person.name == "Bob"
    assert result_person.slack_user_id == "U01B"
    assert result_schedule.current_index == 0 # Should wrap around to 0
