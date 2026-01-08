import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminPage from './pages/AdminPage'; // Will be created in T026
import Layout from './components/Layout'; // Will be created in T013
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<AdminPage />} /> {/* Default route */}
          <Route path="admin" element={<AdminPage />} /> {/* Explicit admin route */}
          {/* Add other routes here as needed */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;