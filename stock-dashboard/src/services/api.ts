// src/services/api.ts
import type { ApiResponse } from '../types';

const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchDailyPicks = async (): Promise<ApiResponse> => {
  const res = await fetch(`${API_BASE_URL}/get-daily-picks`);
  
  if (!res.ok) {
    throw new Error("ไม่สามารถเชื่อมต่อกับ Server ได้");
  }
  
  return await res.json();
};