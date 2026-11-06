import datetime
import math
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import yfinance as yf

app = FastAPI(title="AlphaBreakout Pro Scanner")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# High-liquidity NSE F&O Universe
FO_SYMBOLS = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "BHARTIARTL",
    "TATAMOTORS", "TATASTEEL", "JSWSTEEL", "VEDL", "HINDALCO", "COALINDIA",
    "ONGC", "NTPC", "POWERGRID", "BEL", "HAL", "BHEL", "PFC", "RECLTD",
    "CANBK", "PNB", "BANKBARODA", "DLF", "GODREJPROP", "SUNPHARMA", "CIPLA",
    "DRREDDY", "DIVISLAB", "LTIM", "TECHM", "WIPRO", "TITAN", "ASIANPAINT",
    "BAJFINANCE", "BAJAJFINSV", "MARUTI", "M&M", "HEROMOTOCO", "EICHERMOT",
    "CHOLAFIN", "SHRIRAMFIN", "POLYCAB", "DIXON", "TRENT", "PERSISTENT",
    "COFORGE", "FEDERALBNK", "AUROPHARMA", "KOTAKBANK", "AXISBANK", "ADANIENT",
    "ADANIPORTS", "INDUSINDBK", "APOLLOHOSP", "LT", "SIEMENS", "ABB"
]

def get_strike_step(price: float) -> int:
    """Determines accurate NSE option strike interval based on stock price."""
    if price < 150:
        return 2
    elif price < 300:
        return 5
    elif price < 600:
        return 10
    elif price < 1200:
        return 20
    elif price < 2500:
        return 50
    elif price < 5000:
        return 100
    else:
        return 200

def estimate_option_pricing(spot_price: float, strike_price: float, spot_sl: float, spot_tgt1: float, spot_tgt2: float):
    """
    Simulates realistic ATM/Slight OTM monthly option pricing and target levels
    using delta ~0.50 (ATM) and volatility assumptions.
    """
    strike_diff = spot_price - strike_price
    # Baseline estimated monthly ATM premium (~3.0% to 3.8% of spot price)
    base_atm_premium = spot_price * 0.034
    
    # Intrinsic + Time value estimate
    est_call_entry = max(round(base_atm_premium + (strike_diff * 0.5), 1), spot_price * 0.015)
    
    # Delta risk transmission
    spot_risk = max(spot_price - spot_sl, spot_price * 0.015)
    option_sl = round(max(est_call_entry - (spot_risk * 0.45), est_call_entry * 0.65), 1)
    
    # Target calculations (+40-50% on Tgt 1, +90-120% on Tgt 2)
    spot_move_tgt1 = spot_tgt1 - spot_price
    spot_move_tgt2 = spot_tgt2 - spot_price
    
    option_tgt1 = round(est_call_entry + (spot_move_tgt1 * 0.52), 1)
    option_tgt2 = round(est_call_entry + (spot_move_tgt2 * 0.68), 1)
    
    return {
        "strike": f"{int(strike_price)} CE",
        "entry": est_call_entry,
        "sl": option_sl,
        "tgt1": option_tgt1,
        "tgt2": option_tgt2,
        "rr": round((option_tgt1 - est_call_entry) / max(est_call_entry - option_sl, 0.1), 1)
    }

def run_multi_horizon_screener():
    tickers = [f"{s}.NS" for s in FO_SYMBOLS]
    try:
        data = yf.download(tickers, period="1y", interval="1d", group_by="ticker", progress=False)
    except Exception:
        return []

    screened_cards = []

    for sym in FO_SYMBOLS:
        ticker = f"{sym}.NS"
        try:
            if ticker not in data.columns.levels[0]:
                continue
            df = data[ticker].dropna()
            if len(df) < 100:
                continue

            close = df['Close']
            high = df['High']
            low = df['Low']
            volume = df['Volume']

            cmp = float(close.iloc[-1])
            curr_vol = float(volume.iloc[-1])
            avg_vol_20 = float(volume.iloc[-21:-1].mean())
            rvol = round(curr_vol / avg_vol_20, 2) if avg_vol_20 > 0 else 1.0

            # Technicals
            ema20 = float(close.ewm(span=20, adjust=False).mean().iloc[-1])
            ema50 = float(close.ewm(span=50, adjust=False).mean().iloc[-1])

            # RSI(14)
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = float((100 - (100 / (1 + rs))).iloc[-1])

            # Reference Pivots
            prev_20_high = float(high.iloc[-21:-1].max())
            prev_60_high = float(high.iloc[-61:-1].max())
            prev_200_high = float(high.iloc[-201:-1].max()) if len(df) >= 200 else prev_60_high

            # Filter Strategy:
            # 1. Trend alignment
            is_uptrend = cmp > ema20 and ema20 > ema50
            if not is_uptrend or rsi < 58:
                continue

            # Classify Horizons
            horizon = None
            setup_name = ""

            if cmp >= prev_200_high and rvol >= 1.6:
                horizon = "Monthly Holding"
                setup_name = "Multi-Year / 52W Base Breakout (Arvind Mangal)"
                sl = round(min(float(low.iloc[-1]), ema50), 2)
                tgt1 = round(cmp + (cmp - sl) * 2.0, 2)
                tgt2 = round(cmp + (cmp - sl) * 3.5, 2)

            elif cmp >= prev_60_high and rvol >= 1.4:
                horizon = "Weekly Holding"
                setup_name = "Multi-Month Consolidation Breakout"
                sl = round(min(float(low.iloc[-2:].min()), ema20), 2)
                tgt1 = round(cmp + (cmp - sl) * 1.6, 2)
                tgt2 = round(cmp + (cmp - sl) * 2.8, 2)

            elif cmp >= prev_20_high and rvol >= 1.2:
                horizon = "Daily / Intraday"
                setup_name = "High-Beta Momentum Surge (Option Edge)"
                sl = round(float(low.iloc[-1]), 2)
                tgt1 = round(cmp + (cmp - sl) * 1.4, 2)
                tgt2 = round(cmp + (cmp - sl) * 2.2, 2)
            else:
                continue

            # Calculate Option Strike and Premiums
            step = get_strike_step(cmp)
            atm_strike = round(cmp / step) * step
            option_data = estimate_option_pricing(cmp, atm_strike, sl, tgt1, tgt2)

            risk = cmp - sl
            reward1 = tgt1 - cmp
            rr_ratio = f"1:{round(reward1 / max(risk, 0.1), 1)}"

            screened_cards.append({
                "symbol": sym,
                "cmp": round(cmp, 2),
                "horizon": horizon,
                "setup_name": setup_name,
                "rsi": round(rsi, 1),
                "rvol": rvol,
                "stock_trade": {
                    "entry": round(cmp, 2),
                    "sl": sl,
                    "tgt1": tgt1,
                    "tgt2": tgt2,
                    "rr": rr_ratio,
                    "potential_pct": f"+{round(((tgt1 - cmp) / cmp) * 100, 1)}% / +{round(((tgt2 - cmp) / cmp) * 100, 1)}%"
                },
                "option_trade": option_data
            })
        except Exception:
            continue

    return screened_cards

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    recommendations = run_multi_horizon_screener()
    now_str = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p IST")
    
    # Metrics
    total_found = len(recommendations)
    monthly_count = sum(1 for x in recommendations if x['horizon'] == 'Monthly Holding')
    weekly_count = sum(1 for x in recommendations if x['horizon'] == 'Weekly Holding')
    daily_count = sum(1 for x in recommendations if x['horizon'] == 'Daily / Intraday')

    return templates.TemplateResponse("index.html", {
        "request": request,
        "cards": recommendations,
        "timestamp": now_str,
        "metrics": {
            "total": total_found,
            "monthly": monthly_count,
            "weekly": weekly_count,
            "daily": daily_count
        }
    })

@app.get("/api/scan")
async def scan_json():
    return {"status": "success", "data": run_multi_horizon_screener()}
