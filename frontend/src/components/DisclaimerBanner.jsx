import React from 'react';
import { ShieldAlert, Info } from 'lucide-react';

export default function DisclaimerBanner({ compact = false }) {
  if (compact) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-cyber-darker border border-cyber-border text-xs text-slate-400">
        <Info className="w-4 h-4 text-cyber-teal flex-shrink-0" />
        <span>Defensive & Educational Use Only — College Case Study Benchmark</span>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-cyber-card via-[#0c1830] to-cyber-card border-b border-cyber-border px-4 py-2.5 text-xs text-slate-300 flex items-center justify-between">
      <div className="flex items-center gap-2 max-w-4xl">
        <ShieldAlert className="w-4 h-4 text-cyber-teal flex-shrink-0" />
        <span>
          <strong className="text-cyber-teal font-semibold">Educational Case Study Notice:</strong> This AI Threat Intelligence platform demonstrates automated defensive detection (Phishing, Network Intrusion, UEBA). All outputs are for academic learning and should not be used as the sole basis for live production security without human analyst verification.
        </span>
      </div>
      <div className="hidden sm:flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-cyber-teal animate-ping"></span>
        <span className="font-mono text-[11px] text-cyber-teal">DEFENSIVE_ENGINE_ACTIVE</span>
      </div>
    </div>
  );
}
