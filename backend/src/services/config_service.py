
from ..models.config import (
    AppConfig,
    ConfluenceConfig,
    OnCallConfig,
    OnCallSchedule,
)
from .gcs_service import get_gcs_config_service

_app_config_instance: AppConfig | None = None

def get_app_config() -> AppConfig:
    global _app_config_instance
    if _app_config_instance is None:
        gcs_service = get_gcs_config_service()
        config_data = gcs_service.load_config()
        try:
            _app_config_instance = AppConfig(**config_data)
        except Exception as e:
            # If config is invalid or empty, provide a default structure
            print(f"Error loading or parsing config: {e}. Initializing with default structure.")
            _app_config_instance = AppConfig(
                confluence_config=ConfluenceConfig(confluence_url="https://example.com", slack_channel=""),
                on_call_config=OnCallConfig(slack_channel=""),
                on_call_schedule=OnCallSchedule(roster=[])
            )
            # Optionally save the default config immediately
            gcs_service.save_config(_app_config_instance.model_dump(mode='json'))
    return _app_config_instance

def save_app_config(config: AppConfig):
    global _app_config_instance
    gcs_service = get_gcs_config_service()
    gcs_service.save_config(config.model_dump(mode='json'))
    _app_config_instance = config # Update the in-memory instance
