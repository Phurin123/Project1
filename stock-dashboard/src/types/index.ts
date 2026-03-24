// src/types/index.ts

// ✅ 1. เพิ่ม Type สำหรับข่าวตรงนี้
export type NewsItem = {
  title: string;
  link: string;
  publisher: string;
  date: string;
  sentiment: string;
};

// 2. อัปเดต StockData ให้มี news_list
export type StockData = {
  ticker: string;
  price: number;
  change: number;
  sentiment_score: number;
  final_score: number;
  recommendation: string;
  reason: string;
  news_count: number;
  news_list?: NewsItem[]; // ใช้ ? เพราะอาจจะมีหรือไม่มีก็ได้
};

export type ApiResponse = {
  date: string;
  market_status: string;
  top_picks: StockData[];
  warning_list: StockData[];
  all_stocks: StockData[];
  error?: string;
  message?: string;
};

export type StockCardType = 'buy' | 'sell';