const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

interface ConfluenceConfig {
  enabled: boolean;
  schedule: string;
  confluence_url: string;
  slack_channel: string;
}

interface OnCallPerson {
  name: string;
  slack_user_id: string;
}

interface OnCallSchedule {
  current_index: number;
  roster: OnCallPerson[];
}

interface OnCallConfig {
  enabled: boolean;
  schedule: string;
  slack_channel: string;
}

export interface AppConfig {
  confluence_config: ConfluenceConfig;
  on_call_config: OnCallConfig;
  on_call_schedule: OnCallSchedule;
}

export const getAppConfig = async (): Promise<AppConfig> => {
  const response = await fetch(`${API_BASE_URL}/api/config`);
  if (!response.ok) {
    throw new Error(`Error fetching config: ${response.statusText}`);
  }
  return response.json();
};

export const updateAppConfig = async (config: AppConfig): Promise<AppConfig> => {
  const response = await fetch(`${API_BASE_URL}/api/config`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(config),
  });
  if (!response.ok) {
    throw new Error(`Error updating config: ${response.statusText}`);
  }
  return response.json();
};
