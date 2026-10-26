import React, { useState, useEffect } from 'react';
import {
  BellRing,
  Filter,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  Clock,
  Eye,
  MessageSquare
} from 'lucide-react';
import api from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import AlertReviewModal from '../components/AlertReviewModal';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAlertForReview, setSelectedAlertForReview] = useState(null);
  const [moduleFilter, setModuleFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [reviewFilter, setReviewFilter] = useState(''); // '', 'reviewed', 'pending'

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const params = {};
      if (moduleFilter) params.module = moduleFilter;
      if (severityFilter) params.severity = severityFilter;
      if (reviewFilter === 'reviewed') params.is_reviewed = true;
      if (reviewFilter === 'pending') params.is_reviewed = false;

      const data = await api.getAlerts(params);
      setAlerts(data);
    } catch (err) {
      console.error('Failed to load alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [moduleFilter, severityFilter, reviewFilter]);

  const handleReviewSubmitted = async (alertId, verdict, notes) => {
    await api.reviewAlert(alertId, verdict, notes);
    await fetchAlerts();
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-card border border-cyber-border text-xs font-mono font-semibold text-slate-300 mb-3">
            <BellRing className="w-3.5 h-3.5 text-cyber-teal" />
            INCIDENT TRIAGE & AUDIT LOG
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Security Alerts & Analyst Feedback</h2>
          <p className="text-xs text-slate-400 mt-1">
            Review security incidents, record analyst verdicts, and feed labeled ground truth into the retraining engine.
          </p>
        </div>

        <button
          onClick={fetchAlerts}
          className="px-3.5 py-2 rounded-xl bg-cyber-card hover:bg-cyber-cardHover border border-cyber-border text-xs font-semibold text-slate-200 flex items-center gap-2 transition-all self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-cyber-teal ${loading ? 'animate-spin' : ''}`} />
          Refresh Queue
        </button>
      </div>

      {/* Filters Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-cyber-border flex flex-wrap items-center gap-4 text-xs">
        <div className="flex items-center gap-2 text-slate-400">
          <Filter className="w-4 h-4 text-cyber-teal" />
          <span className="font-semibold uppercase tracking-wider text-[11px]">Filters:</span>
        </div>

        {/* Module Filter */}
        <select
          value={moduleFilter}
          onChange={(e) => setModuleFilter(e.target.value)}
          className="bg-cyber-darker border border-cyber-border rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-cyber-teal"
        >
          <option value="">All Detection Modules</option>
          <option value="phishing">Phishing URLs</option>
          <option value="network">Network Intrusions</option>
          <option value="login">UEBA Logins</option>
        </select>

        {/* Severity Filter */}
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-cyber-darker border border-cyber-border rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-cyber-teal"
        >
          <option value="">All Severities</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

        {/* Review Status Filter */}
        <select
          value={reviewFilter}
          onChange={(e) => setReviewFilter(e.target.value)}
          className="bg-cyber-darker border border-cyber-border rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-cyber-teal"
        >
          <option value="">All Triage States</option>
          <option value="pending">Pending Review Only</option>
          <option value="reviewed">Reviewed Only</option>
        </select>

        {(moduleFilter || severityFilter || reviewFilter) && (
          <button
            onClick={() => { setModuleFilter(''); setSeverityFilter(''); setReviewFilter(''); }}
            className="text-xs text-rose-400 hover:underline font-mono ml-auto"
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Alerts Table */}
      <div className="glass-panel rounded-2xl border border-cyber-border overflow-hidden">
        {loading ? (
          <div className="py-16 text-center space-y-3">
            <RefreshCw className="w-8 h-8 text-cyber-teal animate-spin mx-auto" />
            <p className="text-xs font-mono text-slate-400">Loading incidents queue...</p>
          </div>
        ) : alerts.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-cyber-darker text-slate-400 uppercase font-mono text-[11px] border-b border-cyber-border">
                <tr>
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Module</th>
                  <th className="py-3 px-4">Incident Title & Details</th>
                  <th className="py-3 px-4">Source Identifier</th>
                  <th className="py-3 px-4">Risk Score</th>
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4 text-right">Analyst Review</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-cyber-border/60 text-slate-300">
                {alerts.map((alert) => (
                  <tr key={alert.id} className="hover:bg-cyber-cardHover/60 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-slate-400">#{alert.id}</td>
                    <td className="py-3.5 px-4">
                      <SeverityBadge severity={alert.severity} />
                    </td>
                    <td className="py-3.5 px-4 uppercase font-mono text-[11px] text-cyber-cyan font-semibold">
                      {alert.module}
                    </td>
                    <td className="py-3.5 px-4 max-w-sm">
                      <div className="font-semibold text-slate-200">{alert.title}</div>
                      {alert.analyst_notes && (
                        <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1.5 italic bg-black/30 p-1.5 rounded border border-cyber-border/50">
                          <MessageSquare className="w-3 h-3 text-cyber-teal flex-shrink-0" />
                          <span className="truncate">{alert.analyst_notes}</span>
                        </div>
                      )}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px] truncate max-w-xs" title={alert.source_identifier}>
                      {alert.source_identifier || '—'}
                    </td>
                    <td className="py-3.5 px-4 font-mono font-bold text-cyber-teal text-sm">
                      {alert.risk_score}%
                    </td>
                    <td className="py-3.5 px-4 font-mono text-slate-400 text-[11px] whitespace-nowrap">
                      {new Date(alert.timestamp).toLocaleString([], {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap">
                      {alert.is_reviewed ? (
                        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-mono text-[11px] font-semibold">
                          <CheckCircle className="w-3 h-3" />
                          {alert.analyst_verdict || 'Reviewed'}
                        </div>
                      ) : (
                        <button
                          onClick={() => setSelectedAlertForReview(alert)}
                          className="px-3 py-1.5 rounded-lg bg-cyber-teal hover:bg-cyber-teal/90 text-slate-950 font-bold text-[11px] transition-all shadow-glow-teal"
                        >
                          Mark as reviewed
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-16 text-center text-slate-400 text-xs">
            No alerts match the chosen filters.
          </div>
        )}
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
