import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackService:
    def __init__(self):
        self.token = os.getenv("SLACK_API_TOKEN")
        if not self.token:
            raise ValueError("SLACK_API_TOKEN environment variable not set.")
        self.client = WebClient(token=self.token)

    def send_message(self, channel: str, message: str):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message
            )
            return response
        except SlackApiError as e:
            print(f"Error sending Slack message: {e.response['error']}")
            raise # Re-raise to indicate send failure

    def update_channel_description(self, channel: str, description: str):
        try:
            response = self.client.conversations_setTopic(
                channel=channel,
                topic=description
            )
            return response
        except SlackApiError as e:
            print(f"Error updating Slack channel description: {e.response['error']}")
            raise # Re-raise to indicate update failure
