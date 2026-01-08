import { render, screen } from '@testing-library/react';
import { OnCallRoster } from './OnCallRoster'; // Assuming it's a named export
import { AppConfig } from '../services/api';

describe('OnCallRoster', () => {
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
      roster: [
        { name: 'Alice', slack_user_id: 'U111' },
        { name: 'Bob', slack_user_id: 'U222' },
      ],
    },
  };

  it('renders correctly with provided roster', () => {
    render(<OnCallRoster config={mockConfig} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('U111')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('U222')).toBeInTheDocument();
  });

  // Add more tests for adding, removing, reordering, etc. when the logic is implemented
});
