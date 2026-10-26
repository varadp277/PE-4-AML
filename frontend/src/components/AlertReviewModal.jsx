import React, { useState } from 'react';
import { X, CheckCircle, AlertTriangle, ShieldCheck, MessageSquare } from 'lucide-react';
import SeverityBadge from './SeverityBadge';

export default function AlertReviewModal({ alert, onClose, onReviewSubmitted }) {
  const [verdict, setVerdict] = useState('Confirmed Threat');
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!alert) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onReviewSubmitted(alert.id, verdict, notes);
      onClose();
    } catch (err) {
      console.error('Failed to submit review:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="glass-panel-glow w-full max-w-lg rounded-2xl p-6 border border-cyber-border shadow-2xl relative animate-in fade-in zoom-in-95 duration-200">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Analyst Alert Triage</h3>
            <p className="text-xs text-slate-400">Record investigation feedback to train the feedback loop</p>
          </div>
        </div>

        {/* Alert Metadata Card */}
        <div className="bg-cyber-darker p-3.5 rounded-xl border border-cyber-border mb-5 text-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs text-slate-400">ALERT #{alert.id}</span>
            <SeverityBadge severity={alert.severity} />
          </div>
          <div className="font-semibold text-slate-200">{alert.title}</div>
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span className="uppercase text-cyber-teal font-mono">{alert.module}</span>
            <span>•</span>
            <span className="truncate">{alert.source_identifier || 'Telemetry flow'}</span>
          </div>
          <div className="text-xs text-slate-400">
            Initial Risk Score: <span className="font-mono font-bold text-cyber-cyan">{alert.risk_score} / 100</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Analyst Verdict
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setVerdict('Confirmed Threat')}
                className={`py-2 px-3 rounded-lg text-xs font-medium border flex items-center justify-center gap-1.5 transition-all ${
                  verdict === 'Confirmed Threat'
                    ? 'bg-rose-500/20 border-rose-500 text-rose-300 shadow-glow-rose'
                    : 'bg-cyber-card border-cyber-border text-slate-400 hover:text-slate-200'
                }`}
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                Confirmed Threat
              </button>

              <button
                type="button"
                onClick={() => setVerdict('False Positive')}
                className={`py-2 px-3 rounded-lg text-xs font-medium border flex items-center justify-center gap-1.5 transition-all ${
                  verdict === 'False Positive'
                    ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-glow-teal'
                    : 'bg-cyber-card border-cyber-border text-slate-400 hover:text-slate-200'
                }`}
              >
                <CheckCircle className="w-3.5 h-3.5" />
                False Positive
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Analyst Notes & Justification
            </label>
            <textarea
              rows="3"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Verified typosquatted domain hosted on bulletproof server; confirmed malicious intent..."
              className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-cyber-teal placeholder:text-slate-500"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-xs font-medium text-slate-400 hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 rounded-lg bg-cyber-teal text-slate-950 font-semibold text-xs hover:bg-cyber-teal/90 transition-all flex items-center gap-1.5 disabled:opacity-50"
            >
              {submitting ? 'Saving Review...' : 'Submit & Store Feedback'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
