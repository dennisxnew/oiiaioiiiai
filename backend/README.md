# Development Team Automation Tool Backend

This is the FastAPI backend for the Development Team Automation Tool. It provides APIs for:

- Triggering scheduled jobs (Confluence weekly report generation, Slack on-call notifications)
- Managing application configuration, including on-call rosters, via a web administration interface.

## Features

- **Confluence Weekly Report Automation**: Automatically clones a Confluence template page, updates its title with the current week's details, and notifies a Slack channel.
- **Slack On-Call Notification**: Notifies the current on-call person in a designated Slack channel, including an @-mention and updates the channel topic with the on-call person's name.
- **Config Management API**: Provides RESTful endpoints for the frontend to retrieve and update the application's configuration, which is stored in Google Cloud Storage.

## Technology Stack

- Python 3.11+
- FastAPI
- Uvicorn (ASGI server)
- Google Cloud Storage client library
- Slack SDK for Python
- `requests` (for Confluence API interaction)

## Setup and Local Development

### Prerequisites

- Python 3.11+
- Google Cloud SDK (`gcloud`) authenticated to your GCP project.
- A GCS bucket created for storing `config.json`.
- Environment variables configured (see `.env` file below).

### Installation

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # (assuming requirements.txt will be generated)
    # For now:
    pip install fastapi uvicorn google-cloud-storage slack_sdk requests python-crontab
    ```

### Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```
GCS_BUCKET_NAME="your-gcs-bucket-name"
GCS_CONFIG_FILE_PATH="config.json" # Default is config.json
SLACK_API_TOKEN="xoxb-your-slack-bot-token"
CONFLUENCE_API_TOKEN="your-confluence-api-token"
CONFLUENCE_DOMAIN="your-confluence-domain.atlassian.net" # e.g., your-company.atlassian.net
```

**Note**: Ensure your `config.json` file is uploaded to the specified GCS bucket. A default structure can be found in `specs/001-dev-team-schedulers/data-model.md`.

### Running the Application

```bash
uvicorn src.fastapi:app --reload
```

The backend will be running at `http://127.0.0.1:8000`.

## API Endpoints

Refer to `specs/001-dev-team-schedulers/contracts/openapi.yml` for the full OpenAPI specification.

### Scheduled Job Endpoints (Triggered by Cloud Scheduler)

-   `POST /schedule/confluence-weekly-report`: Triggers the Confluence report generation.
-   `POST /schedule/on-call-notification`: Triggers the Slack on-call notification.

### Admin API Endpoints (Used by Frontend)

-   `GET /api/config`: Retrieves the current application configuration.
-   `PUT /api/config`: Updates the application configuration.

## Testing

Unit and contract tests are located in the `backend/tests/` directory.

To run tests:

```bash
cd backend
source .venv/bin/activate
pytest
```
