import React, { useState } from 'react';
import {
  Globe,
  Search,
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  ArrowRight,
  ExternalLink,
  Code2,
  Info,
  HelpCircle,
  Sparkles
} from 'lucide-react';
import api from '../services/api';

const SAMPLE_URLS = [
  {
    type: 'Safe',
    url: 'https://en.wikipedia.org/wiki/Machine_learning',
    desc: 'Legitimate Wikipedia encyclopedia page with standard HTTPS'
  },
  {
    type: 'Phishing',
    url: 'http://192.168.1.105/paypal/secure-login-verification/auth.php?id=99281',
    desc: 'Suspicious IP address with social engineering keywords & HTTP'
  },
  {
    type: 'Phishing',
    url: 'http://secure-chase-account-verify.auth-portal99.xyz/index.html',
    desc: 'Brand imitation with deceptive subdomains & high-risk TLD'
  },
  {
    type: 'Suspicious',
    url: 'http://login-update-service.com@webscr-account-reset.info/auth',
    desc: 'Obfuscated target using "@" symbol trick to deceive parser'
  }
];

export default function PhishingScan() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showFeatures, setShowFeatures] = useState(false);

  const handleScan = async (targetUrl = url) => {
    const finalUrl = (targetUrl || '').trim();
    if (!finalUrl) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.scanUrl(finalUrl);
      setResult(data);
    } catch (err) {
      console.error('Scan failed:', err);
      setError(err.response?.data?.detail || 'Failed to scan URL. Please verify backend connection.');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictStyle = (verdict) => {
    switch (verdict) {
      case 'Phishing':
        return {
          bg: 'bg-rose-500/10 border-rose-500/40 text-rose-400',
          badge: 'bg-rose-500 text-white',
          icon: ShieldAlert,
          title: 'Phishing Domain Detected'
        };
      case 'Suspicious':
        return {
          bg: 'bg-amber-500/10 border-amber-500/40 text-amber-400',
          badge: 'bg-amber-500 text-slate-950',
          icon: AlertTriangle,
          title: 'Suspicious URL Attributes'
        };
      default:
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400',
          badge: 'bg-emerald-500 text-slate-950',
          icon: CheckCircle2,
          title: 'Safe / Legitimate Domain'
        };
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal text-xs font-mono font-semibold mb-3">
          <Globe className="w-3.5 h-3.5" />
          MODULE 1 // UCI PHISHING WEBSITES MODEL
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          Phishing URL Analysis & Explainable AI
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Lexical, structural, and semantic feature inspection comparing XGBoost and Random Forest classifiers.
        </p>
      </div>

      {/* Input Box */}
      <div className="glass-panel p-6 rounded-2xl border border-cyber-border space-y-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleScan();
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste a URL to inspect (e.g. http://secure-paypal-login.verify.xyz)..."
              className="w-full bg-cyber-darker border border-cyber-border rounded-xl pl-11 pr-4 py-3 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-cyber-teal focus:ring-1 focus:ring-cyber-teal transition-all font-mono"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="px-6 py-3 rounded-xl bg-cyber-teal hover:bg-cyber-teal/90 text-slate-950 font-bold text-sm transition-all flex items-center justify-center gap-2 shadow-glow-teal disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                Analyzing...
              </>
            ) : (
              <>
                Analyze URL
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Quick Sample Selector */}
        <div className="pt-2 border-t border-cyber-border/60">
          <span className="text-[11px] font-mono text-slate-400 block mb-2 uppercase tracking-wider">
            Quick Test Samples:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {SAMPLE_URLS.map((sample, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setUrl(sample.url);
                  handleScan(sample.url);
                }}
                className="p-2.5 rounded-xl bg-cyber-darker hover:bg-cyber-cardHover border border-cyber-border text-left transition-all text-xs flex items-center justify-between group"
              >
                <div className="truncate pr-2">
                  <span className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-mono font-bold mr-2 ${
                    sample.type === 'Safe' ? 'bg-emerald-500/20 text-emerald-400' :
                    sample.type === 'Phishing' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {sample.type}
                  </span>
                  <span className="font-mono text-slate-300 group-hover:text-cyber-teal transition-colors">
                    {sample.url}
                  </span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyber-teal flex-shrink-0" />
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Result Card */}
      {result && (
        <div className="glass-panel rounded-2xl border border-cyber-border overflow-hidden space-y-6 p-6 animate-in fade-in duration-300">
          {(() => {
            const vStyle = getVerdictStyle(result.verdict);
            const VIcon = vStyle.icon;

            return (
              <div className={`p-5 rounded-xl border ${vStyle.bg} flex flex-col md:flex-row md:items-center justify-between gap-4`}>
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-xl bg-black/30 border border-white/10">
                    <VIcon className="w-8 h-8" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2.5">
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold font-mono uppercase tracking-wider ${vStyle.badge}`}>
                        {result.verdict}
                      </span>
                      <span className="text-xs font-mono text-slate-300">
                        Model: <strong className="text-white">{result.model_used}</strong>
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-white mt-1">{vStyle.title}</h3>
                    <p className="text-xs text-slate-300 font-mono truncate max-w-xl">{result.url}</p>
                  </div>
                </div>

                {/* Risk & Confidence Badges */}
                <div className="flex items-center gap-4 bg-black/40 p-3 rounded-xl border border-white/10 self-start md:self-auto">
                  <div className="text-center px-2">
                    <span className="block text-[10px] text-slate-400 uppercase font-mono">Risk Score</span>
                    <span className="text-2xl font-bold font-mono text-white">{result.risk_score}%</span>
                  </div>
                  <div className="h-8 w-[1px] bg-white/20"></div>
                  <div className="text-center px-2">
                    <span className="block text-[10px] text-slate-400 uppercase font-mono">Confidence</span>
                    <span className="text-2xl font-bold font-mono text-cyber-teal">
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Top Reasons / Explainability */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyber-teal" />
                Explainable AI: Key Risk Factors
              </h4>
              <span className="text-xs font-mono text-slate-400">
                {result.reasons?.length || 0} indicators flagged
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {result.reasons?.map((reason, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-cyber-darker border border-cyber-border text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-slate-200">{reason.factor}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                      reason.impact === 'High' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                      reason.impact === 'Medium' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                      reason.impact === 'Low' ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30' :
                      'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    }`}>
                      {reason.impact} Impact
                    </span>
                  </div>
                  <p className="text-slate-400 text-[11px] leading-relaxed">{reason.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Extracted Features Toggle */}
          <div className="pt-2 border-t border-cyber-border">
            <button
              onClick={() => setShowFeatures(!showFeatures)}
              className="text-xs font-mono text-cyber-teal hover:underline flex items-center gap-1.5"
            >
              <Code2 className="w-3.5 h-3.5" />
              {showFeatures ? 'Hide Extracted Vector Features' : 'View Full Extracted Feature Vector (17 features)'}
            </button>

            {showFeatures && (
              <div className="mt-3 p-4 rounded-xl bg-cyber-darkest border border-cyber-border overflow-x-auto text-xs font-mono">
                <table className="w-full text-left">
                  <thead className="text-slate-400 border-b border-cyber-border">
                    <tr>
                      <th className="pb-2">Feature Name</th>
                      <th className="pb-2">Extracted Value</th>
                      <th className="pb-2">Defensive Context</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-cyber-border/40 text-slate-300">
                    {Object.entries(result.features_extracted || {}).map(([key, val]) => (
                      <tr key={key}>
                        <td className="py-1.5 text-cyber-cyan">{key}</td>
                        <td className="py-1.5 font-bold text-white">{String(val)}</td>
                        <td className="py-1.5 text-slate-400 text-[11px]">
                          {key.includes('http') ? 'Transport layer validation' :
                           key.includes('ip') ? 'Direct host addressing' :
                           key.includes('entropy') ? 'Domain character dispersion' :
                           key.includes('keyword') ? 'Social engineering terms' : 'Lexical metric'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
