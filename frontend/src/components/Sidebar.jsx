import React from 'react';
import {
  Shield,
  LayoutDashboard,
  Globe,
  Radio,
  UserCheck,
  BellRing,
  Cpu,
  BookOpen,
  Terminal,
  Activity
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'home', label: 'Overview', icon: BookOpen, badge: null },
    { id: 'dashboard', label: 'Threat Dashboard', icon: LayoutDashboard, badge: 'Live' },
    { id: 'phishing', label: 'Phishing Scanner', icon: Globe, badge: 'ML' },
    { id: 'network', label: 'Network Intrusion', icon: Radio, badge: 'NSL' },
    { id: 'login', label: 'UEBA Login Anomaly', icon: UserCheck, badge: 'UEBA' },
    { id: 'alerts', label: 'Alerts & Triage', icon: BellRing, badge: null },
    { id: 'models', label: 'Model Registry & Retrain', icon: Cpu, badge: 'Audit' },
  ];

  return (
    <aside className="w-64 bg-cyber-darkest border-r border-cyber-border flex flex-col justify-between h-screen sticky top-0 select-none">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-5 border-b border-cyber-border">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-cyber-teal/20 to-cyber-cyan/20 border border-cyber-teal/40 text-cyber-teal shadow-glow-teal">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <div className="font-extrabold text-base tracking-wide bg-gradient-to-r from-white via-slate-200 to-cyber-teal bg-clip-text text-transparent">
              AEGIS // THREAT
            </div>
            <div className="text-[10px] text-slate-400 font-mono tracking-wider">DEFENSIVE AI PLATFORM</div>
          </div>
        </div>

        {/* Navigation Items */}
        <div className="px-3 py-4 space-y-1">
          <div className="px-3 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Detection Modules
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-cyber-card text-cyber-teal border border-cyber-teal/30 shadow-glow-teal font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-cyber-card/60 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-cyber-teal' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                    isActive
                      ? 'bg-cyber-teal/20 text-cyber-teal'
                      : 'bg-cyber-card text-slate-400'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* System Telemetry Footer */}
      <div className="p-4 border-t border-cyber-border bg-cyber-darker/60">
        <div className="glass-panel p-3 rounded-xl border border-cyber-border space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400 flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-cyber-teal animate-pulse" />
              API Status
            </span>
            <span className="font-mono text-emerald-400 font-semibold text-[11px]">ONLINE</span>
          </div>
          <div className="text-[11px] text-slate-400 font-mono truncate">
            FastAPI + Scikit-Learn 1.9+
          </div>
          <div className="pt-1 border-t border-cyber-border/60 flex items-center justify-between text-[10px] text-slate-400">
            <span>Env: {import.meta.env.DEV ? 'Local Dev' : 'Cloud / Vercel'}</span>
            <span className="text-cyber-cyan font-mono">v1.0.0</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
