
from pydantic import BaseModel, Field, HttpUrl


class OnCallPerson(BaseModel):
    """Represents a person on call."""
    name: str
    slack_user_id: str

class OnCallSchedule(BaseModel):
    """Represents the on-call schedule."""
    current_index: int = 0
    roster: list[OnCallPerson] = Field(default_factory=list)

class ConfluenceConfig(BaseModel):
    """Represents the Confluence configuration."""
    enabled: bool = False
    schedule: str = "0 10 * * 1" # Default to Monday 10:00 AM
    confluence_url: HttpUrl
    slack_channel: str
    weekly_report_enabled: bool = False
    weekly_report_slack_channel: str = ""

class OnCallConfig(BaseModel):
    """Represents the on-call configuration."""
    enabled: bool = False
    schedule: str = "0 18 * * 5" # Default to Friday 6:00 PM
    slack_channel: str

class AppConfig(BaseModel):
    """Represents the application configuration."""
    confluence_config: ConfluenceConfig
    on_call_config: OnCallConfig
    on_call_schedule: OnCallSchedule
