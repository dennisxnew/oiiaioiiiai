# Development Team Automation Tool Frontend

This is the React/TypeScript frontend for the Development Team Automation Tool. It provides a web-based administration interface to manage the configuration for the automated backend jobs.

## Features

-   **Confluence Configuration**: Manage settings for the automated Confluence weekly report generation.
-   **On-Call Configuration**: Manage settings for the automated Slack on-call notifications.
-   **On-Call Roster Management**: Add, remove, and reorder on-call personnel and their Slack user IDs.

## Technology Stack

-   React
-   TypeScript
-   Vite (build tool)
-   React Router DOM (for routing)

## Setup and Local Development

### Prerequisites

-   Node.js 18+ and npm
-   The backend service must be running and accessible.

### Installation

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

### Configuration

Create a `.env.local` file in the `frontend/` directory with the following variables:

```
VITE_API_BASE_URL="http://127.0.0.1:8000" # Or the URL where your backend is running
```

### Running the Application

```bash
npm run dev
```

The frontend will be running at `http://localhost:5173` (or another port if 5173 is in use).

## Testing

Component tests are located in `frontend/src/components/*.test.tsx`.

To run tests:

```bash
cd frontend
npm test
```