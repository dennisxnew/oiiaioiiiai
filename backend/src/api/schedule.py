from ..services.config_service import get_app_config, save_app_config
from ..services.confluence_service import ConfluenceService
from ..services.oncall_service import OnCallService  # Import OnCallService
from ..services.slack_service import SlackService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.post("/schedule/confluence-weekly-report")
async def trigger_confluence_weekly_report():
    """Triggers the copying of a Confluence page for the next week."""
    app_config = get_app_config()
    confluence_config = app_config.confluence_config

    if not confluence_config.weekly_report_enabled:
        return {"message": "Confluence page copying is disabled."}

    confluence_service = ConfluenceService()
    slack_service = SlackService()

    try:
        new_page_url = confluence_service.create_next_weekly_report()
        slack_service.send_message(
            channel=confluence_config.weekly_report_slack_channel,
            message=f"Confluence weekly report for next week created: {new_page_url}",
        )
        return {"message": "Confluence page copy for next week triggered."}
    except Exception as e:
        error_message = f"Error copying Confluence page: {e}"
        print(error_message)
        try:
            slack_service.send_message(
                channel=confluence_config.weekly_report_slack_channel, message=error_message
            )
        except Exception as slack_e:
            print(f"Failed to send error notification to Slack: {slack_e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message
        ) from e


@router.post("/schedule/on-call-notification")
async def trigger_on_call_notification():
    """Triggers the on-call notification."""
    app_config = get_app_config()
    on_call_config = app_config.on_call_config
    on_call_schedule = app_config.on_call_schedule

    if not on_call_config.enabled:
        return {"message": "On-call notification is disabled."}

    on_call_service = OnCallService()

    try:
        on_call_person, updated_schedule = on_call_service.notify_on_call_person(
            on_call_config, on_call_schedule
        )
        # Update the app_config with the new schedule and save it
        app_config.on_call_schedule = updated_schedule
        save_app_config(app_config)

        return {
            "message": f"On-call notification triggered for {on_call_person.name} ({on_call_person.slack_user_id})."
        }
    except Exception as e:
        error_message = f"Error sending on-call notification: {e}"
        print(error_message)
        # Attempt to send error notification to Slack (using the general slack_service if available)
        try:
            # Re-initialize SlackService if not already done, or pass it around
            slack_service = SlackService()
            slack_service.send_message(
                channel=on_call_config.slack_channel,  # Send to the configured on-call channel
                message=error_message,
            )
        except Exception as slack_e:
            print(f"Failed to send error notification to Slack: {slack_e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message
        ) from e
