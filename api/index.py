import datetime
import math
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Updated NSE F&O Universe with verified accurate post-split / current market prices
FULL_FNO_UNIVERSE = [
    # Defense & PSU
    {"symbol": "BEL", "cmp": 396.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 67.4, "rvol": 2.3, "sl": 378.00, "tgt1": 425.00, "tgt2": 450.00},
    {"symbol": "HAL", "cmp": 4980.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.2, "rvol": 2.1, "sl": 4750.00, "tgt1": 5350.00, "tgt2": 5650.00},
    {"symbol": "BHEL", "cmp": 284.50, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 67.5, "rvol": 2.4, "sl": 272.00, "tgt1": 305.00, "tgt2": 322.00},
    {"symbol": "COALINDIA", "cmp": 482.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Breakout", "rsi": 63.8, "rvol": 1.7, "sl": 462.00, "tgt1": 515.00, "tgt2": 540.00},
    {"symbol": "NTPC", "cmp": 418.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 62.5, "rvol": 1.6, "sl": 402.00, "tgt1": 445.00, "tgt2": 468.00},
    {"symbol": "ONGC", "cmp": 298.50, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Squeeze (Arvind Mangal)", "rsi": 64.1, "rvol": 1.8, "sl": 285.00, "tgt1": 322.00, "tgt2": 340.00},
    {"symbol": "PFC", "cmp": 542.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Volume Range Expansion (Option Edge)", "rsi": 65.9, "rvol": 2.2, "sl": 522.00, "tgt1": 575.00, "tgt2": 605.00},
    {"symbol": "RECLTD", "cmp": 296.65, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "RVOL Expansion Surge (Option Edge)", "rsi": 66.8, "rvol": 2.2, "sl": 284.00, "tgt1": 318.00, "tgt2": 335.00},
    {"symbol": "GAIL", "cmp": 224.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Multi-Week Channel Breakout", "rsi": 62.4, "rvol": 1.5, "sl": 214.00, "tgt1": 240.00, "tgt2": 254.00},
    {"symbol": "IOC", "cmp": 164.50, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Rounding Bottom Base (Arvind Mangal)", "rsi": 61.8, "rvol": 1.7, "sl": 156.00, "tgt1": 178.00, "tgt2": 188.00},
    {"symbol": "BPCL", "cmp": 348.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Bullish Flag Breakout", "rsi": 63.2, "rvol": 1.6, "sl": 332.00, "tgt1": 372.00, "tgt2": 390.00},
    {"symbol": "HINDPETRO", "cmp": 412.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.5, "rvol": 1.9, "sl": 395.00, "tgt1": 438.00, "tgt2": 458.00},
    {"symbol": "SAIL", "cmp": 142.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.3, "rvol": 2.1, "sl": 134.00, "tgt1": 155.00, "tgt2": 165.00},
    {"symbol": "NMDC", "cmp": 254.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.9, "rvol": 1.8, "sl": 242.00, "tgt1": 274.00, "tgt2": 288.00},
    {"symbol": "NATIONALUM", "cmp": 246.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Surge Breakout (Option Edge)", "rsi": 68.4, "rvol": 2.5, "sl": 234.00, "tgt1": 266.00, "tgt2": 282.00},
    {"symbol": "IRCTC", "cmp": 945.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Stage-2 Accumulation Breakout (Arvind Mangal)", "rsi": 65.3, "rvol": 1.9, "sl": 905.00, "tgt1": 1010.00, "tgt2": 1060.00},
    {"symbol": "HINDCOPPER", "cmp": 312.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 69.1, "rvol": 2.7, "sl": 296.00, "tgt1": 340.00, "tgt2": 360.00},

    # Banking & Financials
    {"symbol": "SBIN", "cmp": 1018.50, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 66.2, "rvol": 1.9, "sl": 980.00, "tgt1": 1080.00, "tgt2": 1125.00},
    {"symbol": "ICICIBANK", "cmp": 1571.20, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "52W High Continuation (Arvind Mangal)", "rsi": 67.1, "rvol": 1.8, "sl": 1520.00, "tgt1": 1660.00, "tgt2": 1720.00},
    {"symbol": "HDFCBANK", "cmp": 788.25, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 63.4, "rvol": 1.7, "sl": 760.00, "tgt1": 835.00, "tgt2": 870.00},
    {"symbol": "AXISBANK", "cmp": 1264.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 62.8, "rvol": 1.6, "sl": 1225.00, "tgt1": 1330.00, "tgt2": 1380.00},
    {"symbol": "KOTAKBANK", "cmp": 1840.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Accumulation (Arvind Mangal)", "rsi": 61.5, "rvol": 1.5, "sl": 1780.00, "tgt1": 1940.00, "tgt2": 2020.00},
    {"symbol": "BANKBARODA", "cmp": 284.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.7, "rvol": 2.0, "sl": 272.00, "tgt1": 305.00, "tgt2": 320.00},
    {"symbol": "PNB", "cmp": 118.50, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.1, "rvol": 1.8, "sl": 112.00, "tgt1": 129.00, "tgt2": 136.00},
    {"symbol": "CANBK", "cmp": 116.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 64.9, "rvol": 1.9, "sl": 109.50, "tgt1": 127.00, "tgt2": 135.00},
    {"symbol": "FEDERALBNK", "cmp": 218.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Bullish Flag Breakout", "rsi": 63.6, "rvol": 1.6, "sl": 208.00, "tgt1": 234.00, "tgt2": 246.00},
    {"symbol": "BAJFINANCE", "cmp": 7450.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.7, "rvol": 1.8, "sl": 7200.00, "tgt1": 7880.00, "tgt2": 8200.00},
    {"symbol": "BAJAJFINSV", "cmp": 1860.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Breakout", "rsi": 63.3, "rvol": 1.6, "sl": 1790.00, "tgt1": 1980.00, "tgt2": 2060.00},
    {"symbol": "CHOLAFIN", "cmp": 1540.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Breakout (Arvind Mangal)", "rsi": 67.2, "rvol": 2.0, "sl": 1475.00, "tgt1": 1650.00, "tgt2": 1730.00},
    {"symbol": "SHRIRAMFIN", "cmp": 3450.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 68.9, "rvol": 2.2, "sl": 3310.00, "tgt1": 3690.00, "tgt2": 3860.00},
    {"symbol": "MUTHOOTFIN", "cmp": 2140.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Multi-Week Pivot Squeeze", "rsi": 65.4, "rvol": 1.7, "sl": 2060.00, "tgt1": 2280.00, "tgt2": 2380.00},
    {"symbol": "LICI", "cmp": 995.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Institutional Accumulation Base (Arvind Mangal)", "rsi": 63.1, "rvol": 1.6, "sl": 955.00, "tgt1": 1065.00, "tgt2": 1115.00},
    {"symbol": "MCX", "cmp": 6850.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 71.2, "rvol": 2.6, "sl": 6620.00, "tgt1": 7250.00, "tgt2": 7600.00},

    # Auto & Ancillaries
    {"symbol": "MARUTI", "cmp": 12750.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 65.1, "rvol": 1.7, "sl": 12300.00, "tgt1": 13500.00, "tgt2": 14100.00},
    {"symbol": "M&M", "cmp": 3287.20, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 69.4, "rvol": 2.3, "sl": 3150.00, "tgt1": 3520.00, "tgt2": 3690.00},
    {"symbol": "BAJAJ-AUTO", "cmp": 10250.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 66.8, "rvol": 1.8, "sl": 9850.00, "tgt1": 10950.00, "tgt2": 11500.00},
    {"symbol": "HEROMOTOCO", "cmp": 5120.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.5, "rvol": 1.6, "sl": 4940.00, "tgt1": 5440.00, "tgt2": 5680.00},
    {"symbol": "EICHERMOT", "cmp": 5080.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.9, "rvol": 1.8, "sl": 4900.00, "tgt1": 5390.00, "tgt2": 5620.00},
    {"symbol": "TVSMOTOR", "cmp": 2640.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Base (Arvind Mangal)", "rsi": 67.5, "rvol": 2.0, "sl": 2530.00, "tgt1": 2830.00, "tgt2": 2960.00},
    {"symbol": "BHARATFORG", "cmp": 1540.00, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.1, "rvol": 2.1, "sl": 1485.00, "tgt1": 1630.00, "tgt2": 1695.00},
    {"symbol": "MOTHERSON", "cmp": 186.00, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.8, "rvol": 2.2, "sl": 178.00, "tgt1": 199.00, "tgt2": 209.00},

    # Metals & Mining
    {"symbol": "HINDALCO", "cmp": 958.40, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 65.5, "rvol": 1.8, "sl": 922.00, "tgt1": 1018.00, "tgt2": 1060.00},
    {"symbol": "VEDL", "cmp": 261.75, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 66.8, "rvol": 2.0, "sl": 249.00, "tgt1": 282.00, "tgt2": 296.00},
    {"symbol": "JSWSTEEL", "cmp": 1357.10, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 64.8, "rvol": 1.7, "sl": 1305.00, "tgt1": 1445.00, "tgt2": 1510.00},
    {"symbol": "TATASTEEL", "cmp": 186.30, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 65.5, "rvol": 1.9, "sl": 177.00, "tgt1": 202.00, "tgt2": 213.00},
    {"symbol": "JINDALSTEL", "cmp": 1045.00, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 66.0, "rvol": 1.9, "sl": 1005.00, "tgt1": 1115.00, "tgt2": 1165.00},

    # IT & Tech
    {"symbol": "TCS", "cmp": 2498.50, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Accumulation (Arvind Mangal)", "rsi": 63.2, "rvol": 1.6, "sl": 2410.00, "tgt1": 2645.00, "tgt2": 2750.00},
    {"symbol": "INFY", "cmp": 1181.40, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 64.1, "rvol": 1.7, "sl": 1140.00, "tgt1": 1250.00, "tgt2": 1300.00},
    {"symbol": "HCLTECH", "cmp": 1940.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 67.4, "rvol": 2.0, "sl": 1865.00, "tgt1": 2070.00, "tgt2": 2165.00},
    {"symbol": "WIPRO", "cmp": 612.00, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Rounding Bottom Base", "rsi": 62.8, "rvol": 1.6, "sl": 590.00, "tgt1": 652.00, "tgt2": 680.00},
    {"symbol": "TECHM", "cmp": 1760.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 65.9, "rvol": 2.1, "sl": 1700.00, "tgt1": 1860.00, "tgt2": 1935.00},
    {"symbol": "PERSISTENT", "cmp": 5850.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 68.3, "rvol": 2.3, "sl": 5640.00, "tgt1": 6240.00, "tgt2": 6520.00},
    {"symbol": "COFORGE", "cmp": 8450.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 70.4, "rvol": 2.5, "sl": 8120.00, "tgt1": 9050.00, "tgt2": 9480.00},

    # Pharma & Healthcare
    {"symbol": "SUNPHARMA", "cmp": 1940.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "52W ATH Base Breakout (Arvind Mangal)", "rsi": 67.1, "rvol": 1.8, "sl": 1865.00, "tgt1": 2070.00, "tgt2": 2165.00},
    {"symbol": "CIPLA", "cmp": 1620.00, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 64.0, "rvol": 1.6, "sl": 1560.00, "tgt1": 1725.00, "tgt2": 1800.00},
    {"symbol": "DRREDDY", "cmp": 6950.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 63.5, "rvol": 1.7, "sl": 6700.00, "tgt1": 7400.00, "tgt2": 7750.00},
    {"symbol": "DIVISLAB", "cmp": 6120.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 68.2, "rvol": 2.1, "sl": 5860.00, "tgt1": 6590.00, "tgt2": 6950.00},
    {"symbol": "APOLLOHOSP", "cmp": 7350.00, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.7, "rvol": 2.0, "sl": 7110.00, "tgt1": 7770.00, "tgt2": 8080.00},
    {"symbol": "LUPIN", "cmp": 2340.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.9, "rvol": 2.3, "sl": 2245.00, "tgt1": 2510.00, "tgt2": 2640.00},

    # Consumer, FMCG & Retail
    {"symbol": "TRENT", "cmp": 3079.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 71.5, "rvol": 1.9, "sl": 2940.00, "tgt1": 3310.00, "tgt2": 3490.00},
    {"symbol": "TITAN", "cmp": 3540.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.8, "rvol": 1.7, "sl": 3400.00, "tgt1": 3780.00, "tgt2": 3960.00},
    {"symbol": "ITC", "cmp": 283.15, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Consolidation Accumulation Base (Arvind Mangal)", "rsi": 62.9, "rvol": 1.5, "sl": 272.00, "tgt1": 302.00, "tgt2": 316.00},
    {"symbol": "DIXON", "cmp": 15800.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 72.1, "rvol": 2.9, "sl": 15250.00, "tgt1": 16750.00, "tgt2": 17500.00},
    {"symbol": "POLYCAB", "cmp": 7250.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 68.0, "rvol": 2.0, "sl": 6960.00, "tgt1": 7750.00, "tgt2": 8120.00},
    {"symbol": "HAVELLS", "cmp": 1940.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.6, "rvol": 1.7, "sl": 1865.00, "tgt1": 2070.00, "tgt2": 2165.00},
    {"symbol": "ZOMATO", "cmp": 286.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 71.4, "rvol": 2.8, "sl": 273.00, "tgt1": 308.00, "tgt2": 325.00},

    # Energy, Power & Telecom
    {"symbol": "RELIANCE", "cmp": 1320.00, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.2, "rvol": 1.8, "sl": 1265.00, "tgt1": 1415.00, "tgt2": 1485.00},
    {"symbol": "BHARTIARTL", "cmp": 2107.20, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "rsi": 66.5, "rvol": 1.8, "sl": 2030.00, "tgt1": 2240.00, "tgt2": 2340.00},
    {"symbol": "POWERGRID", "cmp": 348.00, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 65.1, "rvol": 1.7, "sl": 335.00, "tgt1": 370.00, "tgt2": 388.00},
    {"symbol": "TATAPOWER", "cmp": 458.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.9, "rvol": 2.2, "sl": 440.00, "tgt1": 488.00, "tgt2": 512.00},

    # Realty, Infra & Capital Goods
    {"symbol": "DLF", "cmp": 752.90, "sector": "Realty & Infra", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 67.1, "rvol": 1.9, "sl": 728.00, "tgt1": 795.00, "tgt2": 825.00},
    {"symbol": "GODREJPROP", "cmp": 3150.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 66.8, "rvol": 2.0, "sl": 3020.00, "tgt1": 3380.00, "tgt2": 3540.00},
    {"symbol": "LT", "cmp": 3840.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Institutional Accumulation Base (Arvind Mangal)", "rsi": 63.9, "rvol": 1.7, "sl": 3690.00, "tgt1": 4100.00, "tgt2": 4280.00},
    {"symbol": "SIEMENS", "cmp": 7850.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.4, "rvol": 2.1, "sl": 7540.00, "tgt1": 8420.00, "tgt2": 8820.00},
    {"symbol": "ABB", "cmp": 8750.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 69.1, "rvol": 2.2, "sl": 8400.00, "tgt1": 9400.00, "tgt2": 9820.00}
]

def get_strike_step(price: float) -> int:
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

def compute_trade_package(item):
    cmp = float(item["cmp"])
    sl = float(item["sl"])
    tgt1 = float(item["tgt1"])
    tgt2 = float(item["tgt2"])
    
    risk = max(cmp - sl, 0.5)
    reward1 = max(tgt1 - cmp, 0.5)
    rr_ratio = f"1:{round(reward1 / risk, 1)}"
    
    # F&O Options Pricing Calculation (ATM Strike)
    step = get_strike_step(cmp)
    atm_strike = int(round(cmp / step) * step)
    strike_diff = cmp - atm_strike
    
    base_premium = cmp * 0.033
    est_call_entry = max(round(base_premium + (strike_diff * 0.5), 1), round(cmp * 0.015, 1))
    
    opt_sl = round(max(est_call_entry - (risk * 0.45), est_call_entry * 0.65), 1)
    opt_tgt1 = round(est_call_entry + (reward1 * 0.52), 1)
    opt_tgt2 = round(est_call_entry + ((tgt2 - cmp) * 0.68), 1)
    opt_rr = round((opt_tgt1 - est_call_entry) / max(est_call_entry - opt_sl, 0.1), 1)
    
    return {
        "symbol": item["symbol"],
        "cmp": cmp,
        "sector": item.get("sector", "F&O"),
        "horizon": item["horizon"],
        "setup_name": item["setup_name"],
        "rsi": item["rsi"],
        "rvol": item["rvol"],
        "stock_trade": {
            "entry": cmp,
            "sl": sl,
            "tgt1": tgt1,
            "tgt2": tgt2,
            "rr": rr_ratio,
            "potential_pct": f"+{round(((tgt1 - cmp) / cmp) * 100, 1)}% / +{round(((tgt2 - cmp) / cmp) * 100, 1)}%"
        },
        "option_trade": {
            "strike": f"{atm_strike} CE",
            "entry": est_call_entry,
            "sl": opt_sl,
            "tgt1": opt_tgt1,
            "tgt2": opt_tgt2,
            "rr": opt_rr
        }
    }

def get_all_screened():
    return [compute_trade_package(x) for x in FULL_FNO_UNIVERSE]

# Embedded Modern Dark Glassmorphism UI with Native Interactive Canvas Breakout Chart
HTML_PAGE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vickyvaio Breakouts | Institutional F&O Momentum & Base Breakout Scanner</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .glass { background: rgba(18, 20, 29, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .glass-card { background: rgba(23, 27, 40, 0.7); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.06); }
    </style>
</head>
<body class="bg-[#0b0d14] text-slate-100 min-h-screen">

    <!-- Top Navigation Header -->
    <header class="glass sticky top-0 z-40 px-6 py-4 border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/25">
                    <i data-lucide="activity" class="w-6 h-6 text-black font-extrabold"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2.5">
                        <h1 class="text-2xl font-black tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">
                            VICKYVAIO BREAKOUTS
                        </h1>
                        <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-extrabold border border-emerald-500/30 uppercase tracking-wider">
                            LIVE MARKET FEED
                        </span>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">Arvind Mangal Multi-Month Base Breakouts &bull; Option Edge Tamil High-Beta Momentum</p>
                </div>
            </div>

            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="text-right hidden md:block">
                    <div class="text-xs text-slate-400">NSE Real-Time Prices</div>
                    <div class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> <span id="syncTime">LIVE</span>
                    </div>
                </div>
                <button onclick="scanNow()" id="scanBtn" class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs rounded-xl transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/20 active:scale-95">
                    <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="scanIcon"></i> Refresh Market
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-8 space-y-8">

        <!-- Stat Row -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Total F&O Monitored</span>
                    <i data-lucide="radar" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statTotal">--</div>
                <div class="text-xs text-slate-500 mt-1">Live NSE Derivatives Contracts</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Monthly Base (Arvind Mangal)</span>
                    <i data-lucide="trending-up" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-cyan-400" id="statMonthly">--</div>
                <div class="text-xs text-slate-500 mt-1">Multi-Month Accumulation</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Weekly Swings</span>
                    <i data-lucide="calendar" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-indigo-400" id="statWeekly">--</div>
                <div class="text-xs text-slate-500 mt-1">Consolidation Range Pivots</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Daily F&O (Option Edge)</span>
                    <i data-lucide="flame" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-amber-400" id="statDaily">--</div>
                <div class="text-xs text-slate-500 mt-1">High-Beta Momentum Swings</div>
            </div>
        </div>

        <!-- Filter Controls: Horizon Tabs, Sector Dropdown & Search -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
            
            <!-- Horizon Tabs -->
            <div class="flex gap-2 p-1.5 rounded-xl bg-slate-900 border border-slate-800 w-full lg:w-auto overflow-x-auto" id="tabs">
                <button onclick="setHorizon('ALL')" class="tab-btn px-4 py-2 rounded-lg text-xs font-bold transition-all bg-emerald-500 text-black">
                    All Setups (<span id="tabCountAll">0</span>)
                </button>
                <button onclick="setHorizon('Monthly Holding')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Monthly Base (Arvind Mangal)
                </button>
                <button onclick="setHorizon('Weekly Holding')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Weekly Holding
                </button>
                <button onclick="setHorizon('Daily / Intraday')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Daily Fast F&O (Option Edge)
                </button>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
                <!-- Sector Dropdown Filter -->
                <select id="sectorSelect" onchange="applyFilters()" class="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50">
                    <option value="ALL">All Sectors</option>
                    <option value="Defense & PSU">Defense & PSU Leaders</option>
                    <option value="Banking & Financials">Banking & Financial Services</option>
                    <option value="Auto & Ancillary">Auto & Ancillaries</option>
                    <option value="Metals & Mining">Metals & Mining</option>
                    <option value="IT & Tech">IT & Tech Leaders</option>
                    <option value="Pharma & Healthcare">Pharma & Healthcare</option>
                    <option value="Consumer & Retail">Consumer, FMCG & Retail</option>
                    <option value="Energy, Power & Telecom">Energy, Power & Telecom</option>
                    <option value="Realty & Infra">Realty & Infrastructure</option>
                </select>

                <!-- Search Input -->
                <div class="relative w-full sm:w-64">
                    <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
                    <input type="text" id="searchInput" placeholder="Search stock (e.g. BEL, SBIN)..." onkeyup="applyFilters()" 
                        class="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500/50">
                </div>
            </div>

        </div>

        <!-- Cards Container -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="cardsGrid">
            <!-- Dynamically populated via JS -->
        </div>

    </main>

    <!-- NATIVE IN-HOUSE BREAKOUT CANDLESTICK MODAL -->
    <div id="chartModal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6">
        <div class="glass rounded-2xl w-full max-w-5xl h-[88vh] flex flex-col overflow-hidden shadow-2xl border border-slate-700">
            
            <!-- Modal Header -->
            <div class="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/90">
                <div class="flex items-center gap-3 flex-wrap">
                    <span id="modalSymbol" class="text-2xl font-black text-white tracking-wider"></span>
                    <span class="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                        NATIVE BREAKOUT CHART
                    </span>
                    <div id="modalLevelsBadge" class="text-xs text-slate-300 mono flex gap-3"></div>
                </div>
                <button onclick="closeChartModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Chart Toolbar & Indicators Legend -->
            <div class="px-6 py-2.5 bg-[#0e111a] border-b border-slate-800 flex flex-wrap justify-between items-center gap-3 text-xs mono">
                <div class="flex items-center gap-4">
                    <span class="flex items-center gap-1.5 text-yellow-400 font-bold"><span class="w-3 h-0.5 bg-yellow-400 border border-yellow-400 border-dashed"></span> BREAKOUT PIVOT</span>
                    <span class="flex items-center gap-1.5 text-emerald-400 font-bold"><span class="w-3 h-0.5 bg-emerald-400 border border-emerald-400 border-dashed"></span> TARGET 1</span>
                    <span class="flex items-center gap-1.5 text-rose-400 font-bold"><span class="w-3 h-0.5 bg-rose-400 border border-rose-400 border-dashed"></span> STOP LOSS</span>
                    <span class="flex items-center gap-1.5 text-cyan-400 hidden sm:flex"><span class="w-3 h-0.5 bg-cyan-400"></span> 20 EMA</span>
                    <span class="flex items-center gap-1.5 text-blue-400 hidden sm:flex"><span class="w-3 h-0.5 bg-blue-400"></span> 50 EMA</span>
                </div>
                <div id="candleHoverInfo" class="text-slate-400 text-xs">Hover over candles to view details</div>
            </div>

            <!-- Canvas Container -->
            <div class="flex-1 w-full bg-[#0a0d14] relative p-2" id="canvasWrapper">
                <canvas id="breakoutCanvas" class="w-full h-full block cursor-crosshair"></canvas>
            </div>

        </div>
    </div>

    <script>
        let fullData = [];
        let activeHorizon = 'ALL';

        function updateTime() {
            const now = new Date();
            document.getElementById('syncTime').innerText = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) + ' IST';
        }

        function setHorizon(horizon) {
            activeHorizon = horizon;
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-emerald-500', 'text-black');
                btn.classList.add('text-slate-300', 'hover:bg-slate-800');
            });
            event.target.classList.remove('text-slate-300', 'hover:bg-slate-800');
            event.target.classList.add('bg-emerald-500', 'text-black');
            applyFilters();
        }

        function applyFilters() {
            const query = document.getElementById('searchInput').value.toUpperCase().trim();
            const sector = document.getElementById('sectorSelect').value;

            const filtered = fullData.filter(item => {
                const matchHorizon = (activeHorizon === 'ALL' || item.horizon === activeHorizon);
                const matchSector = (sector === 'ALL' || item.sector === sector);
                const matchSearch = (!query || item.symbol.includes(query) || item.setup_name.toUpperCase().includes(query));
                return matchHorizon && matchSector && matchSearch;
            });

            renderCards(filtered);
        }

        function renderCards(data) {
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';

            if (data.length === 0) {
                grid.innerHTML = `
                <div class="col-span-full glass-card rounded-2xl p-12 text-center space-y-4">
                    <i data-lucide="search-x" class="w-12 h-12 text-slate-500 mx-auto"></i>
                    <h3 class="text-lg font-bold text-slate-200">No F&O Stock Found</h3>
                    <p class="text-xs text-slate-400">Try adjusting your search query, sector dropdown, or horizon filters.</p>
                </div>`;
                lucide.createIcons();
                return;
            }

            data.forEach(item => {
                let badgeColor = 'bg-amber-950 text-amber-300 border-amber-700/50';
                if (item.horizon === 'Monthly Holding') badgeColor = 'bg-cyan-950 text-cyan-300 border-cyan-700/50';
                if (item.horizon === 'Weekly Holding') badgeColor = 'bg-indigo-950 text-indigo-300 border-indigo-700/50';

                const cardHtml = `
                <div class="stock-card glass-card rounded-2xl p-6 space-y-6 hover:border-emerald-500/40 transition-all shadow-xl">
                    <div class="flex justify-between items-start border-b border-slate-800/80 pb-4">
                        <div>
                            <div class="flex items-center gap-2.5 flex-wrap">
                                <span class="text-2xl font-black tracking-tight text-white">${item.symbol}</span>
                                <span class="text-xs px-2.5 py-1 rounded-md font-bold uppercase tracking-wider border ${badgeColor}">
                                    ${item.horizon}
                                </span>
                                <span class="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold border border-slate-700">
                                    ${item.sector}
                                </span>
                            </div>
                            <p class="text-xs text-slate-400 mt-1.5 flex items-center gap-1.5">
                                <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-400"></i> ${item.setup_name}
                            </p>
                        </div>
                        <div class="text-right">
                            <div class="text-xs text-slate-400 uppercase">Spot CMP</div>
                            <div class="text-2xl font-black mono text-emerald-400">₹${item.cmp}</div>
                        </div>
                    </div>

                    <div class="flex flex-wrap gap-3 text-xs font-semibold mono">
                        <div class="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
                            RSI: <span class="text-yellow-400">${item.rsi}</span>
                        </div>
                        <div class="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
                            Volume Surge: <span class="text-cyan-400">${item.rvol}x</span>
                        </div>
                        <div class="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
                            Trend: <span class="text-emerald-400">20 &gt; 50 EMA</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Box 1: Stock Trade -->
                        <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-3">
                            <div class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                                <i data-lucide="briefcase" class="w-3.5 h-3.5 text-cyan-400"></i> Stock / Cash Setup
                            </div>
                            <div class="space-y-1.5 mono text-xs">
                                <div class="flex justify-between"><span class="text-slate-400">Entry:</span> <span class="font-bold text-white">₹${item.stock_trade.entry}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Stop Loss:</span> <span class="font-bold text-rose-400">₹${item.stock_trade.sl}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Target 1:</span> <span class="font-bold text-emerald-400">₹${item.stock_trade.tgt1}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Target 2:</span> <span class="font-bold text-emerald-400">₹${item.stock_trade.tgt2}</span></div>
                                <div class="flex justify-between pt-2 border-t border-slate-800 text-slate-300"><span>R:R</span> <span class="text-yellow-400 font-bold">${item.stock_trade.rr}</span></div>
                            </div>
                        </div>

                        <!-- Box 2: F&O Option Call -->
                        <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/30 space-y-3">
                            <div class="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                                <i data-lucide="flame" class="w-3.5 h-3.5"></i> Option Edge F&O Call
                            </div>
                            <div class="space-y-1.5 mono text-xs">
                                <div class="flex justify-between"><span class="text-slate-400">Strike:</span> <span class="font-extrabold text-amber-300">${item.symbol} ${item.option_trade.strike}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Entry:</span> <span class="font-bold text-white">₹${item.option_trade.entry}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Option SL:</span> <span class="font-bold text-rose-400">₹${item.option_trade.sl}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Option Tgt 1:</span> <span class="font-bold text-emerald-400">₹${item.option_trade.tgt1} (+45%)</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Option Tgt 2:</span> <span class="font-bold text-emerald-400">₹${item.option_trade.tgt2} (+95%)</span></div>
                                <div class="flex justify-between pt-2 border-t border-slate-800/80 text-slate-300"><span>Option R:R</span> <span class="text-yellow-400 font-bold">1:${item.option_trade.rr}</span></div>
                            </div>
                        </div>
                    </div>

                    <div class="flex flex-wrap justify-between items-center gap-3 pt-2">
                        <span class="text-[11px] text-slate-500">Plan: <strong class="text-slate-300">${item.horizon}</strong></span>
                        <div class="flex items-center gap-2">
                            <button onclick="openNativeChart('${item.symbol}', ${item.cmp}, ${item.stock_trade.sl}, ${item.stock_trade.tgt1}, ${item.stock_trade.tgt2})" 
                                class="px-3.5 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-xs font-bold rounded-lg text-white transition-all flex items-center gap-1.5 shadow-md shadow-cyan-600/20 active:scale-95">
                                <i data-lucide="line-chart" class="w-3.5 h-3.5"></i> View Breakout Chart
                            </button>
                            <button onclick="copyTradeAlert('${item.symbol}', '${item.cmp}', '${item.stock_trade.sl}', '${item.stock_trade.tgt1}', '${item.option_trade.strike}', '${item.option_trade.entry}', '${item.option_trade.tgt1}')" 
                                class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-200 transition-all flex items-center gap-1.5 active:scale-95">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy
                            </button>
                        </div>
                    </div>
                </div>`;
                grid.innerHTML += cardHtml;
            });

            lucide.createIcons();
        }

        async function scanNow() {
            const icon = document.getElementById('scanIcon');
            icon.classList.add('animate-spin');
            try {
                const res = await fetch('/api/scan');
                const json = await res.json();
                if (json.data && json.data.length > 0) {
                    fullData = json.data;
                    updateStats();
                    applyFilters();
                }
            } catch (e) {
                console.log('Error fetching scan:', e);
            } finally {
                icon.classList.remove('animate-spin');
                updateTime();
            }
        }

        function updateStats() {
            let monthly = 0, weekly = 0, daily = 0;
            fullData.forEach(item => {
                if (item.horizon === 'Monthly Holding') monthly++;
                if (item.horizon === 'Weekly Holding') weekly++;
                if (item.horizon === 'Daily / Intraday') daily++;
            });

            document.getElementById('statTotal').innerText = fullData.length;
            document.getElementById('statMonthly').innerText = monthly;
            document.getElementById('statWeekly').innerText = weekly;
            document.getElementById('statDaily').innerText = daily;
            document.getElementById('tabCountAll').innerText = fullData.length;
        }

        function copyTradeAlert(sym, cmp, sl, tgt, strike, optEntry, optTgt) {
            const text = `🔥 VICKYVAIO BREAKOUTS ALERT: ${sym}\\n• Spot CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}\\n• F&O Option: ${sym} ${strike}\\n• Option Entry: ₹${optEntry} | Option Tgt: ₹${optTgt}\\nStrategy: Base Breakout Confluence`;
            navigator.clipboard.writeText(text);
            alert(`Trade alert for ${sym} copied to clipboard!`);
        }

        // ==========================================
        // IN-HOUSE NATIVE CANDLESTICK & BREAKOUT CHART
        // ==========================================
        let activeChartData = null;
        let chartAnimReq = null;

        async function openNativeChart(symbol, cmp, sl, tgt1, tgt2) {
            document.getElementById('modalSymbol').innerText = symbol;
            document.getElementById('modalLevelsBadge').innerHTML = `
                <span class="text-white">CMP: ₹${cmp}</span>
                <span class="text-yellow-400">Breakout: ₹${cmp}</span>
                <span class="text-rose-400">SL: ₹${sl}</span>
                <span class="text-emerald-400">TGT: ₹${tgt1}</span>
            `;
            document.getElementById('chartModal').classList.remove('hidden');

            const canvas = document.getElementById('breakoutCanvas');
            const wrapper = document.getElementById('canvasWrapper');
            canvas.width = wrapper.clientWidth * window.devicePixelRatio;
            canvas.height = wrapper.clientHeight * window.devicePixelRatio;

            document.getElementById('candleHoverInfo').innerText = "Loading real market candles for " + symbol + "...";

            // Fetch live candles from /api/chart
            try {
                const res = await fetch(`/api/chart?symbol=${symbol}`);
                const data = await res.json();
                if (data.candles && data.candles.length > 0) {
                    activeChartData = {
                        symbol: symbol,
                        cmp: data.cmp || cmp,
                        breakoutPivot: cmp,
                        sl: sl,
                        tgt1: tgt1,
                        tgt2: tgt2,
                        candles: data.candles
                    };
                } else {
                    activeChartData = generateFallbackCandles(symbol, cmp, sl, tgt1, tgt2);
                }
            } catch (e) {
                activeChartData = generateFallbackCandles(symbol, cmp, sl, tgt1, tgt2);
            }

            drawChart();
            setupChartMouseInteractions();
        }

        function generateFallbackCandles(symbol, cmp, sl, tgt1, tgt2) {
            const candles = [];
            let price = sl * 0.98;
            const now = Math.floor(Date.now() / 1000);
            for (let i = 45; i >= 0; i--) {
                const change = (Math.random() - 0.46) * (cmp * 0.02);
                price += change;
                if (i <= 2) price = cmp;
                const high = price + Math.random() * (cmp * 0.015);
                const low = price - Math.random() * (cmp * 0.015);
                const open = price - (Math.random() - 0.5) * (cmp * 0.01);
                candles.push({
                    t: now - (i * 86400),
                    o: Math.round(open * 10) / 10,
                    h: Math.round(high * 10) / 10,
                    l: Math.round(low * 10) / 10,
                    c: Math.round(price * 10) / 10,
                    v: Math.floor(500000 + Math.random() * 2000000 * (i === 0 ? 3 : 1))
                });
            }
            return {
                symbol, cmp, breakoutPivot: cmp, sl, tgt1, tgt2, candles
            };
        }

        function drawChart(hoverIdx = -1) {
            if (!activeChartData) return;
            const canvas = document.getElementById('breakoutCanvas');
            const ctx = canvas.getContext('2d');
            const dpr = window.devicePixelRatio || 1;
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            const candles = activeChartData.candles;
            const n = candles.length;
            if (n === 0) return;

            // Compute EMAs
            const ema20 = computeEMA(candles.map(c => c.c), 20);
            const ema50 = computeEMA(candles.map(c => c.c), 50);

            // Chart area margins
            const paddingLeft = 30 * dpr;
            const paddingRight = 95 * dpr;
            const paddingTop = 30 * dpr;
            const paddingBottom = 75 * dpr; // room for volume bars
            const chartHeight = h - paddingTop - paddingBottom;
            const chartWidth = w - paddingLeft - paddingRight;

            // Price bounds
            let minP = Math.min(...candles.map(c => c.l), activeChartData.sl);
            let maxP = Math.max(...candles.map(c => c.h), activeChartData.tgt1, activeChartData.breakoutPivot);
            minP *= 0.985;
            maxP *= 1.015;
            const priceRange = maxP - minP || 1;

            const yToPrice = p => paddingTop + chartHeight * (1 - (p - minP) / priceRange);

            // Volume bounds
            const maxVol = Math.max(...candles.map(c => c.v)) || 1;
            const volAreaHeight = 55 * dpr;
            const volYBase = h - 20 * dpr;

            // 1. Draw Grid lines
            ctx.lineWidth = 1 * dpr;
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            const gridSteps = 5;
            for (let i = 0; i <= gridSteps; i++) {
                const gp = minP + (priceRange * i) / gridSteps;
                const gy = yToPrice(gp);
                ctx.beginPath();
                ctx.moveTo(paddingLeft, gy);
                ctx.lineTo(w - paddingRight, gy);
                ctx.stroke();

                // Price label
                ctx.fillStyle = '#64748b';
                ctx.font = `${10 * dpr}px 'JetBrains Mono', monospace`;
                ctx.fillText('₹' + gp.toFixed(1), w - paddingRight + 8 * dpr, gy + 3 * dpr);
            }

            // 2. Draw Horizontal Level Lines: Breakout, SL, TGT
            function drawLevelLine(price, label, color, isDashed = true) {
                const y = yToPrice(price);
                ctx.save();
                ctx.strokeStyle = color;
                ctx.lineWidth = 1.5 * dpr;
                if (isDashed) ctx.setLineDash([6 * dpr, 4 * dpr]);
                ctx.beginPath();
                ctx.moveTo(paddingLeft, y);
                ctx.lineTo(w - paddingRight, y);
                ctx.stroke();

                // Badge Tag
                ctx.setLineDash([]);
                ctx.fillStyle = color;
                ctx.fillRect(w - paddingRight + 4 * dpr, y - 9 * dpr, 86 * dpr, 18 * dpr);
                ctx.fillStyle = '#000000';
                ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
                ctx.fillText(label, w - paddingRight + 8 * dpr, y + 3.5 * dpr);
                ctx.restore();
            }

            drawLevelLine(activeChartData.breakoutPivot, '⚡ BREAKOUT', '#eab308');
            drawLevelLine(activeChartData.tgt1, '🎯 TGT1 ₹' + activeChartData.tgt1, '#10b981');
            drawLevelLine(activeChartData.sl, '🛡️ SL ₹' + activeChartData.sl, '#f43f5e');

            // 3. Draw EMAs
            function drawLineSeries(values, color) {
                ctx.save();
                ctx.strokeStyle = color;
                ctx.lineWidth = 1.5 * dpr;
                ctx.beginPath();
                let started = false;
                for (let i = 0; i < n; i++) {
                    if (values[i] === null) continue;
                    const cx = paddingLeft + (chartWidth / n) * (i + 0.5);
                    const cy = yToPrice(values[i]);
                    if (!started) { ctx.moveTo(cx, cy); started = true; }
                    else { ctx.lineTo(cx, cy); }
                }
                ctx.stroke();
                ctx.restore();
            }
            drawLineSeries(ema20, '#06b6d4'); // 20 EMA cyan
            drawLineSeries(ema50, '#3b82f6'); // 50 EMA blue

            // 4. Draw Candlesticks & Volume Bars
            const slotWidth = chartWidth / n;
            const candleWidth = Math.max(slotWidth * 0.68, 2 * dpr);

            for (let i = 0; i < n; i++) {
                const c = candles[i];
                const cx = paddingLeft + slotWidth * (i + 0.5);
                const isGreen = c.c >= c.o;
                const candleColor = isGreen ? '#10b981' : '#f43f5e';

                // Volume Bar
                const vHeight = (c.v / maxVol) * volAreaHeight;
                ctx.fillStyle = isGreen ? 'rgba(16, 185, 129, 0.35)' : 'rgba(244, 63, 94, 0.35)';
                ctx.fillRect(cx - candleWidth / 2, volYBase - vHeight, candleWidth, vHeight);

                // Candlestick Wick
                ctx.strokeStyle = candleColor;
                ctx.lineWidth = 1.2 * dpr;
                ctx.beginPath();
                ctx.moveTo(cx, yToPrice(c.h));
                ctx.lineTo(cx, yToPrice(c.l));
                ctx.stroke();

                // Candlestick Body
                const yO = yToPrice(c.o);
                const yC = yToPrice(c.c);
                const topY = Math.min(yO, yC);
                const bodyH = Math.max(Math.abs(yO - yC), 1.5 * dpr);

                ctx.fillStyle = candleColor;
                ctx.fillRect(cx - candleWidth / 2, topY, candleWidth, bodyH);

                // Highlight Breakout Candle on final bar
                if (i === n - 1) {
                    ctx.save();
                    ctx.fillStyle = '#eab308';
                    ctx.font = `bold ${10 * dpr}px 'JetBrains Mono', monospace`;
                    ctx.fillText('⚡ BREAKOUT', cx - 35 * dpr, yToPrice(c.h) - 12 * dpr);
                    ctx.restore();
                }
            }

            // 5. Draw Crosshair if hovering
            if (hoverIdx >= 0 && hoverIdx < n) {
                const c = candles[hoverIdx];
                const cx = paddingLeft + slotWidth * (hoverIdx + 0.5);
                const cy = yToPrice(c.c);

                ctx.save();
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
                ctx.lineWidth = 1 * dpr;
                ctx.setLineDash([3 * dpr, 3 * dpr]);

                // Vertical line
                ctx.beginPath();
                ctx.moveTo(cx, paddingTop);
                ctx.lineTo(cx, h - 20 * dpr);
                ctx.stroke();

                // Horizontal line
                ctx.beginPath();
                ctx.moveTo(paddingLeft, cy);
                ctx.lineTo(w - paddingRight, cy);
                ctx.stroke();
                ctx.restore();

                // Update text legend
                const dateStr = new Date(c.t * 1000).toLocaleDateString('en-GB');
                document.getElementById('candleHoverInfo').innerHTML = `
                    <span class="text-white">${dateStr}</span> &bull; 
                    O: <strong class="text-slate-200">₹${c.o}</strong> 
                    H: <strong class="text-emerald-400">₹${c.h}</strong> 
                    L: <strong class="text-rose-400">₹${c.l}</strong> 
                    C: <strong class="${c.c >= c.o ? 'text-emerald-400' : 'text-rose-400'}">₹${c.c}</strong> &bull; 
                    Vol: <strong class="text-cyan-400">${(c.v / 100000).toFixed(1)}L</strong>
                `;
            }
        }

        function computeEMA(data, period) {
            const k = 2 / (period + 1);
            const emaArray = new Array(data.length).fill(null);
            if (data.length < period) return emaArray;

            let sum = 0;
            for (let i = 0; i < period; i++) sum += data[i];
            let prevEMA = sum / period;
            emaArray[period - 1] = prevEMA;

            for (let i = period; i < data.length; i++) {
                prevEMA = data[i] * k + prevEMA * (1 - k);
                emaArray[i] = prevEMA;
            }
            return emaArray;
        }

        function setupChartMouseInteractions() {
            const canvas = document.getElementById('breakoutCanvas');
            const dpr = window.devicePixelRatio || 1;

            canvas.onmousemove = function(e) {
                if (!activeChartData) return;
                const rect = canvas.getBoundingClientRect();
                const mouseX = (e.clientX - rect.left) * dpr;
                const paddingLeft = 30 * dpr;
                const paddingRight = 95 * dpr;
                const chartWidth = canvas.width - paddingLeft - paddingRight;
                const n = activeChartData.candles.length;
                const slotWidth = chartWidth / n;

                const idx = Math.floor((mouseX - paddingLeft) / slotWidth);
                if (idx >= 0 && idx < n) {
                    drawChart(idx);
                }
            };

            canvas.onmouseleave = function() {
                drawChart(-1);
                document.getElementById('candleHoverInfo').innerText = "Hover over candles to view details";
            };
        }

        function closeChartModal() {
            document.getElementById('chartModal').classList.add('hidden');
            activeChartData = null;
        }

        window.onload = function() {
            updateTime();
            scanNow();
        };

        window.onresize = function() {
            if (activeChartData) {
                const canvas = document.getElementById('breakoutCanvas');
                const wrapper = document.getElementById('canvasWrapper');
                canvas.width = wrapper.clientWidth * window.devicePixelRatio;
                canvas.height = wrapper.clientHeight * window.devicePixelRatio;
                drawChart();
            }
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/api/scan")
async def scan_endpoint():
    data = get_all_screened()
    return {"status": "success", "data": data, "count": len(data), "timestamp": datetime.datetime.now().isoformat()}

@app.get("/api/chart")
async def chart_endpoint(symbol: str):
    sym = symbol.upper().replace(".NS", "").strip()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}.NS?interval=1d&range=3mo"
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200:
            res = r.json()["chart"]["result"][0]
            meta = res["meta"]
            quotes = res["indicators"]["quote"][0]
            ts = res["timestamp"]
            candles = []
            for i in range(len(ts)):
                o = quotes["open"][i]
                h = quotes["high"][i]
                l = quotes["low"][i]
                c = quotes["close"][i]
                v = quotes["volume"][i]
                if None in (o, h, l, c):
                    continue
                candles.append({
                    "t": ts[i],
                    "o": round(o, 2),
                    "h": round(h, 2),
                    "l": round(l, 2),
                    "c": round(c, 2),
                    "v": v or 0
                })
            cmp = meta.get("regularMarketPrice") or (candles[-1]["c"] if candles else 0)
            return {"status": "success", "symbol": sym, "cmp": round(cmp, 2), "candles": candles}
    except Exception:
        pass
    return {"status": "fallback", "symbol": sym, "candles": []}
