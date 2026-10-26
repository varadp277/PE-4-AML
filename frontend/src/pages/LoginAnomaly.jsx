import React, { useState } from 'react';
import {
  UserCheck,
  ShieldAlert,
  Clock,
  MapPin,
  Laptop,
  AlertOctagon,
  CheckCircle2,
  Play,
  RotateCcw,
  Sparkles,
  Info
} from 'lucide-react';
import api from '../services/api';

const PRESET_SCENARIOS = [
  {
    label: 'Normal Business Access',
    type: 'Normal',
    data: {
      username: 'alice.security',
      role: 'SecOps',
      timestamp: '2026-10-25T14:15:00',
      login_city: 'New York',
      login_country: 'USA',
      ip_address: '192.168.1.45',
      device: 'MacBook-Corporate',
      failed_attempts: 0
    },
    desc: 'Expected daytime authentication from corporate office workstation'
  },
  {
    label: 'Impossible Travel Jump',
    type: 'Anomaly',
    data: {
      username: 'alice.security',
      role: 'SecOps',
      timestamp: '2026-10-25T15:00:00',
      login_city: 'Pyongyang',
      login_country: 'North Korea',
      ip_address: '89.23.45.10',
      device: 'Tor-Browser-Exit-Node',
      failed_attempts: 1
    },
    desc: 'Immediate relocation across continents through anonymous Tor relay'
  },
  {
    label: 'Late-Night Off-Hours Access',
    type: 'Anomaly',
    data: {
      username: 'charlie.finance',
      role: 'Finance',
      timestamp: '2026-10-25T03:22:00',
      login_city: 'London',
      login_country: 'UK',
      ip_address: '192.168.2.88',
      device: 'Windows-Corporate',
      failed_attempts: 1
    },
    desc: 'Sensitive financial systems access requested at 3:22 AM'
  },
  {
    label: 'Brute-Force Velocity Burst',
    type: 'Anomaly',
    data: {
      username: 'bob.developer',
      role: 'Dev',
      timestamp: '2026-10-25T21:40:00',
      login_city: 'San Francisco',
      login_country: 'USA',
      ip_address: '185.120.45.67',
      device: 'Python-Requests/2.28',
      failed_attempts: 7
    },
    desc: 'High-frequency credential stuffing attempt with 7 consecutive failures'
  }
];

const SYNTHETIC_LOG_STREAM = [
  {
    session_id: 'SESS-ANOM-200001',
    user: 'alice.security',
    time: '2026-10-25 03:15 UTC',
    location: 'Pyongyang, North Korea',
    device: 'Tor-Browser-Exit-Node',
    failures: 4,
    anomaly_type: 'Geographic & Temporal Outlier',
    score: 96.2,
    synthetic_tag: '[SYNTHETIC_DATASET_V1]'
  },
  {
    session_id: 'SESS-ANOM-200002',
    user: 'bob.developer',
    time: '2026-10-25 02:45 UTC',
    location: 'Moscow, Russia',
    device: 'Python-Requests/2.28',
    failures: 8,
    anomaly_type: 'Brute Force Credential Velocity',
    score: 94.0,
    synthetic_tag: '[SYNTHETIC_DATASET_V1]'
  },
  {
    session_id: 'SESS-ANOM-200003',
    user: 'charlie.finance',
    time: '2026-10-25 01:20 UTC',
    location: 'Tehran, Iran',
    device: 'Android-Emulator-Rooted',
    failures: 3,
    anomaly_type: 'Untrusted Device Fingerprint',
    score: 88.5,
    synthetic_tag: '[SYNTHETIC_DATASET_V1]'
  },
  {
    session_id: 'SESS-ANOM-200004',
    user: 'elena.admin',
    time: '2026-10-25 04:10 UTC',
    location: 'Berlin, Germany',
    device: 'Linux-Workstation',
    failures: 5,
    anomaly_type: 'Off-Hours Admin Burst',
    score: 82.0,
    synthetic_tag: '[SYNTHETIC_DATASET_V1]'
  }
];

export default function LoginAnomaly() {
  const [formData, setFormData] = useState({
    username: 'alice.security',
    role: 'SecOps',
    timestamp: new Date().toISOString().slice(0, 16),
    login_city: 'Pyongyang',
    login_country: 'North Korea',
    ip_address: '89.23.45.10',
    device: 'Tor-Browser-Exit-Node',
    failed_attempts: 4
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleTestLogin = async (overrideData = null) => {
    const payload = overrideData || formData;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.scanLogin(payload);
      setResult(response);
    } catch (err) {
      console.error('UEBA scan failed:', err);
      setError(err.response?.data?.detail || 'Failed to analyze login event.');
    } finally {
      setLoading(false);
    }
  };

  const applyScenario = (scenario) => {
    setFormData(scenario.data);
    handleTestLogin(scenario.data);
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono font-semibold mb-3">
          <UserCheck className="w-3.5 h-3.5" />
          MODULE 3 // UEBA ISOLATION FOREST ENGINE
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Login Anomaly & Behavioral Analytics (UEBA)
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Detects credential compromise, off-hours access bursts, and impossible travel patterns using an Isolation Forest trained on baseline user behavior.
        </p>
      </div>

      {/* Synthetic Data Banner */}
      <div className="p-4 rounded-xl bg-cyber-darker border border-amber-500/30 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2.5 text-amber-300">
          <Info className="w-4 h-4 flex-shrink-0" />
          <span>
            <strong className="font-mono text-amber-400 font-bold">[SYNTHETIC_DATASET_V1]</strong> All login profiles and authentication logs in this module are generated with a deterministic seeded random generator for educational defense.
          </span>
        </div>
        <span className="hidden sm:inline-block font-mono text-[10px] text-slate-400 px-2 py-0.5 rounded bg-cyber-card border border-cyber-border">
          SEED: 42 // 1,950 Records
        </span>
      </div>

      {/* Quick Scenarios */}
      <div>
        <span className="text-xs font-mono text-slate-400 block mb-2 uppercase tracking-wider">
          Simulate Preset Scenarios:
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {PRESET_SCENARIOS.map((sc, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => applyScenario(sc)}
              className="p-3 rounded-xl bg-cyber-card hover:bg-cyber-cardHover border border-cyber-border hover:border-amber-500/50 text-left transition-all group flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-semibold text-xs text-slate-200 group-hover:text-amber-400 transition-colors">
                    {sc.label}
                  </span>
                  <span className={`px-1.5 py-0.5 rounded text-[9px] font-mono font-bold ${
                    sc.type === 'Normal' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                  }`}>
                    {sc.type}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-tight">{sc.desc}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-cyber-border/60 flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>{sc.data.login_city}</span>
                <span className="text-amber-400">Simulate &rarr;</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Interactive Form & Result */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Panel */}
        <div className="lg:col-span-7 glass-panel p-6 rounded-2xl border border-cyber-border space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-2">
            Interactive Authentication Simulator
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1">Role / Department</label>
              <input
                type="text"
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1">City</label>
              <input
                type="text"
                value={formData.login_city}
                onChange={(e) => setFormData({ ...formData, login_city: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1">Country</label>
              <input
                type="text"
                value={formData.login_country}
                onChange={(e) => setFormData({ ...formData, login_country: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1">IP Address</label>
              <input
                type="text"
                value={formData.ip_address}
                onChange={(e) => setFormData({ ...formData, ip_address: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1">Failed Attempts Count</label>
              <input
                type="number"
                min="0"
                max="20"
                value={formData.failed_attempts}
                onChange={(e) => setFormData({ ...formData, failed_attempts: parseInt(e.target.value) || 0 })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-slate-400 mb-1">Device Fingerprint</label>
              <input
                type="text"
                value={formData.device}
                onChange={(e) => setFormData({ ...formData, device: e.target.value })}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-white font-mono focus:border-amber-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            onClick={() => handleTestLogin()}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2 mt-4 shadow-lg disabled:opacity-50"
          >
            {loading ? 'Evaluating Manifold...' : 'Run UEBA Evaluation'}
          </button>
        </div>

        {/* Evaluation Output Panel */}
        <div className="lg:col-span-5 glass-panel p-6 rounded-2xl border border-cyber-border flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-3">
              Behavioral Evaluation Result
            </h3>

            {error && (
              <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">
                {error}
              </div>
            )}

            {result ? (
              <div className="space-y-4 animate-in fade-in duration-200">
                <div className={`p-4 rounded-xl border ${
                  result.is_anomaly
                    ? 'bg-rose-500/10 border-rose-500/40 text-rose-400'
                    : 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400'
                }`}>
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold uppercase">{result.verdict}</span>
                    <span className="text-xl font-bold font-mono">{result.risk_score}% Risk</span>
                  </div>
                  <div className="text-xs font-mono text-slate-300 mt-2">
                    Session: <strong className="text-white">{result.session_id}</strong>
                  </div>
                  <div className="text-xs font-mono text-slate-300">
                    Anomaly Score: <span className="text-cyber-cyan">{result.anomaly_score}</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block">
                    Forensic Behavioral Factors:
                  </span>
                  <div className="space-y-1.5">
                    {result.reasons?.map((reason, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-cyber-darker border border-cyber-border text-xs text-slate-300 flex items-start gap-2">
                        <AlertOctagon className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
                        <span>{reason}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-xs text-slate-500 space-y-2">
                <UserCheck className="w-8 h-8 mx-auto text-slate-600" />
                <p>Click "Run UEBA Evaluation" or choose a preset scenario to evaluate user anomaly risk.</p>
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-cyber-border/60 text-[10px] font-mono text-slate-500">
            Engine: Scikit-Learn IsolationForest (contamination=0.08)
          </div>
        </div>
      </div>

      {/* Flagged Logins from Synthetic Dataset Log */}
      <div className="glass-panel p-6 rounded-2xl border border-cyber-border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-white">Flagged Logins from Synthetic Dataset Log</h3>
            <p className="text-xs text-slate-400">Pre-computed anomaly cluster from seeded baseline data</p>
          </div>
          <span className="text-[10px] font-mono px-2 py-1 rounded bg-amber-500/10 border border-amber-500/20 text-amber-400">
            TAGGED [SYNTHETIC]
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-cyber-darker text-slate-400 uppercase font-mono text-[11px] border-b border-cyber-border">
              <tr>
                <th className="py-2.5 px-3">Session ID</th>
                <th className="py-2.5 px-3">User & Time</th>
                <th className="py-2.5 px-3">Geo-Location</th>
                <th className="py-2.5 px-3">Device / Client</th>
                <th className="py-2.5 px-3">Anomaly Type</th>
                <th className="py-2.5 px-3">Risk Score</th>
                <th className="py-2.5 px-3 text-right">Synthetic Label</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-border/60 text-slate-300">
              {SYNTHETIC_LOG_STREAM.map((item) => (
                <tr key={item.session_id} className="hover:bg-cyber-cardHover/60 transition-colors">
                  <td className="py-2.5 px-3 font-mono text-cyber-teal font-semibold">{item.session_id}</td>
                  <td className="py-2.5 px-3">
                    <div className="font-semibold text-slate-200">{item.user}</div>
                    <div className="text-[10px] font-mono text-slate-500">{item.time}</div>
                  </td>
                  <td className="py-2.5 px-3 font-medium text-slate-300">{item.location}</td>
                  <td className="py-2.5 px-3 font-mono text-slate-400 text-[11px]">{item.device}</td>
                  <td className="py-2.5 px-3 text-rose-400 font-medium">{item.anomaly_type}</td>
                  <td className="py-2.5 px-3 font-mono font-bold text-white">{item.score}%</td>
                  <td className="py-2.5 px-3 text-right">
                    <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-cyber-darker text-amber-400 border border-amber-500/30">
                      {item.synthetic_tag}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
