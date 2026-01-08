# Data Model: Development Team Automation Tool

This document defines the key data entities for the project, as stored in the `config.json` file in a GCS bucket.

## Main Configuration Object (`config.json`)

The root object of the `config.json` file will have the following structure:

```json
{
  "confluence_config": {
    "enabled": true,
    "schedule": "0 10 * * 1",
    "confluence_url": "https://your-domain.atlassian.net/wiki/spaces/SPACE/pages/PAGE_ID",
    "slack_channel": "C12345678"
  },
  "on_call_config": {
    "enabled": true,
    "schedule": "0 18 * * 5",
    "slack_channel": "C87654321"
  },
  "on_call_schedule": {
    "current_index": 0,
    "roster": [
      {
        "name": "User One",
        "slack_user_id": "U12345"
      },
      {
        "name": "User Two",
        "slack_user_id": "U67890"
      }
    ]
  }
}
```

## Entity Definitions

### `ConfluenceConfig` (Object)
Contains all settings related to the Confluence weekly report scheduler.

| Field | Type | Description | Validation |
|---|---|---|---|
| `enabled` | boolean | If `true`, the job is active. | Must be a boolean. |
| `schedule`| string | Cron string for the schedule (UTC). | Must be a valid cron expression. |
| `confluence_url` | string | The URL of the Confluence page to clone. | Must be a valid URL. |
| `slack_channel` | string | The Slack Channel ID for notifications. | Must not be empty. |

### `OnCallConfig` (Object)
Contains all settings related to the on-call notification scheduler.

| Field | Type | Description | Validation |
|---|---|---|---|
| `enabled` | boolean | If `true`, the job is active. | Must be a boolean. |
| `schedule`| string | Cron string for the schedule (UTC). | Must be a valid cron expression. |
| `slack_channel` | string | The Slack Channel ID for notifications. | Must not be empty. |

### `OnCallSchedule` (Object)
Defines the on-call rotation.

| Field | Type | Description | Validation |
|---|---|---|---|
| `current_index` | integer | The index of the current on-call person in the `roster` array. | Must be a valid index for the roster array. |
| `roster` | Array[`OnCallPerson`] | An ordered list of team members in the rotation. | Must be an array. Can be empty. |

### `OnCallPerson` (Object)
Represents a single person in the on-call roster.

| Field | Type | Description | Validation |
|---|---|---|---|
| `name` | string | The person's full name. | Must not be empty. |
| `slack_user_id` | string | The person's Slack User ID for @-mentions. | Must not be empty. |
