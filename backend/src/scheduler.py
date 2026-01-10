from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .services.config_service import get_app_config
from .services.confluence_service import run_weekly_report_job
from .services.oncall_service import run_oncall_notification_job

# Initialize scheduler
scheduler = AsyncIOScheduler()


def init_scheduler():
    """
    Initializes and configures the scheduler with jobs from the application config.
    """
    print("Initializing scheduler...")
    app_config = get_app_config()

    # Add Confluence job to the scheduler if it is enabled
    if app_config.confluence_config.enabled:
        try:
            cron_args = {
                key: val
                for key, val in zip(
                    ["minute", "hour", "day", "month", "day_of_week"],
                    app_config.confluence_config.schedule.split(),
                )
            }
            scheduler.add_job(
                run_weekly_report_job,
                "cron",
                **cron_args,
                id="confluence_weekly_report",
                replace_existing=True,
            )
            print(
                f"Confluence job scheduled with cron: {app_config.confluence_config.schedule}"
            )
        except Exception as e:
            print(f"Error scheduling Confluence job: {e}")

    # Add On-call job to the scheduler if it is enabled
    if app_config.on_call_config.enabled:
        try:
            cron_args = {
                key: val
                for key, val in zip(
                    ["minute", "hour", "day", "month", "day_of_week"],
                    app_config.on_call_config.schedule.split(),
                )
            }
            scheduler.add_job(
                run_oncall_notification_job,
                "cron",
                **cron_args,
                id="on_call_notification",
                replace_existing=True,
            )
            print(
                f"On-call job scheduled with cron: {app_config.on_call_config.schedule}"
            )
        except Exception as e:
            print(f"Error scheduling On-call job: {e}")

    # Start the scheduler if there are jobs
    if scheduler.get_jobs():
        scheduler.start()
        print("Scheduler started with running jobs.")
    else:
        print("No jobs were scheduled.")
