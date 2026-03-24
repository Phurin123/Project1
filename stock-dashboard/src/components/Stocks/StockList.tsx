import React from 'react';
import type { StockData, StockCardType } from '../../types';
import { StockCard } from './StockCard';

interface StockListProps {
  title: string;
  icon: string;
  stocks: StockData[];
  type: StockCardType;
  emptyMessage: string;
}

export const StockList: React.FC<StockListProps> = ({ title, icon, stocks, type, emptyMessage }) => {
  return (
    <section>
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">{icon}</span>
        <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
      </div>

      {stocks.length === 0 ? (
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center text-gray-500">
          <p>{emptyMessage}</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stocks.map((stock) => (
            <StockCard key={stock.ticker} stock={stock} type={type} />
          ))}
        </div>
      )}
    </section>
  );
};