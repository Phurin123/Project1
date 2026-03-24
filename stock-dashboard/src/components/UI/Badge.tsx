import React from 'react';

interface BadgeProps {
  text: string;
  type: 'buy' | 'sell' | 'hold';
}

export const Badge: React.FC<BadgeProps> = ({ text, type }) => {
  const colors = {
    buy: 'bg-green-100 text-green-800',
    sell: 'bg-red-100 text-red-800',
    hold: 'bg-yellow-100 text-yellow-800',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[type]}`}>
      {text}
    </span>
  );
};