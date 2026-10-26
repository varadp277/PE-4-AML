import React from 'react';
import {
  ShieldAlert,
  DatabaseZap,
  Lock,
  ArrowRight,
  Globe,
  Radio,
  UserCheck,
  CheckCircle2,
  Terminal,
  Layers,
  Cpu
} from 'lucide-react';

export default function Home({ onNavigate }) {
  return (
    <div className="space-y-10 max-w-6xl mx-auto pb-12">
      {/* Hero Section */}
      <div className="relative rounded-3xl overflow-hidden border border-cyber-border bg-gradient-to-br from-cyber-card via-cyber-darker to-[#091122] p-8 md:p-12 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-96 h-96 bg-cyber-teal/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/3 w-80 h-80 bg-cyber-cyan/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 max-w-3xl space-y-5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal text-xs font-mono font-semibold">
            <span className="w-2 h-2 rounded-full bg-cyber-teal animate-ping"></span>
            COLLEGE CASE STUDY // DEFENSIVE AI BENCHMARK
          </div>

          <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight leading-tight">
            AI-Driven Automated <br />
            <span className="bg-gradient-to-r from-cyber-teal via-cyber-cyan to-blue-400 bg-clip-text text-transparent">
              Threat Intelligence Platform
            </span>
          </h1>

          <p className="text-slate-300 text-base leading-relaxed">
            Modern enterprise security operations suffer from fragmented alert pipelines, signature lag, and sophisticated multi-stage vectors. This platform demonstrates how automated machine learning models (XGBoost, Random Forest, and Isolation Forest) unmask phishing domains, detect network intrusions, and identify anomalous insider logins in real time.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={() => onNavigate('dashboard')}
              className="px-6 py-3 rounded-xl bg-cyber-teal text-slate-950 font-bold text-sm hover:bg-cyber-teal/90 transition-all flex items-center gap-2 shadow-glow-teal"
            >
              Launch Threat Dashboard
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate('models')}
              className="px-6 py-3 rounded-xl bg-cyber-card hover:bg-cyber-cardHover border border-cyber-border hover:border-cyber-cyan/50 text-slate-200 font-semibold text-sm transition-all flex items-center gap-2"
            >
              <Cpu className="w-4 h-4 text-cyber-cyan" />
              View Model Transparency & Retrain
            </button>
          </div>
        </div>
      </div>

      {/* The Problem vs Solution Matrix */}
      <div>
        <div className="text-center max-w-2xl mx-auto mb-8">
          <h2 className="text-2xl font-bold text-white tracking-tight">The Cybersecurity Challenge</h2>
          <p className="text-sm text-slate-400 mt-2">
            Why traditional rules and signature engines fail against modern automated adversary attacks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Problem 1 */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-rose-500/40 transition-all">
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 w-fit mb-4">
              <DatabaseZap className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">1. Data Leaks & Spoofs</h3>
            <p className="text-sm text-slate-300 mt-2 leading-relaxed">
              Adversaries rapidly generate millions of deceptive domains, typosquats, and credential harvesting landing pages that bypass static DNS and keyword blacklists.
            </p>
            <div className="mt-4 pt-4 border-t border-cyber-border/80 text-xs font-mono text-cyber-teal flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Solution: URL Lexical & Entropy ML
            </div>
          </div>

          {/* Problem 2 */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-amber-500/40 transition-all">
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 w-fit mb-4">
              <Layers className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">2. Siloed Security Data</h3>
            <p className="text-sm text-slate-300 mt-2 leading-relaxed">
              Firewall alerts, NetFlow logs, and host sessions live in disconnected silos. SOC analysts drown in false positives without consolidated cross-module risk scoring.
            </p>
            <div className="mt-4 pt-4 border-t border-cyber-border/80 text-xs font-mono text-cyber-teal flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Solution: Unified Tri-Module Pipeline
            </div>
          </div>

          {/* Problem 3 */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-cyber-cyan/40 transition-all">
            <div className="p-3 rounded-xl bg-cyber-cyan/10 border border-cyber-cyan/20 text-cyber-cyan w-fit mb-4">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">3. Reactive Incident Response</h3>
            <p className="text-sm text-slate-300 mt-2 leading-relaxed">
              Defense only triggers after breaches are reported. Without unsupervised anomaly detection and continuous analyst feedback retraining, new zero-days go undetected.
            </p>
            <div className="mt-4 pt-4 border-t border-cyber-border/80 text-xs font-mono text-cyber-teal flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Solution: Isolation Forest & Human-in-Loop Retraining
            </div>
          </div>
        </div>
      </div>

      {/* Detection Modules Overview */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-white">Core Defensive Engines</h2>
            <p className="text-xs text-slate-400 mt-1">Explore each machine learning detector built into the platform</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Module 1 */}
          <div
            onClick={() => onNavigate('phishing')}
            className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-cyber-teal/50 hover:shadow-glow-teal cursor-pointer transition-all group"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-cyber-teal/10 border border-cyber-teal/30 text-cyber-teal">
                <Globe className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-slate-400">UCI Dataset</span>
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-cyber-teal transition-colors">
              Phishing URL Detector
            </h3>
            <p className="text-xs text-slate-300 mt-2 leading-relaxed">
              Real-time lexical, entropy, and token analysis comparing XGBoost and Random Forest models with full explainable feature importance.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-cyber-teal">
              Launch Scanner <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Module 2 */}
          <div
            onClick={() => onNavigate('network')}
            className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-cyber-cyan/50 hover:shadow-glow-cyan cursor-pointer transition-all group"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-cyber-cyan/10 border border-cyber-cyan/30 text-cyber-cyan">
                <Radio className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-slate-400">NSL-KDD / UNSW</span>
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-cyber-cyan transition-colors">
              Network Intrusion Classifier
            </h3>
            <p className="text-xs text-slate-300 mt-2 leading-relaxed">
              CSV batch inspector classifying DoS, Probe, R2L, and U2R signatures via Random Forest, plus zero-day anomaly detection via Isolation Forest.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-cyber-cyan">
              Upload Flow Logs <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Module 3 */}
          <div
            onClick={() => onNavigate('login')}
            className="glass-panel p-6 rounded-2xl border border-cyber-border hover:border-amber-500/50 cursor-pointer transition-all group"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
                <UserCheck className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono text-slate-400">UEBA Profile</span>
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-amber-400 transition-colors">
              Login Anomaly Detector
            </h3>
            <p className="text-xs text-slate-300 mt-2 leading-relaxed">
              User & Entity Behavior Analytics (UEBA) flagging credential stuffing bursts, impossible geographic travel, and abnormal off-hours access.
            </p>
            <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-amber-400">
              Simulate Login <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </div>

      {/* Case Study Technical Specs */}
      <div className="glass-panel p-6 rounded-2xl border border-cyber-border">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-3">
          Architecture & Implementation Integrity
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
          <div className="bg-cyber-darker p-3 rounded-xl border border-cyber-border">
            <span className="text-slate-400 block">Backend</span>
            <span className="text-white font-semibold">Python 3.11 + FastAPI</span>
          </div>
          <div className="bg-cyber-darker p-3 rounded-xl border border-cyber-border">
            <span className="text-slate-400 block">ML Engine</span>
            <span className="text-cyber-teal font-semibold">Scikit-Learn + XGBoost</span>
          </div>
          <div className="bg-cyber-darker p-3 rounded-xl border border-cyber-border">
            <span className="text-slate-400 block">Auditing</span>
            <span className="text-cyber-cyan font-semibold">Real metadata.json (No mocks)</span>
          </div>
          <div className="bg-cyber-darker p-3 rounded-xl border border-cyber-border">
            <span className="text-slate-400 block">Persistence</span>
            <span className="text-white font-semibold">SQLite / SQLAlchemy</span>
          </div>
        </div>
      </div>
    </div>
  );
}
