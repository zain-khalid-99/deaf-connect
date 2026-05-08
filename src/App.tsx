/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sidebar } from './components/Sidebar';
import { DashboardPage } from './pages/Dashboard';
import { CommunicationPage } from './pages/Communication';
import { HistoryPage } from './pages/History';
import { ReferencesPage } from './pages/References';
import { DocumentationPage } from './pages/Documentation';
import { SettingsPage } from './pages/Settings';
import { LandingPage } from './pages/Landing';
import { fetchSettings } from './services/dataService';
import { Menu, X } from 'lucide-react';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isMobile, setIsMobile] = useState(typeof window !== 'undefined' ? window.innerWidth < 1024 : false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'light'>('light');

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 1024;
      setIsMobile(mobile);
      if (!mobile) setIsMobileMenuOpen(false);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    document.documentElement.classList.add('light');
    localStorage.setItem('theme', 'light');
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setActivePage('communication');
  };

  const handleNavigate = (page: string) => {
    setActivePage(page);
    if (isMobile) setIsMobileMenuOpen(false);
  };

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard': return <DashboardPage />;
      case 'communication': return <CommunicationPage />;
      case 'history': return <HistoryPage />;
      case 'references': return <ReferencesPage />;
      case 'documentation': return <DocumentationPage />;
      case 'settings': return <SettingsPage />;
      default: return <DashboardPage />;
    }
  };

  if (!isLoaded) {
    return (
      <div className="h-screen w-full flex flex-col items-center justify-center bg-white gap-6">
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-16 h-16 bg-black rounded-lg flex items-center justify-center shadow-2xl"
        >
          <div className="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin" />
        </motion.div>
        <div className="text-center">
          <h1 className="text-xl font-bold tracking-tight uppercase mb-1">SignSync AI</h1>
          <p className="text-[10px] font-medium tracking-[0.2em] text-gray-400 uppercase">Neural Interface Loading</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LandingPage onStart={handleLogin} />;
  }

  return (
    <div className="flex h-screen bg-white text-black overflow-hidden font-sans relative">
      {/* Mobile Header */}
      {isMobile && (
        <div className="fixed top-0 left-0 right-0 h-16 border-b border-gray-100 bg-white/80 backdrop-blur-md z-[60] flex items-center justify-between px-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-black rounded flex items-center justify-center">
              <span className="text-white text-xs font-bold">S</span>
            </div>
            <span className="font-bold text-sm tracking-tight">SignSync AI</span>
          </div>
          <button 
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      )}

      {/* Sidebar Container */}
      <div className={`${
        isMobile 
          ? `fixed inset-0 z-[70] transition-transform duration-300 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`
          : 'relative'
      }`}>
        {isMobile && isMobileMenuOpen && (
          <div 
            className="absolute inset-0 bg-black/20 backdrop-blur-sm"
            onClick={() => setIsMobileMenuOpen(false)}
          />
        )}
        <Sidebar 
          activePage={activePage} 
          onNavigate={handleNavigate} 
          isCollapsed={isCollapsed && !isMobile}
          setIsCollapsed={setIsCollapsed}
          isMobile={isMobile}
        />
      </div>
      
      <main className={`flex-1 relative overflow-y-auto ${isMobile ? 'pt-16' : ''}`}>
        <AnimatePresence mode="wait">
          <motion.div
            key={activePage}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -5 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="relative z-10 h-full"
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}


