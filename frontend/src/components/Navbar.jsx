import React from 'react';
import { ShieldCheck, Server, AlertCircle } from 'lucide-react';

export default function Navbar({ activeTitle, subtitle }) {
  return (
    <header className="h-16 bg-cyber-darker/90 backdrop-blur-md border-b border-cyber-border px-6 flex items-center justify-between sticky top-0 z-30">
      <div>
        <h1 className="text-base font-bold text-white flex items-center gap-2">
          {activeTitle}
        </h1>
        {subtitle && (
          <p className="text-xs text-slate-400">{subtitle}</p>
        )}
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-cyber-card border border-cyber-border text-xs text-slate-300">
          <Server className="w-3.5 h-3.5 text-cyber-teal" />
          <span className="font-mono text-slate-400">REST API:</span>
          <span className="font-mono text-cyber-teal">http://127.0.0.1:8000</span>
        </div>

        <a
          href="http://127.0.0.1:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="px-3 py-1.5 rounded-lg bg-cyber-card hover:bg-cyber-cardHover border border-cyber-border hover:border-cyber-cyan/50 text-xs font-mono text-cyber-cyan flex items-center gap-1.5 transition-all"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-cyber-cyan animate-pulse"></span>
          Swagger Docs
        </a>
      </div>
    </header>
  );
}
