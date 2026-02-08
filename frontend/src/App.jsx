import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Leads from './pages/Leads';
import LeadDetail from './pages/LeadDetail';
import Analytics from './pages/Analytics';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import './App.css';

const queryClient = new QueryClient();

function App() {
  const [darkMode, setDarkMode] = useState(true);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>

          
          {/* Landing Page - No Sidebar */}
          <Route path="/" element={
            <div style={{ height: 'auto', overflow: 'visible' }}>
              <Landing />
            </div>
          } />
          
          {/* Dashboard Pages - With Sidebar */}
          <Route path="/dashboard" element={
            <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
              <Sidebar darkMode={darkMode} />
              <div className="flex-1 flex flex-col overflow-hidden bg-gray-50">
                <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
                  <Dashboard />
                </main>
              </div>
            </div>
          } />
          
          <Route path="/leads" element={
            <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
              <Sidebar darkMode={darkMode} />
              <div className="flex-1 flex flex-col overflow-hidden bg-gray-50">
                <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
                  <Leads />
                </main>
              </div>
            </div>
          } />
          
          <Route path="/leads/:id" element={
            <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
              <Sidebar darkMode={darkMode} />
              <div className="flex-1 flex flex-col overflow-hidden bg-gray-50">
                <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
                  <LeadDetail />
                </main>
              </div>
            </div>
          } />
          
          <Route path="/analytics" element={
            <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
              <Sidebar darkMode={darkMode} />
              <div className="flex-1 flex flex-col overflow-hidden bg-gray-50">
                <Header darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
                  <Analytics />
                </main>
              </div>
            </div>
          } />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;