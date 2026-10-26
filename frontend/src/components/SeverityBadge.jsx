import React from 'react';

export default function SeverityBadge({ severity }) {
  const s = (severity || 'low').toLowerCase();

  const configs = {
    critical: {
      bg: 'bg-rose-500/15 border-rose-500/40 text-rose-400',
      dot: 'bg-rose-500 animate-pulse',
      label: 'Critical'
    },
    high: {
      bg: 'bg-amber-500/15 border-amber-500/40 text-amber-400',
      dot: 'bg-amber-400',
      label: 'High'
    },
    medium: {
      bg: 'bg-sky-500/15 border-sky-500/40 text-sky-400',
      dot: 'bg-sky-400',
      label: 'Medium'
    },
    low: {
      bg: 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400',
      dot: 'bg-emerald-400',
      label: 'Low'
    }
  };

  const current = configs[s] || configs.low;

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${current.bg}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${current.dot}`}></span>
      {current.label}
    </span>
  );
}
