import { useState, useEffect } from 'react';
import { getAppConfig, updateAppConfig, AppConfig } from '../services/api';
import ConfluenceForm from '../components/ConfluenceForm'; // To be implemented in T027
import OnCallForm from '../components/OnCallForm';       // To be implemented in T028
import OnCallRoster from '../components/OnCallRoster';     // To be implemented in T029

const AdminPage = () => {
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const fetchedConfig = await getAppConfig();
        setConfig(fetchedConfig);
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  const handleSaveConfig = async (updatedConfig: AppConfig) => {
    try {
      setLoading(true);
      const savedConfig = await updateAppConfig(updatedConfig);
      setConfig(savedConfig);
      alert('Configuration saved successfully!');
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      alert('Failed to save configuration.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading configuration...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!config) {
    return <div>No configuration data available.</div>;
  }

  return (
    <div className="admin-page">
      <h1>Admin Panel</h1>
      <p>Manage your automation tool configurations here.</p>

      <section>
        <h2>Confluence Scheduler Settings</h2>
        <ConfluenceForm config={config} onSave={handleSaveConfig} />
      </section>

      <section>
        <h2>On-Call Scheduler Settings</h2>
        <OnCallForm config={config} onSave={handleSaveConfig} />
      </section>

      <section>
        <h2>On-Call Roster Management</h2>
        <OnCallRoster config={config} onSave={handleSaveConfig} />
      </section>
    </div>
  );
};

export default AdminPage;