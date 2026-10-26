import React, { useState } from 'react';
import {
  Radio,
  Upload,
  FileText,
  AlertTriangle,
  CheckCircle,
  Play,
  Filter,
  BarChart2,
  RefreshCw,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  CartesianGrid
} from 'recharts';
import api from '../services/api';

const CAT_COLORS = {
  'Normal Traffic': '#10b981',
  'DoS (Traffic Flooding)': '#ef4444',
  'Probe (Port/Vulnerability Scanning)': '#f59e0b',
  'R2L (Brute Force / Password Attack)': '#8b5cf6',
  'Zero-Day Anomaly (Novel Pattern)': '#0df2c9',
  'Generic Exploits / Malware Traffic': '#ec4899'
};

export default function NetworkScan() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('ALL'); // ALL, ATTACK, NORMAL

  const handleScan = async (uploadedFile = null) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await api.scanNetwork(uploadedFile);
      setData(response);
    } catch (err) {
      console.error('Network scan failed:', err);
      setError(err.response?.data?.detail || 'Failed to inspect network records. Check backend connection.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      handleScan(selected);
    }
  };

  const filteredRows = data?.rows?.filter((r) => {
    if (filter === 'ATTACK') return r.is_attack;
    if (filter === 'NORMAL') return !r.is_attack;
    return true;
  }) || [];

  // Chart data preparation
  const categoryChartData = data?.summary?.attack_categories_breakdown
    ? Object.entries(data.summary.attack_categories_breakdown).map(([name, count]) => ({
        name,
        count
      }))
    : [];

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-cyan/10 border border-cyber-cyan/30 text-cyber-cyan text-xs font-mono font-semibold mb-3">
          <Radio className="w-3.5 h-3.5" />
          MODULE 2 // NSL-KDD & UNSW-NB15 DUAL ENGINES
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Network Intrusion & Zero-Day Anomaly Detector
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Supervised Random Forest attack classification paired with an Unsupervised Isolation Forest for statistical novelty detection.
        </p>
      </div>

      {/* Upload & Demo Trigger Panel */}
      <div className="glass-panel p-6 rounded-2xl border border-cyber-border space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="w-full sm:w-auto">
            <label className="flex items-center justify-center gap-2.5 px-5 py-3 rounded-xl bg-cyber-darker hover:bg-cyber-cardHover border border-dashed border-cyber-border hover:border-cyber-teal cursor-pointer transition-all text-xs font-semibold text-slate-200">
              <Upload className="w-4 h-4 text-cyber-teal" />
              <span>{file ? file.name : 'Upload NetFlow CSV File'}</span>
              <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
            </label>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-400">
            <span>or run instantly without local file:</span>
            <button
              onClick={() => handleScan(null)}
              disabled={loading}
              className="px-4 py-2.5 rounded-xl bg-cyber-teal text-slate-950 font-bold text-xs hover:bg-cyber-teal/90 transition-all flex items-center gap-2 shadow-glow-teal disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              Run Demo Batch (NSL-KDD Test Split)
            </button>
          </div>
        </div>

        <div className="p-3 rounded-xl bg-cyber-darker/60 border border-cyber-border/60 text-xs text-slate-400 flex items-center gap-2">
          <Info className="w-4 h-4 text-cyber-cyan flex-shrink-0" />
          <span>
            Accepts official NetFlow columns: <code className="text-cyber-cyan font-mono">protocol_type, service, flag, src_bytes, dst_bytes, count, srv_count, serror_rate...</code>
          </span>
        </div>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="glass-panel p-12 rounded-2xl border border-cyber-border flex flex-col items-center justify-center space-y-3">
          <RefreshCw className="w-8 h-8 text-cyber-teal animate-spin" />
          <p className="text-sm font-mono text-slate-300">Processing NetFlow Records & Computing Isolation Ensembles...</p>
          <span className="text-xs text-slate-500">Transforming 36 dimensions through Standard Scaler and One-Hot encoders</span>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Inspection Results */}
      {data && !loading && (
        <div className="space-y-6 animate-in fade-in duration-300">
          {/* Summary KPIs */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="glass-panel p-4 rounded-xl border border-cyber-border">
              <span className="text-xs text-slate-400 block uppercase font-mono">Flow Records</span>
              <span className="text-2xl font-bold font-mono text-white mt-1 block">
                {data.summary.total_records}
              </span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-cyber-border">
              <span className="text-xs text-slate-400 block uppercase font-mono">Attacks Flagged</span>
              <span className="text-2xl font-bold font-mono text-rose-400 mt-1 block">
                {data.summary.attack_count}
              </span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-cyber-border">
              <span className="text-xs text-slate-400 block uppercase font-mono">Normal Baseline</span>
              <span className="text-2xl font-bold font-mono text-emerald-400 mt-1 block">
                {data.summary.normal_count}
              </span>
            </div>
            <div className="glass-panel p-4 rounded-xl border border-cyber-border">
              <span className="text-xs text-slate-400 block uppercase font-mono">Threat Share</span>
              <span className="text-2xl font-bold font-mono text-cyber-cyan mt-1 block">
                {data.summary.threat_percentage}%
              </span>
            </div>
          </div>

          {/* Attack Distribution Bar Chart */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border">
            <h3 className="text-base font-bold text-white mb-1">Intrusion Categories Distribution</h3>
            <p className="text-xs text-slate-400 mb-4">Classified threat vectors & statistical anomalies</p>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryChartData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e3256" opacity={0.5} />
                  <XAxis
                    dataKey="name"
                    stroke="#94a3b8"
                    fontSize={10}
                    interval={0}
                    angle={-15}
                    textAnchor="end"
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0b1324', borderColor: '#1e3256', borderRadius: '10px', fontSize: '12px' }}
                  />
                  <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    {categoryChartData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={CAT_COLORS[entry.name] || '#38bdf8'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Labeled Records Table */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 mb-4">
              <div>
                <h3 className="text-base font-bold text-white">Flow-by-Flow Labeled Inspection</h3>
                <p className="text-xs text-slate-400">Classified using Random Forest & Isolation Forest</p>
              </div>

              {/* Filter Tabs */}
              <div className="flex items-center gap-1.5 p-1 rounded-xl bg-cyber-darker border border-cyber-border text-xs">
                {['ALL', 'ATTACK', 'NORMAL'].map((mode) => (
                  <button
                    key={mode}
                    onClick={() => setFilter(mode)}
                    className={`px-3 py-1 rounded-lg font-mono text-[11px] font-semibold transition-all ${
                      filter === mode
                        ? 'bg-cyber-card text-cyber-teal border border-cyber-teal/30 shadow-glow-teal'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {mode} ({mode === 'ALL' ? data.rows.length : mode === 'ATTACK' ? data.summary.attack_count : data.summary.normal_count})
                  </button>
                ))}
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-cyber-darker text-slate-400 uppercase font-mono text-[11px] border-b border-cyber-border">
                  <tr>
                    <th className="py-2.5 px-3">#</th>
                    <th className="py-2.5 px-3">Verdict</th>
                    <th className="py-2.5 px-3">Category</th>
                    <th className="py-2.5 px-3">Protocol / Service</th>
                    <th className="py-2.5 px-3">Flag</th>
                    <th className="py-2.5 px-3">Risk Score</th>
                    <th className="py-2.5 px-3">Detection Forensics</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-cyber-border/60 text-slate-300">
                  {filteredRows.slice(0, 30).map((row) => (
                    <tr key={row.row_id} className="hover:bg-cyber-cardHover/60 transition-colors">
                      <td className="py-2.5 px-3 font-mono text-slate-400">{row.row_id}</td>
                      <td className="py-2.5 px-3">
                        <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-bold ${
                          row.is_attack
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                            : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                        }`}>
                          {row.verdict}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">
                        {row.attack_category}
                      </td>
                      <td className="py-2.5 px-3 font-mono text-cyber-cyan text-[11px]">
                        {row.protocol.toUpperCase()} / {row.service}
                      </td>
                      <td className="py-2.5 px-3 font-mono text-slate-400">{row.flag}</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-cyber-teal">
                        {row.risk_score}%
                      </td>
                      <td className="py-2.5 px-3 max-w-sm text-slate-400 truncate text-[11px]" title={row.details}>
                        {row.details}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {filteredRows.length > 30 && (
              <p className="text-center text-xs font-mono text-slate-400 mt-4">
                Showing top 30 of {filteredRows.length} labeled flow records.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
