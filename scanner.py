import yfinance as yf
from config import FULL_UNIVERSE

def get_top_movers(top_n=20):
    """
    สแกนหาหุ้นที่มีการเคลื่อนไหวของราคาสูงที่สุด (ทั้งขึ้นและลง)
    """
    print(f"🔍 Scanning {len(FULL_UNIVERSE)} stocks for top movers...")
    data_list = []
    
    for ticker in FULL_UNIVERSE:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if len(hist) < 2:
                continue
            
            current_vol = hist['Volume'].iloc[-1]
            avg_vol = hist['Volume'].iloc[:-1].mean()
            
            close_today = float(hist['Close'].iloc[-1])
            close_yest = float(hist['Close'].iloc[-2])
            
            pct_change = ((close_today - close_yest) / close_yest) * 100
            vol_ratio = current_vol / avg_vol if avg_vol > 0 else 0
            
            # เกณฑ์: วิ่งเกิน 1% หรือ Volume พุ่งเกิน 1.5 เท่า
            if abs(pct_change) > 1.0 or vol_ratio > 1.5:
                data_list.append({
                    "ticker": ticker,
                    "pct_change": pct_change,
                    "vol_ratio": vol_ratio,
                    "price": close_today
                })
        except Exception:
            continue

    if not data_list:
        print("⚠️ No significant movers found.")
        return []

    # คัดเลือก Top Gainers และ Top Losers
    top_gainers = sorted([x for x in data_list if x['pct_change'] > 0], key=lambda x: x['pct_change'], reverse=True)[:top_n//2]
    top_losers = sorted([x for x in data_list if x['pct_change'] < 0], key=lambda x: x['pct_change'])[:top_n//2]
    
    selected = top_gainers + top_losers
    
    # เติมให้ครบจำนวนถ้าไม่พอ
    if len(selected) < top_n:
        remaining = [x for x in data_list if x not in selected]
        selected.extend(remaining[:top_n - len(selected)])

    tickers = [s['ticker'] for s in selected]
    print(f"✅ Selected {len(tickers)} movers: {tickers}")
    return tickers