import React, { useState, useEffect } from 'react';
import { AppConfig, OnCallPerson } from '../services/api';

interface OnCallRosterProps {
  config: AppConfig;
  onSave: (config: AppConfig) => void;
}

export const OnCallRoster: React.FC<OnCallRosterProps> = ({ config, onSave }) => {
  const [roster, setRoster] = useState<OnCallPerson[]>(config.on_call_schedule.roster);
  const [newPersonName, setNewPersonName] = useState('');
  const [newPersonSlackId, setNewPersonSlackId] = useState('');

  useEffect(() => {
    setRoster(config.on_call_schedule.roster);
  }, [config.on_call_schedule.roster]);

  const handleAddPerson = () => {
    if (newPersonName && newPersonSlackId) {
      const updatedRoster = [...roster, { name: newPersonName, slack_user_id: newPersonSlackId }];
      setRoster(updatedRoster);
      setNewPersonName('');
      setNewPersonSlackId('');
      onSave({ ...config, on_call_schedule: { ...config.on_call_schedule, roster: updatedRoster } });
    }
  };

  const handleRemovePerson = (index: number) => {
    const updatedRoster = roster.filter((_, i) => i !== index);
    setRoster(updatedRoster);
    onSave({ ...config, on_call_schedule: { ...config.on_call_schedule, roster: updatedRoster } });
  };

  // Basic reordering (drag and drop would be better for UX, but this is for MVP)
  const handleMovePerson = (index: number, direction: 'up' | 'down') => {
    const updatedRoster = [...roster];
    if (direction === 'up' && index > 0) {
      [updatedRoster[index - 1], updatedRoster[index]] = [updatedRoster[index], updatedRoster[index - 1]];
    } else if (direction === 'down' && index < updatedRoster.length - 1) {
      [updatedRoster[index + 1], updatedRoster[index]] = [updatedRoster[index], updatedRoster[index + 1]];
    }
    setRoster(updatedRoster);
    onSave({ ...config, on_call_schedule: { ...config.on_call_schedule, roster: updatedRoster } });
  };

  return (
    <div>
      <h3>Add New On-Call Person</h3>
      <div>
        <input
          type="text"
          placeholder="Name"
          value={newPersonName}
          onChange={(e) => setNewPersonName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Slack User ID (e.g., U12345)"
          value={newPersonSlackId}
          onChange={(e) => setNewPersonSlackId(e.target.value)}
        />
        <button onClick={handleAddPerson}>Add Person</button>
      </div>

      <h3>Current Roster</h3>
      {roster.length === 0 ? (
        <p>No one in the on-call roster yet.</p>
      ) : (
        <ul>
          {roster.map((person, index) => (
            <li key={index}>
              {person.name} ({person.slack_user_id})
              <button onClick={() => handleMovePerson(index, 'up')} disabled={index === 0}>↑</button>
              <button onClick={() => handleMovePerson(index, 'down')} disabled={index === roster.length - 1}>↓</button>
              <button onClick={() => handleRemovePerson(index)}>Remove</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default OnCallRoster;
