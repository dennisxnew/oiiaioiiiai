# Quickstart: Development Team Automation Tool

This guide provides instructions to set up and run the backend and frontend services locally.

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Google Cloud SDK (`gcloud`) authenticated to your GCP project.
- A GCS bucket created.
- A `config.json` file based on `data-model.md` uploaded to the GCS bucket.
- Confluence and Slack API credentials/tokens.

## Backend (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn google-cloud-storage
    # Add other dependencies for Confluence/Slack APIs
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend` directory:
    ```
    GCS_BUCKET_NAME="your-gcs-bucket-name"
    GCS_CONFIG_FILE_PATH="config.json"
    SLACK_API_TOKEN="xoxb-your-token"
    CONFLUENCE_API_TOKEN="your-token"
    ```

5.  **Run the server:**
    ```bash
    uvicorn src.main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

## Frontend (React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Environment Variables:**
    Create a `.env.local` file in the `frontend` directory:
    ```
    VITE_API_BASE_URL="http://127.0.0.1:8000"
    ```

4.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://127.0.0.1:5173` (or another port if 5173 is in use).
