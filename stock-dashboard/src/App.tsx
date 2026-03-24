import { useEffect, useState } from "react";
import type { ApiResponse } from "./types";
import { fetchDailyPicks } from "./services/api";

// Layout Components
import { Header } from "./components/Layout/Header";
import { LoadingScreen } from "./components/Layout/LoadingScreen";

// Stock Components
import { StockList } from "./components/Stocks/StockList";
import { StockTable } from "./components/Stocks/StockTable";

function App() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchDailyPicks();
      if (result.error) {
        throw new Error(result.error || "เกิดข้อผิดพลาดจากเซิร์ฟเวอร์");
      }
      setData(result);
    } catch (err: any) {
      console.error("Error fetching data:", err);
      setError(err.message || "เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // แสดงหน้าจอโหลด หรือ ข้อผิดพลาด
  if (loading || (!data && !error)) {
    return <LoadingScreen error={error} onRetry={loadData} />;
  }

  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 font-sans text-gray-800">
      
      <Header 
        date={data.date}
        marketStatus={data.market_status}
        onRefresh={loadData}
        isLoading={loading}
      />

      <main className="max-w-6xl mx-auto space-y-10">
        
        <StockList 
          title="หุ้นน่าสนใจวันนี้ (Buy)"
          icon="🟢"
          stocks={data.top_picks}
          type="buy"
          emptyMessage="วันนี้ยังไม่มีหุ้นที่มีสัญญาณซื้อชัดเจนจาก AI"
        />

        <StockList 
          title="หุ้นที่ควรระวัง (Sell/Avoid)"
          icon="🔴"
          stocks={data.warning_list}
          type="sell"
          emptyMessage="ไม่มีหุ้นที่มีสัญญาณขายรุนแรงในขณะนี้"
        />

        <StockTable stocks={data.all_stocks} />

      </main>
    </div>
  );
}

export default App;