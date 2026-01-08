import json
import os

from google.cloud import storage


class GCSConfigService:
    def __init__(self, bucket_name: str, config_file_path: str):
        self.bucket_name = bucket_name
        self.config_file_path = config_file_path
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
        self.blob = self.bucket.blob(self.config_file_path)

    def load_config(self) -> dict:
        """Loads the configuration from GCS."""
        try:
            content = self.blob.download_as_text()
            return json.loads(content)
        except Exception as e:
            # Handle cases where the file doesn't exist yet or other GCS errors
            print(f"Error loading config from GCS: {e}")
            return {} # Return empty config for now, will be initialized by Admin UI

    def save_config(self, config: dict):
        """Saves the configuration to GCS."""
        try:
            self.blob.upload_from_string(json.dumps(config, indent=2), content_type="application/json")
        except Exception as e:
            print(f"Error saving config to GCS: {e}")
            raise # Re-raise to indicate save failure

_gcs_config_service = None

def get_gcs_config_service() -> GCSConfigService:
    global _gcs_config_service
    if _gcs_config_service is None:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        config_file_path = os.getenv("GCS_CONFIG_FILE_PATH", "config.json")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME environment variable not set.")
        _gcs_config_service = GCSConfigService(bucket_name, config_file_path)
    return _gcs_config_service
