import React from 'react';
import type { StockData } from '../../types';
import { Badge } from '../UI/Badge';
import { ProgressBar } from '../UI/ProgressBar';

interface StockTableProps {
  stocks: StockData[];
}

export const StockTable: React.FC<StockTableProps> = ({ stocks }) => {
  const getBadgeType = (rec: string): 'buy' | 'sell' | 'hold' => {
    if (rec.includes('BUY')) return 'buy';
    if (rec.includes('SELL')) return 'sell';
    return 'hold';
  };

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-4 bg-gray-50 border-b border-gray-100">
        <h3 className="font-bold text-gray-700">สรุปข้อมูลทุกหุ้นที่ติดตาม</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 text-gray-500">
            <tr>
              <th className="p-3 font-medium">หุ้น</th>
              <th className="p-3 font-medium">ราคา</th>
              <th className="p-3 font-medium">เปลี่ยนแปลง</th>
              <th className="p-3 font-medium">Sentiment</th>
              <th className="p-3 font-medium">คำแนะนำ</th>
              <th className="p-3 font-medium hidden md:table-cell">เหตุผล</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {stocks.map((stock) => (
              <tr key={stock.ticker} className="hover:bg-gray-50 transition-colors">
                <td className="p-3 font-bold text-gray-900">{stock.ticker}</td>
                <td className="p-3 font-mono">${stock.price}</td>
                <td className={`p-3 font-medium ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {stock.change > 0 ? '+' : ''}{stock.change}%
                </td>
                <td className="p-3">
                  <ProgressBar value={stock.sentiment_score} />
                </td>
                <td className="p-3">
                  <Badge text={stock.recommendation.split(' ')[0]} type={getBadgeType(stock.recommendation)} />
                </td>
                <td className="p-3 text-gray-600 hidden md:table-cell max-w-xs truncate" title={stock.reason}>
                  {stock.reason}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};