import { render, screen } from '@testing-library/react';
import { ConfluenceForm } from './ConfluenceForm'; // Assuming it's a named export
import { AppConfig } from '../services/api';

describe('ConfluenceForm', () => {
  const mockConfig: AppConfig = {
    confluence_config: {
      enabled: true,
      schedule: '0 10 * * 1',
      confluence_url: 'https://test.confluence.com',
      slack_channel: 'C12345',
    },
    on_call_config: {
      enabled: false,
      schedule: '0 18 * * 5',
      slack_channel: 'C67890',
    },
    on_call_schedule: {
      current_index: 0,
      roster: [],
    },
  };

  it('renders correctly with provided config', () => {
    render(<ConfluenceForm config={mockConfig} />);

    expect(screen.getByLabelText(/Confluence URL/i)).toHaveValue('https://test.confluence.com');
    expect(screen.getByLabelText(/Slack Channel ID/i)).toHaveValue('C12345');
    expect(screen.getByLabelText(/Enabled/i)).toBeChecked();
  });

  // Add more tests for interaction, validation, etc. when the form logic is implemented
});
