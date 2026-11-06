# AlphaBreakout Pro Scanner & F&O Engine 🚀

An institutional-grade Stock & F&O Momentum Breakout Scanner inspired by **CA Arvind Mangal (`#Chart_Sab_Kuch_Bolta_Hai`)** and **Option Edge Tamil (High-Beta F&O Momentum)**.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vigneshrece92-cmyk/pro-stock-fno-scanner)

---

## 🌟 Key Features

1. **Multi-Horizon Categorization:**
   - **Monthly Holding (Arvind Mangal Base):** 52-week / 3–12 month base consolidation breakouts with massive accumulation volume.
   - **Weekly Holding:** Multi-month consolidation breakout targeting 1:2 to 1:3 R:R.
   - **Daily / Intraday (Option Edge Tamil):** 20-day high momentum expansions with high RVOL.

2. **Complete Trade Execution Levels:**
   - **Spot Equity Levels:** Exact Entry Price, Stop Loss, Target 1, Target 2, Risk:Reward ratio.
   - **F&O Option Recommendations:** Calculated ATM/OTM Strike (e.g. `BEL 310 CE`), Option Entry Premium, Option Stop Loss, Target 1 (+45%), Target 2 (+95% Doubler).

3. **Live Interactive Candlestick Charts:**
   - Click **"View Breakout Chart"** on any stock to view interactive TradingView candlestick charts with pre-loaded **20 EMA**, **50 EMA**, **Volume**, and **RSI**.

---

## 🛠️ Deploy to Vercel (1-Click)

Click the button below to deploy this scanner directly to your Vercel account:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vigneshrece92-cmyk/pro-stock-fno-scanner)

---

## 💻 Local Development

```bash
git clone https://github.com/vigneshrece92-cmyk/pro-stock-fno-scanner.git
cd pro-stock-fno-scanner
pip install -r requirements.txt
uvicorn api.index:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
