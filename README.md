# 📈 Stock AI Sentiment Analysis Dashboard

ระบบวิเคราะห์แนวโน้มหุ้นอัจฉริยะด้วยการประมวลผลภาษาธรรมชาติ (NLP) เพื่อประเมินความรู้สึกจากข่าวสารทางการเงินและข้อมูลราคาแบบเรียลไทม์ ช่วยให้นักลงทุนตัดสินใจได้แม่นยำยิ่งขึ้นด้วยข้อมูลเชิงลึกจาก AI

## ✨ คุณสมบัติหลัก

-   **🤖 AI-Powered Sentiment Analysis:** ใช้โมเดล Machine Learning (Transformers) วิเคราะห์พาดหัวข่าวจากแหล่งข่าวชั้นนำ (Reuters, Bloomberg, CNBC ฯลฯ) เพื่อระบุว่าเป็นข่าวบวก, ลบ หรือกลาง
-   **🔍 Smart Stock Scanner:** สแกนหุ้นกว่า 80+ ตัว (ทั้งสหรัฐฯ และไทย) คัดกรองเฉพาะหุ้นที่มีความเคลื่อนไหวของราคาและวอลุ่มผิดปกติ (Top Movers) เพื่อนำมาวิเคราะห์เชิงลึก
-   **📊 Real-time Data Integration:** ดึงข้อมูลราคาและข่าวล่าสุดจาก Yahoo Finance ผ่าน `yfinance`
-   **🎯 Actionable Recommendations:** ให้คำแนะนำการลงทุนแบบชัดเจน (BUY 🟢, SELL 🔴, HOLD 🟡) พร้อมเหตุผลประกอบโดยผสมผสานระหว่างSentiment Score และแนวโน้มราคา
-   **💻 Modern Full-Stack Architecture:**
    -   **Backend:** FastAPI (Python) รวดเร็วและรองรับการทำงานแบบ Asynchronous
    -   **Frontend:** React + TypeScript + Tailwind CSS ออกแบบให้สวยงามและตอบสนองทุกอุปกรณ์ (Responsive)
    -   **Database:** MySQL สำหรับเก็บประวัติการวิเคราะห์และทำ Caching

## 🏗️ โครงสร้างโปรเจกต์

```text
Project1/
├── main.py              # จุดเริ่มต้นของ FastAPI Server
├── config.py            # การตั้งค่า Database และรายชื่อหุ้น (Universe)
├── scanner.py           # โลจิกการคัดกรองหุ้นที่น่าสนใจ (Top Movers)
├── analyzer.py          # โลจิกการวิเคราะห์ข่าวด้วย AI
├── model_dowload.py     # โหลดโมเดล Classifier
├── src/                 # โค้ดส่วน Frontend (React)
│   ├── components/      # UI Components แยกส่วน
│   ├── services/        # API Services
│   ├── types/           # TypeScript Definitions
│   └── App.tsx          # หน้าหลัก
├── .env                 # ไฟล์เก็บความลับ (รหัสผ่าน DB, API Keys) *ไม่ควรรวมใน Git*
└── README.md
