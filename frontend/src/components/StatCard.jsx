import React from 'react';

export default function StatCard({ title, value, subtext, icon: Icon, trend, variant = 'teal' }) {
  const variantStyles = {
    teal: 'border-cyber-border hover:border-cyber-teal/50 hover:shadow-glow-teal',
    rose: 'border-cyber-border hover:border-rose-500/50 hover:shadow-glow-rose',
    amber: 'border-cyber-border hover:border-amber-500/50',
    cyan: 'border-cyber-border hover:border-cyber-cyan/50 hover:shadow-glow-cyan',
  };

  const iconColors = {
    teal: 'text-cyber-teal bg-cyber-teal/10 border-cyber-teal/20',
    rose: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    cyan: 'text-cyber-cyan bg-cyber-cyan/10 border-cyber-cyan/20',
  };

  return (
    <div className={`glass-panel p-5 rounded-xl border transition-all duration-300 ${variantStyles[variant] || variantStyles.teal}`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400 tracking-wide uppercase">{title}</span>
        {Icon && (
          <div className={`p-2.5 rounded-lg border ${iconColors[variant] || iconColors.teal}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-3xl font-bold font-mono text-white tracking-tight">{value}</span>
        {trend && (
          <span className="text-xs font-semibold text-cyber-teal flex items-center">
            {trend}
          </span>
        )}
      </div>
      {subtext && (
        <p className="mt-1.5 text-xs text-slate-400 truncate">{subtext}</p>
      )}
    </div>
  );
}
