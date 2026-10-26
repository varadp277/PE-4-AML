import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  Activity,
  AlertTriangle,
  Flame,
  CheckCircle,
  RefreshCw,
  ExternalLink,
  ChevronRight,
  Filter
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  CartesianGrid
} from 'recharts';

import api from '../services/api';
import StatCard from '../components/StatCard';
import SeverityBadge from '../components/SeverityBadge';
import AlertReviewModal from '../components/AlertReviewModal';

const PIE_COLORS = ['#0df2c9', '#38bdf8', '#f59e0b', '#f43f5e'];

export default function Dashboard({ onNavigate }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedAlertForReview, setSelectedAlertForReview] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard stats:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleReviewSubmitted = async (alertId, verdict, notes) => {
    await api.reviewAlert(alertId, verdict, notes);
    await fetchStats();
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-3">
        <RefreshCw className="w-8 h-8 text-cyber-teal animate-spin" />
        <p className="text-sm font-mono text-slate-400">Loading Threat Intelligence Telemetry...</p>
      </div>
    );
  }

  // Format threat types data for pie chart
  const threatTypesData = stats?.threats_by_module ? [
    { name: 'Phishing URLs', value: stats.threats_by_module.phishing || 0 },
    { name: 'Network Intrusions', value: stats.threats_by_module.network || 0 },
    { name: 'UEBA Login Anomalies', value: stats.threats_by_module.login || 0 },
  ].filter(d => d.value > 0) : [];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Top Banner with Refresh Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            Threat Intelligence Operations
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time aggregate telemetry across Phishing, NetFlow, and UEBA authentication vectors
          </p>
        </div>

        <button
          onClick={() => { setRefreshing(true); fetchStats(); }}
          disabled={refreshing}
          className="px-3.5 py-2 rounded-xl bg-cyber-card hover:bg-cyber-cardHover border border-cyber-border text-xs font-semibold text-slate-200 flex items-center gap-2 transition-all self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-cyber-teal ${refreshing ? 'animate-spin' : ''}`} />
          {refreshing ? 'Refreshing...' : 'Refresh Telemetry'}
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Scans"
          value={stats?.total_scans?.toLocaleString() || '0'}
          subtext="Telemetry inputs processed"
          icon={Activity}
          variant="cyan"
        />
        <StatCard
          title="Threats Detected"
          value={stats?.threats_detected?.toLocaleString() || '0'}
          subtext="High & Critical incidents logged"
          icon={ShieldAlert}
          variant="rose"
        />
        <StatCard
          title="Alerts Today"
          value={stats?.alerts_today?.toLocaleString() || '0'}
          subtext="Active 24h operational alerts"
          icon={AlertTriangle}
          variant="amber"
        />
        <StatCard
          title="Average Risk Score"
          value={`${stats?.average_risk_score || 0}%`}
          subtext="Composite multi-module index"
          icon={Flame}
          variant="teal"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Threats Over Time Chart */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-cyber-border">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Threats Over Time</h3>
              <p className="text-xs text-slate-400">Incident volume distribution over past 7 days</p>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <span className="flex items-center gap-1.5 text-cyber-teal">
                <span className="w-2.5 h-2.5 rounded-full bg-cyber-teal"></span> Phishing
              </span>
              <span className="flex items-center gap-1.5 text-cyber-cyan">
                <span className="w-2.5 h-2.5 rounded-full bg-cyber-cyan"></span> Network
              </span>
              <span className="flex items-center gap-1.5 text-amber-400">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Login
              </span>
            </div>
          </div>

          <div className="h-64 w-full">
            {stats?.threats_over_time?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats.threats_over_time} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorThreats" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0df2c9" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#0df2c9" stopOpacity={0.0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e3256" opacity={0.5} />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0b1324', borderColor: '#1e3256', borderRadius: '12px', fontSize: '12px' }}
                    itemStyle={{ color: '#0df2c9' }}
                  />
                  <Area type="monotone" dataKey="threats" stroke="#0df2c9" strokeWidth={2} fillOpacity={1} fill="url(#colorThreats)" name="Total Incidents" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                No temporal telemetry recorded yet.
              </div>
            )}
          </div>
        </div>

        {/* Threat Types Breakdown Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-cyber-border flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Threat Types Breakdown</h3>
            <p className="text-xs text-slate-400">Incidents by vector module</p>
          </div>

          <div className="h-52 w-full my-auto flex items-center justify-center">
            {threatTypesData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={threatTypesData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {threatTypesData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} stroke="#0b1324" strokeWidth={2} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0b1324', borderColor: '#1e3256', borderRadius: '10px', fontSize: '12px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-xs text-slate-400">No threat types classified yet.</div>
            )}
          </div>

          <div className="space-y-1.5 pt-2 border-t border-cyber-border/80 text-xs">
            {threatTypesData.map((d, idx) => (
              <div key={d.name} className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-slate-300">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: PIE_COLORS[idx % PIE_COLORS.length] }}></span>
                  {d.name}
                </span>
                <span className="font-mono font-bold text-slate-200">{d.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Risk Sources & Recent Alerts Table */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Top Risk Sources */}
        <div className="glass-panel p-6 rounded-2xl border border-cyber-border lg:col-span-1">
          <h3 className="text-base font-bold text-white mb-1">Top Risk Sources</h3>
          <p className="text-xs text-slate-400 mb-4">Highest occurrence identifiers</p>

          <div className="space-y-3">
            {stats?.top_risk_sources?.length > 0 ? (
              stats.top_risk_sources.map((src, i) => (
                <div key={i} className="p-3 rounded-xl bg-cyber-darker border border-cyber-border text-xs">
                  <div className="font-mono text-slate-200 truncate font-medium" title={src.source}>
                    {src.source}
                  </div>
                  <div className="flex items-center justify-between mt-2 pt-2 border-t border-cyber-border/60 text-slate-400">
                    <span>Incidents: <strong className="text-white font-mono">{src.count}</strong></span>
                    <span className="text-cyber-cyan font-mono font-semibold">{src.max_risk}% Risk</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-xs text-slate-400 py-4 text-center">No repeat risk sources identified.</div>
            )}
          </div>
        </div>

        {/* Recent Alerts Feed with "Mark as reviewed" */}
        <div className="glass-panel p-6 rounded-2xl border border-cyber-border lg:col-span-3">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Active Threat Feed & Triage</h3>
              <p className="text-xs text-slate-400">Recent security incidents requiring analyst review</p>
            </div>
            <button
              onClick={() => onNavigate('alerts')}
              className="text-xs font-semibold text-cyber-teal hover:underline flex items-center gap-1"
            >
              View All Alerts <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-cyber-darker text-slate-400 uppercase font-mono text-[11px] border-b border-cyber-border">
                <tr>
                  <th className="py-2.5 px-3">Severity</th>
                  <th className="py-2.5 px-3">Incident Title</th>
                  <th className="py-2.5 px-3">Module</th>
                  <th className="py-2.5 px-3">Risk</th>
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-cyber-border/60 text-slate-300">
                {stats?.recent_alerts?.length > 0 ? (
                  stats.recent_alerts.slice(0, 7).map((alert) => (
                    <tr key={alert.id} className="hover:bg-cyber-cardHover/60 transition-colors">
                      <td className="py-3 px-3">
                        <SeverityBadge severity={alert.severity} />
                      </td>
                      <td className="py-3 px-3 max-w-xs truncate font-medium text-slate-200">
                        {alert.title}
                        {alert.is_reviewed && (
                          <span className="ml-2 inline-flex items-center text-[10px] text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
                            Reviewed
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-3 uppercase font-mono text-[11px] text-cyber-cyan">
                        {alert.module}
                      </td>
                      <td className="py-3 px-3 font-mono font-bold text-cyber-teal">
                        {alert.risk_score}%
                      </td>
                      <td className="py-3 px-3 text-slate-400 font-mono text-[11px]">
                        {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </td>
                      <td className="py-3 px-3 text-right">
                        {alert.is_reviewed ? (
                          <span className="text-slate-400 font-mono text-[11px]">
                            {alert.analyst_verdict || 'Verified'}
                          </span>
                        ) : (
                          <button
                            onClick={() => setSelectedAlertForReview(alert)}
                            className="px-2.5 py-1 rounded bg-cyber-teal/15 hover:bg-cyber-teal/25 border border-cyber-teal/40 text-cyber-teal font-semibold text-[11px] transition-all"
                          >
                            Review
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="py-8 text-center text-slate-400">
                      No active alerts in queue. System is clear.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Review Modal */}
      {selectedAlertForReview && (
        <AlertReviewModal
          alert={selectedAlertForReview}
          onClose={() => setSelectedAlertForReview(null)}
          onReviewSubmitted={handleReviewSubmitted}
        />
      )}
    </div>
  );
}
