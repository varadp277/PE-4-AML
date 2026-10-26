import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Database,
  Layers,
  Sparkles,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  TrendingUp,
  AlertCircle,
  Clock,
  RotateCcw
} from 'lucide-react';
import api from '../services/api';
import StatCard from '../components/StatCard';

export default function ModelInfo() {
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [retrainResult, setRetrainResult] = useState(null);
  const [error, setError] = useState(null);

  const fetchMetadata = async () => {
    try {
      const data = await api.getModelsInfo();
      setMetadata(data);
    } catch (err) {
      console.error('Failed to load model metadata:', err);
      setError('Failed to fetch training metadata. Ensure models are trained.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetadata();
  }, []);

  const handleRetrain = async (module = 'all') => {
    setRetraining(true);
    setRetrainResult(null);
    setError(null);

    try {
      const result = await api.retrainModel(module);
      setRetrainResult(result);
      await fetchMetadata();
    } catch (err) {
      console.error('Retraining failed:', err);
      setError(err.response?.data?.detail || 'Retraining failed. Check backend logs.');
    } finally {
      setRetraining(false);
    }
  };

  if (loading) {
    return (
      <div className="py-24 text-center space-y-3">
        <RefreshCw className="w-8 h-8 text-cyber-teal animate-spin mx-auto" />
        <p className="text-sm font-mono text-slate-400">Loading Model Metadata & Dataset Audits...</p>
      </div>
    );
  }

  const summary = metadata?.summary || {};
  const models = metadata?.models || {};

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header & Retrain Trigger Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal text-xs font-mono font-semibold mb-3">
            <Cpu className="w-3.5 h-3.5" />
            AUDITING & TRANSPARENCY // NO HARDCODED VALUES
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Model Registry & Training Metrics</h2>
          <p className="text-xs text-slate-400 mt-1">
            Auditable provenance: records, dimensions, splits, and evaluation confusion matrices read dynamically from real training data.
          </p>
        </div>

        <button
          onClick={() => handleRetrain('all')}
          disabled={retraining}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyber-teal to-cyber-cyan text-slate-950 font-bold text-xs uppercase tracking-wider hover:opacity-90 transition-all flex items-center gap-2 shadow-glow-teal disabled:opacity-50 self-start sm:self-auto"
        >
          <RotateCcw className={`w-4 h-4 ${retraining ? 'animate-spin' : ''}`} />
          {retraining ? 'Retraining Pipeline In Progress...' : 'Retrain All Models with Analyst Feedback'}
        </button>
      </div>

      {/* Retrain Result Alert Banner */}
      {retrainResult && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs animate-in fade-in space-y-2">
          <div className="flex items-center gap-2 font-bold text-sm text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
            Retraining Pipeline Completed Successfully!
          </div>
          <p className="text-slate-300">
            {retrainResult.message} Incorporated {retrainResult.total_analyst_feedback_records_used} analyst-reviewed incidents into the training dataset.
          </p>
          {retrainResult.modules_updated?.phishing && (
            <div className="font-mono text-[11px] text-cyber-teal pt-1 border-t border-emerald-500/20">
              Phishing Model F1: {retrainResult.modules_updated.phishing.previous_f1} &rarr; {retrainResult.modules_updated.phishing.new_f1}
              ({retrainResult.modules_updated.phishing.analyst_samples_incorporated} feedback samples merged)
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Real Computed Global Totals Cards (Zero Hardcoded) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <StatCard
          title="Datasets Used"
          value={summary.total_datasets || 0}
          subtext="Unique public benchmark datasets"
          icon={Database}
          variant="teal"
        />
        <StatCard
          title="Total Records Trained On"
          value={(summary.total_records_trained_on || 0).toLocaleString()}
          subtext="Summed real instances in training manifolds"
          icon={Layers}
          variant="cyan"
        />
        <StatCard
          title="Models Trained"
          value={summary.total_models_trained || 0}
          subtext="Supervised & Unsupervised artifacts"
          icon={Cpu}
          variant="amber"
        />
      </div>

      {/* Models Detail Cards */}
      <div className="space-y-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyber-teal" />
          Active Model Registries
        </h3>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {Object.entries(models).map(([modelId, m]) => (
            <div
              key={modelId}
              className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-cyber-border/80 transition-all flex flex-col justify-between space-y-5"
            >
              <div>
                {/* Header */}
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <span className="text-[10px] font-mono text-cyber-teal uppercase tracking-wider block">
                      {m.algorithm}
                    </span>
                    <h4 className="text-base font-bold text-white mt-0.5">{m.model_name}</h4>
                  </div>
                  {m.is_retrained && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyber-teal/20 text-cyber-teal border border-cyber-teal/30">
                      Retrained V2
                    </span>
                  )}
                </div>

                {/* Dataset Link & Source */}
                <div className="p-3 rounded-xl bg-cyber-darker border border-cyber-border text-xs space-y-1 mb-4">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 font-mono text-[11px]">DATASET:</span>
                    <span className="font-semibold text-slate-200">{m.dataset_name}</span>
                  </div>
                  {m.dataset_source_link && m.dataset_source_link.startsWith('http') && (
                    <div className="pt-1 border-t border-cyber-border/60">
                      <a
                        href={m.dataset_source_link}
                        target="_blank"
                        rel="noreferrer"
                        className="text-cyber-cyan hover:underline flex items-center gap-1 font-mono text-[11px]"
                      >
                        Academic Source Link <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  )}
                </div>

                {/* Training Metadata Stats Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 text-xs font-mono mb-4">
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">Train Records</span>
                    <span className="font-bold text-white text-sm">{(m.num_records_trained || 0).toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">Test Records</span>
                    <span className="font-bold text-slate-200 text-sm">{(m.num_records_tested || 0).toLocaleString()}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">Features</span>
                    <span className="font-bold text-cyber-cyan text-sm">{m.num_features || 0}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">Accuracy</span>
                    <span className="font-bold text-cyber-teal text-sm">
                      {m.accuracy !== null ? `${(m.accuracy * 100).toFixed(1)}%` : 'N/A'}
                    </span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">Precision</span>
                    <span className="font-bold text-white text-sm">
                      {m.precision !== null ? `${(m.precision * 100).toFixed(1)}%` : 'N/A'}
                    </span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-cyber-darker/60 border border-cyber-border">
                    <span className="text-[10px] text-slate-400 block">F1 Score</span>
                    <span className="font-bold text-amber-400 text-sm">
                      {m.f1_score !== null ? `${(m.f1_score * 100).toFixed(1)}%` : 'N/A'}
                    </span>
                  </div>
                </div>

                {/* Confusion Matrix Visualization */}
                {m.confusion_matrix && (
                  <div className="p-3 rounded-xl bg-cyber-darkest border border-cyber-border text-xs">
                    <span className="font-mono text-[10px] text-slate-400 uppercase tracking-wider block mb-2">
                      Validation Confusion Matrix (TN, FP / FN, TP):
                    </span>
                    <div className="grid grid-cols-2 gap-2 text-center font-mono">
                      <div className="p-2 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
                        <span className="text-[9px] text-slate-400 block">True Negative</span>
                        <span className="text-base font-bold">{m.confusion_matrix[0]?.[0]}</span>
                      </div>
                      <div className="p-2 rounded bg-rose-500/10 border border-rose-500/30 text-rose-300">
                        <span className="text-[9px] text-slate-400 block">False Positive</span>
                        <span className="text-base font-bold">{m.confusion_matrix[0]?.[1]}</span>
                      </div>
                      <div className="p-2 rounded bg-amber-500/10 border border-amber-500/30 text-amber-300">
                        <span className="text-[9px] text-slate-400 block">False Negative</span>
                        <span className="text-base font-bold">{m.confusion_matrix[1]?.[0]}</span>
                      </div>
                      <div className="p-2 rounded bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal">
                        <span className="text-[9px] text-slate-400 block">True Positive</span>
                        <span className="text-base font-bold">{m.confusion_matrix[1]?.[1]}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Training Date Footer */}
              <div className="pt-3 border-t border-cyber-border/60 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span className="flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5" />
                  Trained: {m.trained_at ? new Date(m.trained_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recent'}
                </span>
                <span className="text-slate-400">{m.train_test_split}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
