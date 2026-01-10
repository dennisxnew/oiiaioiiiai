import datetime
import re

from .config_service import get_app_config
from .confluence_client import ConfluenceClient
from .slack_service import SlackService


class ConfluenceService:
    """Service for interacting with Confluence."""

    def __init__(self):
        self.confluence_client = ConfluenceClient()

    def create_next_weekly_report(self) -> str:
        """
        Orchestrates the creation of the next weekly report.
        1. Finds the root folder for the current year.
        2. Finds the latest weekly report under that root.
        3. Calculates the date for the next week's report.
        4. Handles year change by creating a new root folder if necessary.
        5. Copies the latest report to the correct root folder.
        6. Updates the title of the new report.
        """
        today = datetime.date.today()
        root_page, _ = self._find_or_create_root_page(today.year)
        if not root_page:
            raise Exception(f"Could not find or create root folder for year {today.year}")

        latest_report = self._find_latest_weekly_report(root_page["id"])
        if not latest_report:
            raise Exception(f"No weekly reports found under root page {root_page['title']}")

        new_title, next_monday = self._generate_next_week_title(latest_report["title"])

        # Handle year change
        destination_parent_id = root_page["id"]
        if next_monday.year != today.year:
            new_root_page, _ = self._find_or_create_root_page(next_monday.year)
            if not new_root_page:
                raise Exception(
                    f"Could not create root folder for new year {next_monday.year}"
                )
            destination_parent_id = new_root_page["id"]

        # Copy the page
        copied_page = self.confluence_client.copy_page(
            page_id=latest_report["id"],
            destination={
                "destination": {  # Corrected payload structure
                    "type": "parent_page",
                    "value": destination_parent_id,
                }
            },
        )

        # Update the title of the copied page
        updated_page = self.confluence_client.update_page(
            page_id=copied_page["id"],
            title=new_title,
            version=copied_page["version"]["number"] + 1,
        )

        new_weekly_report_url = f"https://{self.confluence_client.domain}{updated_page['_links']['webui']}"
        return new_weekly_report_url

    def _find_or_create_root_page(self, year: int) -> tuple[dict, bool]:
        """Finds the root page for a given year, or creates it if it doesn't exist."""
        title = f"團隊週會 {year}"
        page = self.confluence_client.get_page_by_title(title)
        if page:
            return page, True

        # If not found, create it.
        # This assumes we are creating it at the space root. A parent can be specified if needed.
        new_page = self.confluence_client.create_page(
            space_key=self.confluence_client.space_key,
            parent_id=None,  # Or a configured parent ID for all yearly folders
            title=title,
            content=f"{year} weekly reports.",
        )
        return new_page, False

    def _find_latest_weekly_report(self, parent_page_id: str) -> dict | None:
        """Finds the latest weekly report under a given parent page."""
        child_pages = self.confluence_client.get_child_pages(parent_page_id)
        if not child_pages:
            return None

        latest_report = None
        latest_date = datetime.date.min

        for page in child_pages:
            end_date = self._get_date_from_title(page["title"])
            if end_date and end_date > latest_date:
                latest_date = end_date
                latest_report = page

        return latest_report

    def _get_date_from_title(self, title: str) -> datetime.date | None:
        """Extracts the end date from a report title."""
        match = re.search(r"\((\d{4})-(\d{4})\)", title)
        if not match:
            return None

        start_str, end_str = match.groups()
        # We only care about the end date for sorting
        end_month, end_day = int(end_str[:2]), int(end_str[2:])

        # This is tricky because we don't know the year of the end date.
        # We can infer it from the title, assuming format "YYYY W## ..."
        year_match = re.search(r"^(\d{4})", title)
        if not year_match:
            return None
        year = int(year_match.group(1))

        # Handle year-end case where end_month is 1 and start_month is 12
        if end_month == 1 and int(start_str[:2]) == 12:
            year += 1

        return datetime.date(year, end_month, end_day)

    def _generate_next_week_title(self, latest_title: str) -> tuple[str, datetime.date]:
        """Generates the title for the next week's report."""
        end_date = self._get_date_from_title(latest_title)
        if not end_date:
            raise ValueError("Could not parse date from latest report title.")

        next_monday = end_date + datetime.timedelta(days=1)
        # Find the next Monday
        while next_monday.weekday() != 0:
            next_monday += datetime.timedelta(days=1)

        next_friday = next_monday + datetime.timedelta(days=4)
        
        # Keep the original title structure, but replace the date part.
        # Example: "2025 W1 技術部 RD4 團隊週報 (1229-0102)"
        title_prefix = re.sub(r"\((\d{4})-(\d{4})\)", "", latest_title).strip()
        
        # Generate new year and week number for the title
        year = next_monday.year
        week_num = next_monday.isocalendar()[1]
        
        # Reconstruct prefix with new year and week number
        # Assuming format "YYYY W## TEAM_NAME REPORT_TYPE"
        parts = title_prefix.split(" ")
        if len(parts) >= 4:
            team_and_report = " ".join(parts[2:])
            new_prefix = f"{year} W{week_num:02d} {team_and_report}"
        else:
            new_prefix = title_prefix # Fallback

        start_str = next_monday.strftime("%m%d")
        end_str = next_friday.strftime("%m%d")
        
        new_title = f"{new_prefix} ({start_str}-{end_str})"
        
        return new_title, next_monday


def run_weekly_report_job():
    """
    Core logic to execute the Confluence weekly report generation.
    This can be called by a scheduler or an HTTP request.
    """
    app_config = get_app_config()
    confluence_config = app_config.confluence_config

    if not confluence_config.weekly_report_enabled:
        message = "Confluence page copying is disabled."
        print(message)
        return {"message": message}

    confluence_service = ConfluenceService()
    slack_service = SlackService()

    try:
        new_weekly_report_url = confluence_service.create_next_weekly_report()
        message = f":uia_cat: Hi <!subteam^S03GP72G62J> 本週週報已長出來: <{new_weekly_report_url}|New Weekly Report> ，請記得週五前完成！"
        slack_service.send_message(
            channel=confluence_config.weekly_report_slack_channel,
            message=message,
        )
        print(message)  # Log to console for scheduler visibility
        return {"message": "Confluence page copy for next week triggered."}
    except Exception as e:
        error_message = f"Error running Confluence job: {e}"
        print(error_message)
        raise e