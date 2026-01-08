import { render, screen } from '@testing-library/react';
import { OnCallForm } from './OnCallForm'; // Assuming it's a named export
import { AppConfig } from '../services/api';

describe('OnCallForm', () => {
  const mockConfig: AppConfig = {
    confluence_config: {
      enabled: false,
      schedule: '0 10 * * 1',
      confluence_url: 'https://test.confluence.com',
      slack_channel: 'C12345',
    },
    on_call_config: {
      enabled: true,
      schedule: '0 18 * * 5',
      slack_channel: 'C67890',
    },
    on_call_schedule: {
      current_index: 0,
      roster: [],
    },
  };

  it('renders correctly with provided config', () => {
    render(<OnCallForm config={mockConfig} />);

    expect(screen.getByLabelText(/On-Call Enabled/i)).toBeChecked();
    expect(screen.getByLabelText(/On-Call Slack Channel ID/i)).toHaveValue('C67890');
    expect(screen.getByLabelText(/Schedule/i)).toHaveValue('0 18 * * 5');
  });

  // Add more tests for interaction, validation, etc. when the form logic is implemented
});
