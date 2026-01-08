import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import './Layout.css'; // Will create this file

const Layout: React.FC = () => {
  return (
    <div className="layout-container">
      <header className="layout-header">
        <h1>Development Automation Tool</h1>
        <nav className="layout-nav">
          <Link to="/admin">Admin Panel</Link>
          {/* Add other navigation links here */}
        </nav>
      </header>
      <main className="layout-main">
        <Outlet /> {/* Renders the current route's component */}
      </main>
      <footer className="layout-footer">
        <p>&copy; 2026 Development Automation Tool</p>
      </footer>
    </div>
  );
};

export default Layout;
