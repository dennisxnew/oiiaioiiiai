import React, { useState, useEffect } from 'react';
import { AppConfig } from '../services/api';

interface OnCallFormProps {
  config: AppConfig;
  onSave: (config: AppConfig) => void;
}

export const OnCallForm: React.FC<OnCallFormProps> = ({ config, onSave }) => {
  const [onCallConfig, setOnCallConfig] = useState(config.on_call_config);

  useEffect(() => {
    setOnCallConfig(config.on_call_config);
  }, [config.on_call_config]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setOnCallConfig(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({ ...config, on_call_config: onCallConfig });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="onCallEnabled">
          <input
            type="checkbox"
            id="onCallEnabled"
            name="enabled"
            checked={onCallConfig.enabled}
            onChange={handleChange}
          />
          On-Call Enabled
        </label>
      </div>
      <div>
        <label htmlFor="onCallSchedule">Schedule (Cron):</label>
        <input
          type="text"
          id="onCallSchedule"
          name="schedule"
          value={onCallConfig.schedule}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="onCallSlackChannel">On-Call Slack Channel ID:</label>
        <input
          type="text"
          id="onCallSlackChannel"
          name="slack_channel"
          value={onCallConfig.slack_channel}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Save On-Call Settings</button>
    </form>
  );
};

export default OnCallForm;
