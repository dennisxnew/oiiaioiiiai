from ..models.config import OnCallConfig, OnCallPerson, OnCallSchedule
from .slack_service import SlackService


class OnCallService:
    def __init__(self):
        self.slack_service = SlackService()

    def notify_on_call_person(
        self,
        on_call_config: OnCallConfig,
        on_call_schedule: OnCallSchedule
    ) -> tuple[OnCallPerson, OnCallSchedule]:
        """
        Determines the current on-call person, sends a Slack notification,
        updates the channel description, and advances the rotation.
        """
        if not on_call_schedule.roster:
            raise ValueError("On-call roster is empty. Cannot notify anyone.")

        current_index = on_call_schedule.current_index
        if current_index >= len(on_call_schedule.roster):
            current_index = 0 # Reset if index is out of bounds

        on_call_person = on_call_schedule.roster[current_index]

        # Send Slack notification
        message = f":uia_cat: 本週值班人員: <@{on_call_person.slack_user_id}>"
        self.slack_service.send_message(
            channel=on_call_config.slack_channel,
            message=message
        )

        # Update Slack channel description
        description = f":uia_cat: 本週值班人員: <@{on_call_person.slack_user_id}>"
        self.slack_service.update_channel_description(
            channel=on_call_config.slack_channel,
            description=description
        )

        # Advance rotation for next week
        next_index = (current_index + 1) % len(on_call_schedule.roster)
        on_call_schedule.current_index = next_index

        return on_call_person, on_call_schedule
