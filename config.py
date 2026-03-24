import mysql.connector

# 🔥 รายชื่อหุ้นสำหรับสแกน (Universe)
UNIVERSE_US = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "V", "JNJ",
    "WMT", "JPM", "MA", "PG", "UNH", "HD", "CVX", "MRK", "ABBV", "KO",
    "PEP", "COST", "AVGO", "TMO", "MCD", "CSCO", "ACN", "ABT", "LLY", "ADBE",
    "TXN", "DHR", "NEE", "BMY", "PM", "RTX", "QCOM", "HON", "UPS", "LOW",
    "AMD", "SBUX", "INTC", "BA", "GE", "CAT", "DE", "GS", "BLK", "GILD"
]

UNIVERSE_TH = [
    "PTT.BK", "AOT.BK", "KBANK.BK", "GULF.BK", "CPALL.BK", "SCB.BK", "BBL.BK",
    "ADVANC.BK", "TRUE.BK", "DELTA.BK", "HANA.BK", "IVL.BK", "PTTEP.BK", "BDMS.BK",
    "CRC.BK", "TU.BK", "SCC.BK", "INTUCH.BK", "BANPU.BK", "STA.BK", "GPSC.BK",
    "OR.BK", "AWC.BK", "CENTEL.BK", "MINT.BK", "SAWAD.BK", "TIDLOR.BK", "AEONTS.BK"
]

FULL_UNIVERSE = UNIVERSE_US + UNIVERSE_TH

# 🔥 การเชื่อมต่อ Database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "stock_ai"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS stock_ai")
        cursor.execute("USE stock_ai")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_analysis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(20),
            price FLOAT,
            change_pct FLOAT,
            sentiment_score FLOAT,
            final_score FLOAT,
            recommendation VARCHAR(20),
            reason TEXT,
            news_count INT,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized.")
    except Exception as e:
        print(f"❌ DB Init Error: {e}")
        
def cleanup_old_data(days_to_keep=7):
    """ลบข้อมูลที่เก่าเกินกว่าที่กำหนด (ค่าเริ่มต้นเก็บไว้ 7 วัน)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ลบข้อมูลที่ created_at เก่ากว่า X วัน
        sql = f"DELETE FROM daily_analysis WHERE analyzed_at < NOW() - INTERVAL {days_to_keep} DAY"
        cursor.execute(sql)
        conn.commit()
        
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            print(f"🧹 ลบข้อมูลเก่าแล้ว {deleted_rows} รายการ (เก็บไว้แค่ {days_to_keep} วัน)")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error cleaning up data: {e}")

