import React from 'react';

interface HeaderProps {
  date: string;
  marketStatus: string;
  onRefresh: () => void;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({ date, marketStatus, onRefresh, isLoading }) => {
  const getStatusColor = (status: string) => {
    if (status.includes('Bullish')) return 'bg-green-100 text-green-800';
    if (status.includes('Bearish')) return 'bg-red-100 text-red-800';
    return 'bg-blue-100 text-blue-800';
  };

  return (
    <header className="max-w-6xl mx-auto mb-8 text-center">
      <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">
        📈 Daily Stock Picks
      </h1>
      <p className="text-gray-500 mb-4">AI วิเคราะห์แนวโน้มจากข่าวและราคา ({date})</p>
      
      <div className="flex flex-col md:flex-row justify-center items-center gap-4">
        <span className={`px-4 py-1.5 rounded-full text-sm font-bold shadow-sm ${getStatusColor(marketStatus)}`}>
          สถานะตลาด: {marketStatus}
        </span>
        
        <button 
          onClick={onRefresh} 
          disabled={isLoading}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium hover:underline disabled:opacity-50"
        >
          {isLoading ? 'กำลังโหลด...' : '🔄 รีเฟรชข้อมูล'}
        </button>
      </div>
    </header>
  );
};