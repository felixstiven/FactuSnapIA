import React from 'react';
import { FacturaProvider } from './context/FacturaContext';
import { Header } from './components/Header';
import { CameraScanner } from './components/CameraScanner';
import { FacturaList } from './components/FacturaList';
import { ShareBar } from './components/ShareBar';
import './index.css';

export const App: React.FC = () => {
  return (
    <FacturaProvider>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <CameraScanner />
          <FacturaList />
        </main>
        <ShareBar />
      </div>
    </FacturaProvider>
  );
};

export default App;
