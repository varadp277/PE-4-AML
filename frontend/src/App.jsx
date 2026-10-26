import React, { useState } from 'react';
import DisclaimerBanner from './components/DisclaimerBanner';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';

// Pages
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import PhishingScan from './pages/PhishingScan';
import NetworkScan from './pages/NetworkScan';
import LoginAnomaly from './pages/LoginAnomaly';
import Alerts from './pages/Alerts';
import ModelInfo from './pages/ModelInfo';

const TAB_CONFIGS = {
  home: {
    title: 'Platform Overview & Cybersecurity Architecture',
    subtitle: 'Defensive case study for automated threat detection'
  },
  dashboard: {
    title: 'Threat Intelligence Security Operations Center',
    subtitle: 'Live multi-module telemetry and active incident feed'
  },
  phishing: {
    title: 'Phishing URL Analysis & Explainable AI',
    subtitle: 'Lexical, entropy, and structural URL classifier'
  },
  network: {
    title: 'Network Intrusion & Flow Anomaly Detector',
    subtitle: 'NSL-KDD supervised classification & UNSW-NB15 anomaly manifold'
  },
  login: {
    title: 'User & Entity Behavior Analytics (UEBA)',
    subtitle: 'Isolation Forest detection for off-hours and impossible travel'
  },
  alerts: {
    title: 'Security Alerts & Analyst Feedback Triage',
    subtitle: 'Audit trail and human-in-the-loop retraining dataset'
  },
  models: {
    title: 'Model Registry, Datasets & Retrain Studio',
    subtitle: 'Dynamically computed dataset statistics and model metrics'
  }
};

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  const currentTabInfo = TAB_CONFIGS[activeTab] || TAB_CONFIGS.home;

  const renderActivePage = () => {
    switch (activeTab) {
      case 'home':
        return <Home onNavigate={(tab) => setActiveTab(tab)} />;
      case 'dashboard':
        return <Dashboard onNavigate={(tab) => setActiveTab(tab)} />;
      case 'phishing':
        return <PhishingScan />;
      case 'network':
        return <NetworkScan />;
      case 'login':
        return <LoginAnomaly />;
      case 'alerts':
        return <Alerts />;
      case 'models':
        return <ModelInfo />;
      default:
        return <Home onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans">
      {/* Top Disclaimer Banner */}
      <DisclaimerBanner />

      <div className="flex flex-1">
        {/* Sidebar Navigation */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar
            activeTitle={currentTabInfo.title}
            subtitle={currentTabInfo.subtitle}
          />

          <main className="flex-1 p-6 md:p-8 overflow-y-auto radar-grid">
            {renderActivePage()}
          </main>

          {/* Educational Disclaimer Footer */}
          <footer className="py-4 px-8 border-t border-cyber-border text-center text-xs text-slate-500 font-mono">
            AI-Based Threat Intelligence Platform — College Case Study Project // Defensive & Educational Use Only
          </footer>
        </div>
      </div>
    </div>
  );
}
