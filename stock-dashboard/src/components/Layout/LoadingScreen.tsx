import React from 'react';

interface LoadingScreenProps {
  error: string | null;
  onRetry: () => void;
}

export const LoadingScreen: React.FC<LoadingScreenProps> = ({ error, onRetry }) => {
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="bg-red-50 text-red-700 p-6 rounded-xl shadow-md max-w-md text-center border border-red-200">
          <h2 className="text-xl font-bold mb-2">⚠️ เกิดข้อผิดพลาด</h2>
          <p className="mb-4">{error}</p>
          <button onClick={onRetry} className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700">
            ลองใหม่อีกครั้ง
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600 font-medium">กำลังวิเคราะห์ตลาด...</p>
      </div>
    </div>
  );
};