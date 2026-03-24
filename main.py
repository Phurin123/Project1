from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from datetime import datetime

from config import get_db_connection, init_db
from scanner import get_top_movers
from analyze import analyze_stock_deep

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# เริ่มต้นฐานข้อมูลเมื่อเปิดโปรแกรม
init_db()


def process_market_smart():
    print("--- 🚀 Starting Smart Market Scan ---")

    # 1. คัดกรองหา Top Movers (จาก scanner.py)
    target_tickers = get_top_movers(top_n=20)

    if not target_tickers:
        print("No stocks to analyze.")
        return []

    results = []
    for ticker in target_tickers:
        print(f"Analyzing deep: {ticker}...")
        # 2. วิเคราะห์เชิงลึก (จาก analyzer.py)
        data = analyze_stock_deep(ticker)

        if "final_score" in data:
            results.append(data)

            # บันทึกลง DB
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                sql = """INSERT INTO daily_analysis 
                         (ticker, price, change_pct, sentiment_score, final_score, recommendation, reason, news_count) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(
                    sql,
                    (
                        data["ticker"],
                        data["price"],
                        data["change"],
                        data["sentiment_score"],
                        data["final_score"],
                        data["recommendation"],
                        data["reason"],
                        data["news_count"],
                    ),
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as db_err:
                print(f"DB Save Error: {db_err}")

    results.sort(key=lambda x: x["final_score"], reverse=True)
    print(f"--- ✅ Analysis Complete. Found {len(results)} stocks. ---")
    return results


@app.get("/get-daily-picks")
def get_daily_picks():
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # หาเวลาวิเคราะห์ล่าสุด
        cur.execute("SELECT MAX(analyzed_at) as last_run FROM daily_analysis")
        last_run_row = cur.fetchone()
        last_run = last_run_row["last_run"] if last_run_row else None

        data = []

        # ถ้ามีข้อมูลไม่เกิน 1 ชม. ให้ใช้ข้อมูลเก่า
        if last_run and (datetime.now() - last_run).total_seconds() < 3600:
            print("Using cached data from DB...")
            cur.execute(
                """
                SELECT * FROM daily_analysis 
                WHERE analyzed_at = %s 
                ORDER BY final_score DESC
            """,
                (last_run,),
            )
            rows = cur.fetchall()

            for row in rows:
                row["price"] = float(row["price"])
                row["change"] = float(row["change_pct"])
                row["sentiment_score"] = float(row["sentiment_score"])
                row["final_score"] = float(row["final_score"])
                row["news_count"] = int(row["news_count"])
                row["change"] = row.pop("change_pct")  # Rename ให้ตรงกับ Frontend
            data = rows
        else:
            print("Data expired. Running new analysis...")
            cur.close()
            conn.close()
            data = process_market_smart()

        cur.close()
        conn.close()

        # จัดกลุ่มข้อมูล
        buys = [s for s in data if "BUY" in s.get("recommendation", "")]
        sells = [s for s in data if "SELL" in s.get("recommendation", "")]

        market_status = "ปกติ"
        if len(buys) > len(sells) * 1.5:
            market_status = "ตลาดกระทิง (Bullish) 🐂"
        elif len(sells) > len(buys) * 1.5:
            market_status = "ตลาดหมี (Bearish) 🐻"

        return {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "market_status": market_status,
            "top_picks": buys[:5],
            "warning_list": sells[:5],
            "all_stocks": data,
        }

    except Exception as e:
        print(f"API Error: {e}")
        return {"error": str(e), "message": "Fallback mode"}


@app.get("/force-refresh")
def force_refresh():
    """บังคับวิเคราะห์ใหม่ทันที"""
    data = process_market_smart()
    return {"message": "Analysis completed", "data": data}


@app.get("/")
def home():
    return {"message": "Stock AI Server Ready"}


# รัน Background Thread
def auto_scan_loop():
    while True:
        process_market_smart()
        time.sleep(3600)


threading.Thread(target=auto_scan_loop, daemon=True).start()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
