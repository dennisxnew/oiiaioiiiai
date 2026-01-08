import React, { useState, useEffect } from 'react';
import { AppConfig } from '../services/api';

interface ConfluenceFormProps {
  config: AppConfig;
  onSave: (config: AppConfig) => void;
}

export const ConfluenceForm: React.FC<ConfluenceFormProps> = ({ config, onSave }) => {
  const [confluenceConfig, setConfluenceConfig] = useState(config.confluence_config);

  useEffect(() => {
    setConfluenceConfig(config.confluence_config);
  }, [config.confluence_config]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setConfluenceConfig(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({ ...config, confluence_config: confluenceConfig });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="confluenceEnabled">
          <input
            type="checkbox"
            id="confluenceEnabled"
            name="enabled"
            checked={confluenceConfig.enabled}
            onChange={handleChange}
          />
          Enabled
        </label>
      </div>
      <div>
        <label htmlFor="confluenceSchedule">Schedule (Cron):</label>
        <input
          type="text"
          id="confluenceSchedule"
          name="schedule"
          value={confluenceConfig.schedule}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="confluenceUrl">Confluence URL:</label>
        <input
          type="url"
          id="confluenceUrl"
          name="confluence_url"
          value={confluenceConfig.confluence_url}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="confluenceSlackChannel">Slack Channel ID:</label>
        <input
          type="text"
          id="confluenceSlackChannel"
          name="slack_channel"
          value={confluenceConfig.slack_channel}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Save Confluence Settings</button>
    </form>
  );
};

export default ConfluenceForm;
