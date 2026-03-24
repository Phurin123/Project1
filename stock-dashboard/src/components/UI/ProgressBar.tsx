import React from 'react';

interface ProgressBarProps {
  value: number; // -1 to 1
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ value }) => {
  const isPositive = value > 0;
  const width = Math.min(Math.abs(value) * 100, 100);

  return (
    <div className="flex items-center gap-2">
      <div className="w-16 bg-gray-200 rounded-full h-1.5 overflow-hidden">
        <div 
          className={`h-full rounded-full transition-all duration-500 ${isPositive ? 'bg-green-500' : 'bg-red-500'}`} 
          style={{ width: `${width}%` }}
        />
      </div>
      <span className="text-xs text-gray-500 font-mono">{value.toFixed(2)}</span>
    </div>
  );
};