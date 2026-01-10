from ..models.config import OnCallConfig, OnCallPerson, OnCallSchedule
from .config_service import get_app_config, save_app_config
from .slack_service import SlackService


class OnCallService:
    def __init__(self):
        self.slack_service = SlackService()

    def notify_on_call_person(
        self,
        on_call_config: OnCallConfig,
        on_call_schedule: OnCallSchedule,
    ) -> tuple[OnCallPerson, OnCallSchedule]:
        """
        Determines the current on-call person, sends a Slack notification,
        updates the channel topic, and advances the rotation.
        """
        if not on_call_schedule.roster:
            raise ValueError("On-call roster is empty. Cannot notify anyone.")

        current_index = on_call_schedule.current_index
        if current_index >= len(on_call_schedule.roster):
            current_index = 0  # Reset if index is out of bounds

        on_call_person = on_call_schedule.roster[current_index]

        # Update Slack channel topic (description)
        topic = f":uia_cat: 本週值班人員: {on_call_person.name}"
        self.slack_service.update_channel_description(
            channel=on_call_config.slack_channel, description=topic
        )

        # Advance rotation for next week
        next_index = (current_index + 1) % len(on_call_schedule.roster)
        on_call_schedule.current_index = next_index

        return on_call_person, on_call_schedule


def run_oncall_notification_job():
    """
    Core logic to execute the on-call notification.
    This can be called by a scheduler or an HTTP request.
    """
    app_config = get_app_config()
    on_call_config = app_config.on_call_config

    if not on_call_config.enabled:
        message = "On-call notification is disabled."
        print(message)
        return {"message": message}

    on_call_service = OnCallService()

    try:
        on_call_person, updated_schedule = on_call_service.notify_on_call_person(
            on_call_config, app_config.on_call_schedule
        )
        # Update the app_config with the new schedule and save it
        app_config.on_call_schedule = updated_schedule
        save_app_config(app_config)

        message = f"On-call notification triggered for {on_call_person.name} ({on_call_person.slack_user_id})."
        print(message)
        return {"message": message}
    except Exception as e:
        error_message = f"Error sending on-call notification: {e}"
        print(error_message)
        raise e