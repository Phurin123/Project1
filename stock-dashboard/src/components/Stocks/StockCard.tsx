import React from 'react';
import type { StockData, StockCardType } from '../../types';

interface StockCardProps {
  stock: StockData;
  type: StockCardType;
}

export const StockCard: React.FC<StockCardProps> = ({ stock, type }) => {
  const isBuy = type === 'buy';
  const borderColor = isBuy ? 'border-green-500' : 'border-red-500';
  const changeColor = stock.change >= 0 ? 'text-green-700 bg-green-50' : 'text-red-700 bg-red-50';

  return (
    <div className={`group relative p-5 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 border-t-4 ${borderColor} bg-white hover:-translate-y-1 flex flex-col`}>
      {/* ส่วนหัว (Header) */}
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-extrabold text-gray-900 tracking-tight">{stock.ticker}</h3>
        <span className={`text-sm font-bold px-2 py-1 rounded-md ${changeColor}`}>
          {stock.change > 0 ? '+' : ''}{stock.change}%
        </span>
      </div>
      
      <div className="text-3xl font-bold text-gray-900 mb-3">${stock.price}</div>
      
      <p className="text-sm text-gray-600 mb-4 leading-relaxed min-h-[3rem]">
        {stock.reason}
      </p>
      
      {/* 🔥 ส่วนแสดงรายการข่าว (News List) */}
      {stock.news_list && stock.news_list.length > 0 && (
        <div className="mt-auto pt-4 border-t border-gray-100">
          <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">
            ข่าวล่าสุด ({stock.news_list.length})
          </p>
          <ul className="space-y-2">
            {stock.news_list.map((news, idx) => (
              <li key={idx} className="text-sm">
                <a 
                  href={news.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="block group/link"
                >
                  <div className="flex items-start gap-2">
                    <span className={`mt-1.5 w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                      news.sentiment === 'positive' ? 'bg-green-500' : 
                      news.sentiment === 'negative' ? 'bg-red-500' : 'bg-gray-400'
                    }`} />
                    <div>
                      <p className="text-gray-700 font-medium group-hover/link:text-blue-600 group-hover/link:underline transition-colors line-clamp-2">
                        {news.title}
                      </p>
                      <p className="text-xs text-gray-400 mt-0.5">
                        {news.publisher} • {news.date}
                      </p>
                    </div>
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ส่วนคะแนน (Footer) */}
      <div className="pt-3 mt-3 border-t border-gray-100 flex justify-between items-center text-xs text-gray-400">
        <span>วิเคราะห์: {stock.news_count} ข่าว</span>
        <span className={`font-mono font-semibold ${stock.final_score > 0 ? 'text-green-600' : 'text-red-600'}`}>
          Score: {stock.final_score.toFixed(2)}
        </span>
      </div>
    </div>
  );
};