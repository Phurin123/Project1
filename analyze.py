import yfinance as yf
from model_dowload import classifier

def analyze_stock_deep(ticker):
    """วิเคราะห์เชิงลึกเฉพาะหุ้นที่ถูกเลือกมาแล้ว"""
    default_result = {
        "ticker": ticker, "price": 0, "change": 0, "sentiment_score": 0,
        "final_score": 0, "recommendation": "HOLD", "reason": "Data error", "news_count": 0
    }
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if len(hist) < 2:
            return default_result
        
        current_price = float(hist['Close'].iloc[-1])
        prev_price = float(hist['Close'].iloc[-2])
        price_change_pct = ((current_price - prev_price) / prev_price) * 100
        
        news_list = stock.news[:5]
        if not news_list:
            return {
                "ticker": ticker, "price": round(current_price, 2), 
                "change": round(price_change_pct, 2), "sentiment_score": 0,
                "final_score": (price_change_pct / 2) * 0.3,
                "recommendation": "HOLD", "reason": "ไม่มีข่าวประกอบ", "news_count": 0
            }

        total_sentiment = 0
        valid_count = 0
        news_details = [] # 🔥 สร้างลิสต์ไว้เก็บข้อมูลข่าวแต่ละชิ้น

        for news in news_list:
            title = news.get('title', '')
            link = news.get('link', '')       # 🔥 ดึงลิงก์
            publisher = news.get('publisher', 'Unknown') # 🔥 ดึงชื่อสำนักข่าว
            published_at = news.get('providerPublishTime', 0)
            
            # แปลงเวลาให้เป็นรูปแบบที่อ่านง่าย (Optional)
            from datetime import datetime
            try:
                pub_date = datetime.fromtimestamp(published_at).strftime("%d/%m %H:%M")
            except:
                pub_date = ""

            if not title:
                continue
            
            try:
                res = classifier(title)[0]
                label = res['label'].lower()
                score = float(res['score'])
                
                val = score if label == 'positive' else (-score if label == 'negative' else 0)
                total_sentiment += val
                valid_count += 1
                
                # 🔥 เก็บข้อมูลข่าวลงลิสต์
                news_details.append({
                    "title": title,
                    "link": link,
                    "publisher": publisher,
                    "date": pub_date,
                    "sentiment": label
                })
            except:
                continue
        
        avg_sentiment = total_sentiment / valid_count if valid_count > 0 else 0
        
        # Logic การให้คะแนน
        price_factor = max(-1, min(1, price_change_pct / 2))
        final_score = (avg_sentiment * 0.6) + (price_factor * 0.4)
        
        action = "HOLD"
        reason = "สัญญาณผสมผสาน ระวังความผันผวน"
        
        if final_score > 0.3:
            action = "BUY 🟢"
            reason = "ข่าวบวกสอดคล้องกับราคาที่กำลังพุ่ง"
        elif final_score < -0.3:
            action = "SELL 🔴"
            reason = "ข่าวลบยืนยันแนวโน้มขาลง"
            
        return {
            "ticker": ticker,
            "price": round(current_price, 2),
            "change": round(price_change_pct, 2),
            "sentiment_score": round(avg_sentiment, 3),
            "final_score": round(final_score, 3),
            "recommendation": action,
            "reason": reason,
            "news_count": valid_count,
            "news_list": news_details  # 🔥 ส่งลิสต์ข่าวกลับไปด้วย!
    }
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        default_result["reason"] = str(e)
        return default_result