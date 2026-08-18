import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="header-bar">
      <div className="logo-container">
        <span className="logo-icon">📸⚡</span>
        <h1>FactuSnap <span className="badge">AI</span></h1>
      </div>
      <p className="subtitle">MVP Seguro & Clean Architecture (FastAPI + Supabase)</p>
    </header>
  );
};
