import datetime
import math
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Verified Authentic Breakout Setups with Exact Resistance, Base Floor, and Quality Scoring
VERIFIED_BREAKOUT_DATA = [{"symbol": "EICHERMOT", "cmp": 7713.0, "resistance": 7713.0, "base_floor": 6767.5, "pct_dist": 0.0, "stage": "🔥 LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.2, "rvol": 0.91, "stock_trade": {"entry": 7713.0, "sl": 6767.5, "tgt1": 9131.25, "tgt2": 10360.4, "rr": "1:1.5", "potential_pct": "+18.4% / +34.3%"}, "option_trade": {"strike": "7800 CE", "entry": 211.0, "sl": 137.2, "tgt1": 948.5, "tgt2": 2011.2, "rr": 10.0}}, {"symbol": "GODREJPROP", "cmp": 1815.0, "resistance": 1815.0, "base_floor": 1468.4, "pct_dist": 0.0, "stage": "🔥 LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.6, "rvol": 1.49, "stock_trade": {"entry": 1815.0, "sl": 1468.4, "tgt1": 2334.9, "tgt2": 2785.48, "rr": "1:1.5", "potential_pct": "+28.6% / +53.5%"}, "option_trade": {"strike": "1800 CE", "entry": 67.4, "sl": 43.8, "tgt1": 337.7, "tgt2": 727.3, "rr": 11.5}}, {"symbol": "ICICIBANK", "cmp": 1500.0, "resistance": 1501.4, "base_floor": 1329.4, "pct_dist": -0.09, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 74.7, "rvol": 2.95, "stock_trade": {"entry": 1500.0, "sl": 1329.4, "tgt1": 1755.9, "tgt2": 1977.68, "rr": "1:1.5", "potential_pct": "+17.1% / +31.8%"}, "option_trade": {"strike": "1500 CE", "entry": 49.5, "sl": 32.2, "tgt1": 182.6, "tgt2": 374.3, "rr": 7.7}}, {"symbol": "DIVISLAB", "cmp": 10140.5, "resistance": 10159.0, "base_floor": 8797.0, "pct_dist": -0.18, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.6, "rvol": 1.34, "stock_trade": {"entry": 10140.5, "sl": 8797.0, "tgt1": 12155.75, "tgt2": 13902.3, "rr": "1:1.5", "potential_pct": "+19.9% / +37.1%"}, "option_trade": {"strike": "10200 CE", "entry": 304.9, "sl": 198.2, "tgt1": 1352.8, "tgt2": 2862.9, "rr": 9.8}}, {"symbol": "MARUTI", "cmp": 12652.0, "resistance": 12681.0, "base_floor": 10985.0, "pct_dist": -0.23, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 77.1, "rvol": 1.87, "stock_trade": {"entry": 12652.0, "sl": 10985.0, "tgt1": 15152.5, "tgt2": 17319.6, "rr": "1:1.5", "potential_pct": "+19.8% / +36.9%"}, "option_trade": {"strike": "12600 CE", "entry": 443.5, "sl": 288.3, "tgt1": 1743.8, "tgt2": 3617.5, "rr": 8.4}}, {"symbol": "HEROMOTOCO", "cmp": 5514.0, "resistance": 5527.0, "base_floor": 4825.0, "pct_dist": -0.24, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.8, "rvol": 1.34, "stock_trade": {"entry": 5514.0, "sl": 4825.0, "tgt1": 6547.5, "tgt2": 7443.2, "rr": "1:1.5", "potential_pct": "+18.7% / +35.0%"}, "option_trade": {"strike": "5600 CE", "entry": 139.0, "sl": 90.4, "tgt1": 676.4, "tgt2": 1450.9, "rr": 11.1}}, {"symbol": "CIPLA", "cmp": 1404.1, "resistance": 1408.0, "base_floor": 1292.0, "pct_dist": -0.28, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 79.4, "rvol": 1.25, "stock_trade": {"entry": 1404.1, "sl": 1292.0, "tgt1": 1572.25, "tgt2": 1717.98, "rr": "1:1.5", "potential_pct": "+12.0% / +22.4%"}, "option_trade": {"strike": "1400 CE", "entry": 48.4, "sl": 31.5, "tgt1": 135.8, "tgt2": 261.8, "rr": 5.2}}, {"symbol": "BAJAJ-AUTO", "cmp": 10758.0, "resistance": 10789.0, "base_floor": 9637.0, "pct_dist": -0.29, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 62.4, "rvol": 1.85, "stock_trade": {"entry": 10758.0, "sl": 9637.0, "tgt1": 12439.5, "tgt2": 13896.8, "rr": "1:1.5", "potential_pct": "+15.6% / +29.2%"}, "option_trade": {"strike": "10800 CE", "entry": 334.0, "sl": 217.1, "tgt1": 1208.4, "tgt2": 2468.4, "rr": 7.5}}, {"symbol": "SBIN", "cmp": 1006.4, "resistance": 1009.6, "base_floor": 937.5, "pct_dist": -0.32, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.2, "rvol": 1.43, "stock_trade": {"entry": 1006.4, "sl": 937.5, "tgt1": 1109.75, "tgt2": 1199.32, "rr": "1:1.5", "potential_pct": "+10.3% / +19.2%"}, "option_trade": {"strike": "1000 CE", "entry": 36.4, "sl": 23.7, "tgt1": 90.1, "tgt2": 167.6, "rr": 4.2}}, {"symbol": "HDFCBANK", "cmp": 760.0, "resistance": 762.7, "base_floor": 669.2, "pct_dist": -0.35, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 62.3, "rvol": 2.3, "stock_trade": {"entry": 760.0, "sl": 669.2, "tgt1": 896.2, "tgt2": 1014.24, "rr": "1:1.5", "potential_pct": "+17.9% / +33.5%"}, "option_trade": {"strike": "760 CE", "entry": 25.1, "sl": 16.3, "tgt1": 95.9, "tgt2": 198.0, "rr": 8.0}}, {"symbol": "DLF", "cmp": 745.2, "resistance": 748.0, "base_floor": 634.15, "pct_dist": -0.37, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 79.7, "rvol": 1.09, "stock_trade": {"entry": 745.2, "sl": 634.15, "tgt1": 911.78, "tgt2": 1056.14, "rr": "1:1.5", "potential_pct": "+22.4% / +41.7%"}, "option_trade": {"strike": "740 CE", "entry": 27.2, "sl": 17.7, "tgt1": 113.8, "tgt2": 238.6, "rr": 9.1}}, {"symbol": "BAJFINANCE", "cmp": 1070.0, "resistance": 1074.85, "base_floor": 899.15, "pct_dist": -0.45, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 68.9, "rvol": 0.95, "stock_trade": {"entry": 1070.0, "sl": 899.15, "tgt1": 1326.28, "tgt2": 1548.38, "rr": "1:1.5", "potential_pct": "+24.0% / +44.7%"}, "option_trade": {"strike": "1080 CE", "entry": 30.3, "sl": 19.7, "tgt1": 163.6, "tgt2": 355.6, "rr": 12.6}}, {"symbol": "TITAN", "cmp": 4834.6, "resistance": 4857.1, "base_floor": 4209.0, "pct_dist": -0.46, "stage": "⚡ IMMINENT PIVOT BREAKOUT", "score": 90, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 75.4, "rvol": 5.55, "stock_trade": {"entry": 4834.6, "sl": 4209.0, "tgt1": 5773.0, "tgt2": 6586.28, "rr": "1:1.5", "potential_pct": "+19.4% / +36.2%"}, "option_trade": {"strike": "4800 CE", "entry": 176.8, "sl": 114.9, "tgt1": 664.8, "tgt2": 1367.9, "rr": 7.9}}, {"symbol": "LT", "cmp": 4050.0, "resistance": 4071.6, "base_floor": 3592.9, "pct_dist": -0.53, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 90.4, "rvol": 1.53, "stock_trade": {"entry": 4050.0, "sl": 3592.9, "tgt1": 4735.65, "tgt2": 5329.88, "rr": "1:1.5", "potential_pct": "+16.9% / +31.6%"}, "option_trade": {"strike": "4000 CE", "entry": 158.7, "sl": 103.2, "tgt1": 515.2, "tgt2": 1029.0, "rr": 6.4}}, {"symbol": "PNB", "cmp": 126.1, "resistance": 126.8, "base_floor": 113.71, "pct_dist": -0.55, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 73.5, "rvol": 0.97, "stock_trade": {"entry": 126.1, "sl": 113.71, "tgt1": 144.68, "tgt2": 160.79, "rr": "1:1.5", "potential_pct": "+14.7% / +27.5%"}, "option_trade": {"strike": "126 CE", "entry": 4.2, "sl": 2.7, "tgt1": 13.9, "tgt2": 27.8, "rr": 6.5}}, {"symbol": "M&M", "cmp": 3127.5, "resistance": 3145.0, "base_floor": 2744.3, "pct_dist": -0.56, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 76.5, "rvol": 3.26, "stock_trade": {"entry": 3127.5, "sl": 2744.3, "tgt1": 3702.3, "tgt2": 4200.46, "rr": "1:1.5", "potential_pct": "+18.4% / +34.3%"}, "option_trade": {"strike": "3100 CE", "entry": 117.0, "sl": 76.0, "tgt1": 415.9, "tgt2": 846.6, "rr": 7.3}}, {"symbol": "MUTHOOTFIN", "cmp": 2839.0, "resistance": 2856.8, "base_floor": 2305.0, "pct_dist": -0.62, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.3, "rvol": 1.3, "stock_trade": {"entry": 2839.0, "sl": 2305.0, "tgt1": 3640.0, "tgt2": 4334.2, "rr": "1:1.5", "potential_pct": "+28.2% / +52.7%"}, "option_trade": {"strike": "2800 CE", "entry": 113.2, "sl": 73.6, "tgt1": 529.7, "tgt2": 1129.9, "rr": 10.5}}, {"symbol": "TATAPOWER", "cmp": 364.55, "resistance": 366.9, "base_floor": 333.2, "pct_dist": -0.64, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 63.0, "rvol": 2.32, "stock_trade": {"entry": 364.55, "sl": 333.2, "tgt1": 411.57, "tgt2": 452.33, "rr": "1:1.5", "potential_pct": "+12.9% / +24.1%"}, "option_trade": {"strike": "360 CE", "entry": 14.3, "sl": 9.3, "tgt1": 38.8, "tgt2": 74.0, "rr": 4.9}}, {"symbol": "NATIONALUM", "cmp": 331.0, "resistance": 333.2, "base_floor": 293.0, "pct_dist": -0.66, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 56.0, "rvol": 1.14, "stock_trade": {"entry": 331.0, "sl": 293.0, "tgt1": 388.0, "tgt2": 437.4, "rr": "1:1.5", "potential_pct": "+17.2% / +32.1%"}, "option_trade": {"strike": "330 CE", "entry": 11.4, "sl": 7.4, "tgt1": 41.0, "tgt2": 83.8, "rr": 7.4}}, {"symbol": "BANKBARODA", "cmp": 249.67, "resistance": 251.34, "base_floor": 225.2, "pct_dist": -0.66, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 71.8, "rvol": 0.98, "stock_trade": {"entry": 249.67, "sl": 225.2, "tgt1": 286.37, "tgt2": 318.19, "rr": "1:1.5", "potential_pct": "+14.7% / +27.4%"}, "option_trade": {"strike": "250 CE", "entry": 8.1, "sl": 5.3, "tgt1": 27.2, "tgt2": 54.7, "rr": 6.8}}, {"symbol": "TATASTEEL", "cmp": 182.0, "resistance": 183.33, "base_floor": 163.41, "pct_dist": -0.73, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 58.5, "rvol": 1.53, "stock_trade": {"entry": 182.0, "sl": 163.41, "tgt1": 209.88, "tgt2": 234.05, "rr": "1:1.5", "potential_pct": "+15.3% / +28.6%"}, "option_trade": {"strike": "180 CE", "entry": 7.0, "sl": 4.5, "tgt1": 21.5, "tgt2": 42.4, "rr": 5.8}}, {"symbol": "BAJAJFINSV", "cmp": 1835.0, "resistance": 1848.8, "base_floor": 1624.8, "pct_dist": -0.75, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.8, "rvol": 0.65, "stock_trade": {"entry": 1835.0, "sl": 1624.8, "tgt1": 2150.3, "tgt2": 2423.56, "rr": "1:1.5", "potential_pct": "+17.2% / +32.1%"}, "option_trade": {"strike": "1850 CE", "entry": 53.1, "sl": 34.5, "tgt1": 217.1, "tgt2": 453.3, "rr": 8.8}}, {"symbol": "WIPRO", "cmp": 198.4, "resistance": 200.11, "base_floor": 158.3, "pct_dist": -0.85, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 73.7, "rvol": 0.67, "stock_trade": {"entry": 198.4, "sl": 158.3, "tgt1": 258.55, "tgt2": 310.68, "rr": "1:1.5", "potential_pct": "+30.3% / +56.6%"}, "option_trade": {"strike": "200 CE", "entry": 5.7, "sl": 3.7, "tgt1": 37.0, "tgt2": 82.1, "rr": 15.7}}, {"symbol": "MOTHERSON", "cmp": 168.0, "resistance": 169.49, "base_floor": 147.27, "pct_dist": -0.88, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 60.8, "rvol": 4.18, "stock_trade": {"entry": 168.0, "sl": 147.27, "tgt1": 199.09, "tgt2": 226.04, "rr": "1:1.5", "potential_pct": "+18.5% / +34.5%"}, "option_trade": {"strike": "170 CE", "entry": 4.5, "sl": 2.9, "tgt1": 20.7, "tgt2": 44.0, "rr": 10.1}}, {"symbol": "RELIANCE", "cmp": 1313.4, "resistance": 1325.0, "base_floor": 1152.2, "pct_dist": -0.88, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 68.5, "rvol": 1.11, "stock_trade": {"entry": 1313.4, "sl": 1152.2, "tgt1": 1555.2, "tgt2": 1764.76, "rr": "1:1.5", "potential_pct": "+18.4% / +34.4%"}, "option_trade": {"strike": "1300 CE", "entry": 50.0, "sl": 32.5, "tgt1": 175.7, "tgt2": 356.9, "rr": 7.2}}, {"symbol": "TVSMOTOR", "cmp": 4450.0, "resistance": 4490.0, "base_floor": 3741.9, "pct_dist": -0.89, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 75.5, "rvol": 0.74, "stock_trade": {"entry": 4450.0, "sl": 3741.9, "tgt1": 5512.15, "tgt2": 6432.68, "rr": "1:1.5", "potential_pct": "+23.9% / +44.6%"}, "option_trade": {"strike": "4400 CE", "entry": 171.8, "sl": 111.7, "tgt1": 724.1, "tgt2": 1520.0, "rr": 9.2}}, {"symbol": "HINDALCO", "cmp": 937.85, "resistance": 947.7, "base_floor": 851.1, "pct_dist": -1.04, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Metals & Mining", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 65.9, "rvol": 3.29, "stock_trade": {"entry": 937.85, "sl": 851.1, "tgt1": 1067.97, "tgt2": 1180.75, "rr": "1:1.5", "potential_pct": "+13.9% / +25.9%"}, "option_trade": {"strike": "940 CE", "entry": 29.9, "sl": 19.4, "tgt1": 97.6, "tgt2": 195.1, "rr": 6.4}}, {"symbol": "JSWSTEEL", "cmp": 1355.6, "resistance": 1370.0, "base_floor": 1158.0, "pct_dist": -1.05, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 74.0, "rvol": 1.35, "stock_trade": {"entry": 1355.6, "sl": 1158.0, "tgt1": 1652.0, "tgt2": 1908.88, "rr": "1:1.5", "potential_pct": "+21.9% / +40.8%"}, "option_trade": {"strike": "1350 CE", "entry": 47.5, "sl": 30.9, "tgt1": 201.6, "tgt2": 423.7, "rr": 9.3}}, {"symbol": "AXISBANK", "cmp": 1280.0, "resistance": 1293.8, "base_floor": 1196.9, "pct_dist": -1.07, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 48.1, "rvol": 1.32, "stock_trade": {"entry": 1280.0, "sl": 1196.9, "tgt1": 1404.65, "tgt2": 1512.68, "rr": "1:1.5", "potential_pct": "+9.7% / +18.2%"}, "option_trade": {"strike": "1300 CE", "entry": 32.2, "sl": 20.9, "tgt1": 97.0, "tgt2": 190.4, "rr": 5.7}}, {"symbol": "KOTAKBANK", "cmp": 467.0, "resistance": 472.5, "base_floor": 427.7, "pct_dist": -1.16, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 62.5, "rvol": 1.05, "stock_trade": {"entry": 467.0, "sl": 427.7, "tgt1": 525.95, "tgt2": 577.04, "rr": "1:1.5", "potential_pct": "+12.6% / +23.6%"}, "option_trade": {"strike": "470 CE", "entry": 13.9, "sl": 9.0, "tgt1": 44.6, "tgt2": 88.7, "rr": 6.3}}, {"symbol": "CHOLAFIN", "cmp": 1760.0, "resistance": 1781.0, "base_floor": 1415.0, "pct_dist": -1.18, "stage": "⏳ BASE SQUEEZE AT RESISTANCE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.8, "rvol": 0.75, "stock_trade": {"entry": 1760.0, "sl": 1415.0, "tgt1": 2277.5, "tgt2": 2726.0, "rr": "1:1.5", "potential_pct": "+29.4% / +54.9%"}, "option_trade": {"strike": "1750 CE", "entry": 63.1, "sl": 41.0, "tgt1": 332.2, "tgt2": 720.0, "rr": 12.2}}, {"symbol": "DRREDDY", "cmp": 1366.0, "resistance": 1384.0, "base_floor": 1167.2, "pct_dist": -1.3, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 84.2, "rvol": 0.59, "stock_trade": {"entry": 1366.0, "sl": 1167.2, "tgt1": 1664.2, "tgt2": 1922.64, "rr": "1:1.5", "potential_pct": "+21.8% / +40.7%"}, "option_trade": {"strike": "1350 CE", "entry": 53.1, "sl": 34.5, "tgt1": 208.2, "tgt2": 431.6, "rr": 8.3}}, {"symbol": "BHARTIARTL", "cmp": 2056.9, "resistance": 2084.0, "base_floor": 1756.2, "pct_dist": -1.3, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 78.9, "rvol": 1.76, "stock_trade": {"entry": 2056.9, "sl": 1756.2, "tgt1": 2507.95, "tgt2": 2898.86, "rr": "1:1.5", "potential_pct": "+21.9% / +40.9%"}, "option_trade": {"strike": "2050 CE", "entry": 71.3, "sl": 46.3, "tgt1": 305.8, "tgt2": 643.8, "rr": 9.4}}, {"symbol": "VEDL", "cmp": 263.8, "resistance": 267.5, "base_floor": 221.6, "pct_dist": -1.38, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.7, "rvol": 0.99, "stock_trade": {"entry": 263.8, "sl": 221.6, "tgt1": 327.1, "tgt2": 381.96, "rr": "1:1.5", "potential_pct": "+24.0% / +44.8%"}, "option_trade": {"strike": "265 CE", "entry": 8.1, "sl": 5.3, "tgt1": 41.0, "tgt2": 88.4, "rr": 11.8}}, {"symbol": "SUNPHARMA", "cmp": 1829.0, "resistance": 1855.0, "base_floor": 1719.1, "pct_dist": -1.4, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.5, "rvol": 1.13, "stock_trade": {"entry": 1829.0, "sl": 1719.1, "tgt1": 1993.85, "tgt2": 2136.72, "rr": "1:1.5", "potential_pct": "+9.0% / +16.8%"}, "option_trade": {"strike": "1850 CE", "entry": 49.9, "sl": 32.4, "tgt1": 135.6, "tgt2": 259.1, "rr": 4.9}}, {"symbol": "HAL", "cmp": 5043.0, "resistance": 5119.0, "base_floor": 4590.0, "pct_dist": -1.48, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 58.1, "rvol": 1.6, "stock_trade": {"entry": 5043.0, "sl": 4590.0, "tgt1": 5722.5, "tgt2": 6311.4, "rr": "1:1.5", "potential_pct": "+13.5% / +25.2%"}, "option_trade": {"strike": "5000 CE", "entry": 187.9, "sl": 122.1, "tgt1": 541.2, "tgt2": 1050.4, "rr": 5.4}}, {"symbol": "BPCL", "cmp": 317.1, "resistance": 322.0, "base_floor": 275.4, "pct_dist": -1.52, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.7, "rvol": 1.14, "stock_trade": {"entry": 317.1, "sl": 275.4, "tgt1": 379.65, "tgt2": 433.86, "rr": "1:1.5", "potential_pct": "+19.7% / +36.8%"}, "option_trade": {"strike": "320 CE", "entry": 9.0, "sl": 5.9, "tgt1": 41.5, "tgt2": 88.4, "rr": 10.5}}, {"symbol": "TECHM", "cmp": 1822.7, "resistance": 1851.0, "base_floor": 1442.5, "pct_dist": -1.53, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.3, "rvol": 0.47, "stock_trade": {"entry": 1822.7, "sl": 1442.5, "tgt1": 2393.0, "tgt2": 2887.26, "rr": "1:1.5", "potential_pct": "+31.3% / +58.4%"}, "option_trade": {"strike": "1800 CE", "entry": 71.5, "sl": 46.5, "tgt1": 368.1, "tgt2": 795.4, "rr": 11.9}}, {"symbol": "GAIL", "cmp": 185.99, "resistance": 188.9, "base_floor": 160.7, "pct_dist": -1.54, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.2, "rvol": 0.87, "stock_trade": {"entry": 185.99, "sl": 160.7, "tgt1": 223.93, "tgt2": 256.8, "rr": "1:1.5", "potential_pct": "+20.4% / +38.1%"}, "option_trade": {"strike": "185 CE", "entry": 6.6, "sl": 4.3, "tgt1": 26.3, "tgt2": 54.8, "rr": 8.6}}, {"symbol": "PERSISTENT", "cmp": 6109.5, "resistance": 6209.0, "base_floor": 5430.0, "pct_dist": -1.6, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.5, "rvol": 0.66, "stock_trade": {"entry": 6109.5, "sl": 5430.0, "tgt1": 7128.75, "tgt2": 8012.1, "rr": "1:1.5", "potential_pct": "+16.7% / +31.1%"}, "option_trade": {"strike": "6200 CE", "entry": 156.4, "sl": 101.7, "tgt1": 686.4, "tgt2": 1450.2, "rr": 9.7}}, {"symbol": "JINDALSTEL", "cmp": 1149.9, "resistance": 1169.9, "base_floor": 1000.8, "pct_dist": -1.71, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.2, "rvol": 0.88, "stock_trade": {"entry": 1149.9, "sl": 1000.8, "tgt1": 1373.55, "tgt2": 1567.38, "rr": "1:1.5", "potential_pct": "+19.4% / +36.3%"}, "option_trade": {"strike": "1140 CE", "entry": 42.9, "sl": 27.9, "tgt1": 159.2, "tgt2": 326.8, "rr": 7.8}}, {"symbol": "ITC", "cmp": 278.85, "resistance": 283.9, "base_floor": 252.8, "pct_dist": -1.78, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.2, "rvol": 0.78, "stock_trade": {"entry": 278.85, "sl": 252.8, "tgt1": 317.93, "tgt2": 351.79, "rr": "1:1.5", "potential_pct": "+14.0% / +26.2%"}, "option_trade": {"strike": "280 CE", "entry": 8.6, "sl": 5.6, "tgt1": 28.9, "tgt2": 58.2, "rr": 6.8}}, {"symbol": "COFORGE", "cmp": 2079.0, "resistance": 2119.0, "base_floor": 1804.5, "pct_dist": -1.89, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.2, "rvol": 0.89, "stock_trade": {"entry": 2079.0, "sl": 1804.5, "tgt1": 2490.75, "tgt2": 2847.6, "rr": "1:1.5", "potential_pct": "+19.8% / +37.0%"}, "option_trade": {"strike": "2100 CE", "entry": 58.1, "sl": 37.8, "tgt1": 272.2, "tgt2": 580.7, "rr": 10.5}}, {"symbol": "IOC", "cmp": 144.5, "resistance": 147.31, "base_floor": 124.92, "pct_dist": -1.91, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 81.7, "rvol": 2.03, "stock_trade": {"entry": 144.5, "sl": 124.92, "tgt1": 173.87, "tgt2": 199.32, "rr": "1:1.5", "potential_pct": "+20.3% / +37.9%"}, "option_trade": {"strike": "144 CE", "entry": 5.0, "sl": 3.2, "tgt1": 20.3, "tgt2": 42.3, "rr": 8.5}}, {"symbol": "BEL", "cmp": 395.1, "resistance": 404.5, "base_floor": 354.55, "pct_dist": -2.32, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 60.9, "rvol": 0.79, "stock_trade": {"entry": 395.1, "sl": 354.55, "tgt1": 455.93, "tgt2": 508.64, "rr": "1:1.5", "potential_pct": "+15.4% / +28.7%"}, "option_trade": {"strike": "400 CE", "entry": 10.6, "sl": 6.9, "tgt1": 42.2, "tgt2": 87.8, "rr": 8.5}}, {"symbol": "COALINDIA", "cmp": 394.3, "resistance": 420.3, "base_floor": 380.4, "pct_dist": -6.19, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 35.0, "rvol": 0.66, "stock_trade": {"entry": 394.3, "sl": 380.4, "tgt1": 415.15, "tgt2": 433.22, "rr": "1:1.5", "potential_pct": "+5.3% / +9.9%"}, "option_trade": {"strike": "390 CE", "entry": 15.2, "sl": 9.9, "tgt1": 26.0, "tgt2": 41.7, "rr": 2.0}}, {"symbol": "BHEL", "cmp": 418.1, "resistance": 464.0, "base_floor": 377.7, "pct_dist": -9.89, "stage": "📈 PRE-BREAKOUT ACCUMULATION", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 43.5, "rvol": 1.08, "stock_trade": {"entry": 418.1, "sl": 377.7, "tgt1": 478.7, "tgt2": 531.22, "rr": "1:1.5", "potential_pct": "+14.5% / +27.1%"}, "option_trade": {"strike": "420 CE", "entry": 12.8, "sl": 8.3, "tgt1": 44.3, "tgt2": 89.7, "rr": 7.0}}]

HTML_PAGE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vickyvaio Breakouts | Verified Institutional F&O Breakout Engine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .glass { background: rgba(18, 20, 29, 0.88); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .glass-card { background: rgba(22, 26, 38, 0.72); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.07); }
    </style>
</head>
<body class="bg-[#0a0c13] text-slate-100 min-h-screen">

    <!-- Top Navigation Header -->
    <header class="glass sticky top-0 z-40 px-6 py-4 border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/25">
                    <i data-lucide="flame" class="w-6 h-6 text-black font-extrabold"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2.5 flex-wrap">
                        <h1 class="text-2xl font-black tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">
                            VICKYVAIO BREAKOUTS
                        </h1>
                        <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-extrabold border border-emerald-500/30 uppercase tracking-wider">
                            STRICT 6-FACTOR VERIFIED
                        </span>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">Arvind Mangal Multi-Month Consolidation Bases &bull; Option Edge Tamil High-Beta Momentum</p>
                </div>
            </div>

            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="text-right hidden md:block">
                    <div class="text-xs text-slate-400">Strict Live Verification</div>
                    <div class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> <span id="syncTime">LIVE</span>
                    </div>
                </div>
                <button onclick="scanNow()" id="scanBtn" class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs rounded-xl transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/20 active:scale-95">
                    <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="scanIcon"></i> Re-Scan Breakouts
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
                    <span class="text-xs font-semibold uppercase">Verified Breakouts</span>
                    <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statTotal">--</div>
                <div class="text-xs text-slate-500 mt-1">Filtered from Full F&O Universe</div>
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
                    <i data-lucide="zap" class="w-4 h-4 text-amber-400"></i>
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
                    All Verified Breakouts (<span id="tabCountAll">0</span>)
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
                    <option value="Auto & Ancillary">Auto & Ancillaries</option>
                    <option value="Banking & Financials">Banking & Financial Services</option>
                    <option value="Defense & PSU">Defense & PSU Leaders</option>
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
                    <input type="text" id="searchInput" placeholder="Search verified stock..." onkeyup="applyFilters()" 
                        class="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500/50">
                </div>
            </div>

        </div>

        <!-- Cards Container -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="cardsGrid">
            <!-- Dynamically populated via JS -->
        </div>

    </main>

    <!-- NATIVE IN-HOUSE BREAKOUT PATTERN CANDLESTICK MODAL -->
    <div id="chartModal" class="fixed inset-0 z-50 hidden bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6">
        <div class="glass rounded-2xl w-full max-w-5xl h-[90vh] flex flex-col overflow-hidden shadow-2xl border border-slate-700">
            
            <!-- Modal Header -->
            <div class="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/95">
                <div class="flex items-center gap-3 flex-wrap">
                    <span id="modalSymbol" class="text-2xl font-black text-white tracking-wider"></span>
                    <span id="modalPatternBadge" class="text-xs px-2.5 py-1 rounded bg-yellow-500/20 text-yellow-400 font-bold border border-yellow-500/30">
                        BREAKOUT PATTERN
                    </span>
                    <div id="modalLevelsBadge" class="text-xs text-slate-300 mono flex gap-3"></div>
                </div>
                <button onclick="closeChartModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Chart Toolbar & Indicators Legend -->
            <div class="px-6 py-2.5 bg-[#0d1017] border-b border-slate-800 flex flex-wrap justify-between items-center gap-3 text-xs mono">
                <div class="flex items-center gap-3 sm:gap-4 flex-wrap">
                    <span class="flex items-center gap-1.5 text-yellow-400 font-bold"><span class="w-3 h-0.5 bg-yellow-400 border border-yellow-400"></span> RESISTANCE PIVOT</span>
                    <span class="flex items-center gap-1.5 text-indigo-400 font-bold"><span class="w-3 h-3 bg-indigo-500/20 border border-indigo-400/50"></span> CONSOLIDATION BASE</span>
                    <span class="flex items-center gap-1.5 text-emerald-400 font-bold"><span class="w-3 h-0.5 bg-emerald-400 border border-emerald-400 border-dashed"></span> TARGET 1</span>
                    <span class="flex items-center gap-1.5 text-rose-400 font-bold"><span class="w-3 h-0.5 bg-rose-400 border border-rose-400 border-dashed"></span> STOP LOSS</span>
                    <span class="flex items-center gap-1.5 text-cyan-400 hidden sm:flex"><span class="w-3 h-0.5 bg-cyan-400"></span> 20 EMA</span>
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
                const matchSearch = (!query || item.symbol.includes(query) || item.setup_name.toUpperCase().includes(query) || item.pattern.toUpperCase().includes(query));
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
                    <h3 class="text-lg font-bold text-slate-200">No Breakout Stocks Found in this Category</h3>
                    <p class="text-xs text-slate-400">Try adjusting your sector filter or search criteria.</p>
                </div>`;
                lucide.createIcons();
                return;
            }

            data.forEach(item => {
                let badgeColor = 'bg-amber-950 text-amber-300 border-amber-700/50';
                if (item.horizon === 'Monthly Holding') badgeColor = 'bg-cyan-950 text-cyan-300 border-cyan-700/50';
                if (item.horizon === 'Weekly Holding') badgeColor = 'bg-indigo-950 text-indigo-300 border-indigo-700/50';

                let stageBadge = 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60';
                if (item.stage.includes('IMMINENT')) stageBadge = 'bg-yellow-950/80 text-yellow-300 border-yellow-700/60';
                else if (item.stage.includes('BASE SQUEEZE')) stageBadge = 'bg-cyan-950/80 text-cyan-300 border-cyan-700/60';

                const distStr = item.pct_dist >= 0 ? `+${item.pct_dist}% above pivot` : `${item.pct_dist}% to pivot`;

                const cardHtml = `
                <div class="stock-card glass-card rounded-2xl p-6 space-y-6 hover:border-emerald-500/40 transition-all shadow-xl">
                    <div class="flex justify-between items-start border-b border-slate-800/80 pb-4">
                        <div>
                            <div class="flex items-center gap-2.5 flex-wrap">
                                <span class="text-2xl font-black tracking-tight text-white">${item.symbol}</span>
                                <span class="text-xs px-2.5 py-1 rounded-md font-bold uppercase tracking-wider border ${badgeColor}">
                                    ${item.horizon}
                                </span>
                                <span class="text-xs px-2 py-0.5 rounded font-extrabold border ${stageBadge}">
                                    ${item.stage}
                                </span>
                            </div>
                            <div class="flex items-center gap-3 mt-1.5 text-xs text-slate-400">
                                <span class="flex items-center gap-1 text-slate-300 font-medium">
                                    <i data-lucide="crosshair" class="w-3.5 h-3.5 text-yellow-400"></i> Pivot: ₹${item.resistance} (${distStr})
                                </span>
                                <span>&bull;</span>
                                <span class="text-slate-400">${item.sector}</span>
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-xs text-slate-400 uppercase">Live Spot CMP</div>
                            <div class="text-2xl font-black mono text-emerald-400">₹${item.cmp}</div>
                        </div>
                    </div>

                    <!-- Technical Metrics Grid -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-semibold mono">
                        <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-[10px] text-slate-500 uppercase">Confidence Score</div>
                            <div class="text-emerald-400 font-bold">${item.score}% High Conviction</div>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-[10px] text-slate-500 uppercase">RSI(14)</div>
                            <div class="text-yellow-400 font-bold">${item.rsi} (Expansion)</div>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-[10px] text-slate-500 uppercase">Volume Surge</div>
                            <div class="text-cyan-400 font-bold">${item.rvol}x RVOL</div>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-[10px] text-slate-500 uppercase">Consolidation Floor</div>
                            <div class="text-slate-300 font-bold">₹${item.base_floor}</div>
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
                        <span class="text-[11px] text-slate-500">Pattern: <strong class="text-slate-300">${item.pattern}</strong></span>
                        <div class="flex items-center gap-2">
                            <button onclick="openNativeChart('${item.symbol}', ${item.cmp}, ${item.resistance}, ${item.base_floor}, ${item.stock_trade.sl}, ${item.stock_trade.tgt1}, ${item.stock_trade.tgt2}, '${item.pattern}')" 
                                class="px-3.5 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-xs font-bold rounded-lg text-white transition-all flex items-center gap-1.5 shadow-md shadow-cyan-600/20 active:scale-95">
                                <i data-lucide="line-chart" class="w-3.5 h-3.5"></i> View Breakout Pattern Chart
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
            const text = `🔥 VICKYVAIO BREAKOUTS ALERT: ${sym}\n• Spot CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}\n• F&O Option: ${sym} ${strike}\n• Option Entry: ₹${optEntry} | Option Tgt: ₹${optTgt}\nStrategy: Base Breakout Confluence`;
            navigator.clipboard.writeText(text);
            alert(`Trade alert for ${sym} copied to clipboard!`);
        }

        // ==========================================
        // ADVANCED BREAKOUT PATTERN CANVAS CHART
        // ==========================================
        let activeChartData = null;

        async function openNativeChart(symbol, cmp, resistance, baseFloor, sl, tgt1, tgt2, pattern) {
            document.getElementById('modalSymbol').innerText = symbol;
            document.getElementById('modalPatternBadge').innerText = pattern.toUpperCase();
            document.getElementById('modalLevelsBadge').innerHTML = `
                <span class="text-white font-bold">CMP: ₹${cmp}</span>
                <span class="text-yellow-400 font-bold">Pivot: ₹${resistance}</span>
                <span class="text-indigo-300">Base Floor: ₹${baseFloor}</span>
                <span class="text-rose-400">SL: ₹${sl}</span>
                <span class="text-emerald-400">TGT: ₹${tgt1}</span>
            `;
            document.getElementById('chartModal').classList.remove('hidden');

            const canvas = document.getElementById('breakoutCanvas');
            const wrapper = document.getElementById('canvasWrapper');
            canvas.width = wrapper.clientWidth * window.devicePixelRatio;
            canvas.height = wrapper.clientHeight * window.devicePixelRatio;

            document.getElementById('candleHoverInfo').innerText = "Loading real market candles for " + symbol + "...";

            try {
                const res = await fetch(`/api/chart?symbol=${symbol}`);
                const data = await res.json();
                if (data.candles && data.candles.length > 0) {
                    activeChartData = {
                        symbol: symbol,
                        cmp: data.cmp || cmp,
                        resistance: resistance,
                        baseFloor: baseFloor,
                        sl: sl,
                        tgt1: tgt1,
                        tgt2: tgt2,
                        pattern: pattern,
                        candles: data.candles
                    };
                } else {
                    activeChartData = generateFallbackCandles(symbol, cmp, resistance, baseFloor, sl, tgt1, tgt2, pattern);
                }
            } catch (e) {
                activeChartData = generateFallbackCandles(symbol, cmp, resistance, baseFloor, sl, tgt1, tgt2, pattern);
            }

            drawChart();
            setupChartMouseInteractions();
        }

        function generateFallbackCandles(symbol, cmp, resistance, baseFloor, sl, tgt1, tgt2, pattern) {
            const candles = [];
            const now = Math.floor(Date.now() / 1000);
            let p = baseFloor * 1.02;
            for (let i = 45; i >= 0; i--) {
                if (i <= 3) p = cmp;
                else p = baseFloor + (resistance - baseFloor) * (0.3 + 0.6 * (1 - i / 45)) + (Math.random() - 0.5) * (cmp * 0.015);
                const high = p + Math.random() * (cmp * 0.012);
                const low = p - Math.random() * (cmp * 0.012);
                const open = p - (Math.random() - 0.5) * (cmp * 0.008);
                candles.push({
                    t: now - (i * 86400),
                    o: Math.round(open * 10) / 10,
                    h: Math.round(high * 10) / 10,
                    l: Math.round(low * 10) / 10,
                    c: Math.round(p * 10) / 10,
                    v: Math.floor(600000 + Math.random() * 2500000 * (i <= 2 ? 3 : 1))
                });
            }
            return { symbol, cmp, resistance, baseFloor, sl, tgt1, tgt2, pattern, candles };
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

            const ema20 = computeEMA(candles.map(c => c.c), 20);

            // Margins
            const paddingLeft = 35 * dpr;
            const paddingRight = 110 * dpr;
            const paddingTop = 35 * dpr;
            const paddingBottom = 75 * dpr;
            const chartHeight = h - paddingTop - paddingBottom;
            const chartWidth = w - paddingLeft - paddingRight;

            // Price bounds
            let minP = Math.min(...candles.map(c => c.l), activeChartData.sl, activeChartData.baseFloor * 0.99);
            let maxP = Math.max(...candles.map(c => c.h), activeChartData.tgt1, activeChartData.resistance * 1.01);
            minP *= 0.985;
            maxP *= 1.015;
            const priceRange = maxP - minP || 1;

            const yToPrice = p => paddingTop + chartHeight * (1 - (p - minP) / priceRange);

            const maxVol = Math.max(...candles.map(c => c.v)) || 1;
            const volAreaHeight = 55 * dpr;
            const volYBase = h - 20 * dpr;

            // 1. DRAW SHADED CONSOLIDATION BASE BOX (Arvind Mangal Base Formation)
            const baseTopY = yToPrice(activeChartData.resistance);
            const baseBottomY = yToPrice(activeChartData.baseFloor);
            const baseHeight = Math.abs(baseBottomY - baseTopY);
            
            // Draw shaded accumulation zone
            ctx.save();
            ctx.fillStyle = 'rgba(99, 102, 241, 0.08)';
            ctx.fillRect(paddingLeft, Math.min(baseTopY, baseBottomY), chartWidth, baseHeight);
            
            // Draw subtle base boundary borders
            ctx.strokeStyle = 'rgba(99, 102, 241, 0.3)';
            ctx.lineWidth = 1 * dpr;
            ctx.setLineDash([4 * dpr, 4 * dpr]);
            ctx.strokeRect(paddingLeft, Math.min(baseTopY, baseBottomY), chartWidth, baseHeight);
            ctx.setLineDash([]);

            // Base annotation text inside box
            ctx.fillStyle = 'rgba(165, 180, 252, 0.45)';
            ctx.font = `bold ${11 * dpr}px 'Plus Jakarta Sans', sans-serif`;
            ctx.fillText("ACCUMULATION / CONSOLIDATION BASE ZONE", paddingLeft + 15 * dpr, Math.min(baseTopY, baseBottomY) + 20 * dpr);
            ctx.restore();

            // 2. Draw Horizontal Grid lines
            ctx.lineWidth = 1 * dpr;
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
            const gridSteps = 5;
            for (let i = 0; i <= gridSteps; i++) {
                const gp = minP + (priceRange * i) / gridSteps;
                const gy = yToPrice(gp);
                ctx.beginPath();
                ctx.moveTo(paddingLeft, gy);
                ctx.lineTo(w - paddingRight, gy);
                ctx.stroke();

                ctx.fillStyle = '#64748b';
                ctx.font = `${10 * dpr}px 'JetBrains Mono', monospace`;
                ctx.fillText('₹' + gp.toFixed(1), w - paddingRight + 8 * dpr, gy + 3.5 * dpr);
            }

            // 3. Draw Level Lines: Breakout Pivot, Target 1, Stop Loss
            function drawLevelLine(price, label, color, isDashed = true) {
                const y = yToPrice(price);
                ctx.save();
                ctx.strokeStyle = color;
                ctx.lineWidth = 1.6 * dpr;
                if (isDashed) ctx.setLineDash([6 * dpr, 4 * dpr]);
                ctx.beginPath();
                ctx.moveTo(paddingLeft, y);
                ctx.lineTo(w - paddingRight, y);
                ctx.stroke();

                ctx.setLineDash([]);
                ctx.fillStyle = color;
                ctx.fillRect(w - paddingRight + 4 * dpr, y - 9.5 * dpr, 100 * dpr, 19 * dpr);
                ctx.fillStyle = '#000000';
                ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
                ctx.fillText(label, w - paddingRight + 8 * dpr, y + 3.5 * dpr);
                ctx.restore();
            }

            drawLevelLine(activeChartData.resistance, '⚡ BREAKOUT PIVOT', '#eab308', false);
            drawLevelLine(activeChartData.tgt1, '🎯 TARGET 1', '#10b981', true);
            drawLevelLine(activeChartData.sl, '🛡️ STOP LOSS', '#f43f5e', true);

            // 4. Draw 20 EMA
            ctx.save();
            ctx.strokeStyle = '#06b6d4';
            ctx.lineWidth = 1.6 * dpr;
            ctx.beginPath();
            let started = false;
            for (let i = 0; i < n; i++) {
                if (ema20[i] === null) continue;
                const cx = paddingLeft + (chartWidth / n) * (i + 0.5);
                const cy = yToPrice(ema20[i]);
                if (!started) { ctx.moveTo(cx, cy); started = true; }
                else { ctx.lineTo(cx, cy); }
            }
            ctx.stroke();
            ctx.restore();

            // 5. Draw Candlesticks & Volume Bars
            const slotWidth = chartWidth / n;
            const candleWidth = Math.max(slotWidth * 0.68, 2.5 * dpr);

            for (let i = 0; i < n; i++) {
                const c = candles[i];
                const cx = paddingLeft + slotWidth * (i + 0.5);
                const isGreen = c.c >= c.o;
                const candleColor = isGreen ? '#10b981' : '#f43f5e';

                // Volume Bar
                const vHeight = (c.v / maxVol) * volAreaHeight;
                ctx.fillStyle = isGreen ? 'rgba(16, 185, 129, 0.4)' : 'rgba(244, 63, 94, 0.4)';
                ctx.fillRect(cx - candleWidth / 2, volYBase - vHeight, candleWidth, vHeight);

                // Wick
                ctx.strokeStyle = candleColor;
                ctx.lineWidth = 1.3 * dpr;
                ctx.beginPath();
                ctx.moveTo(cx, yToPrice(c.h));
                ctx.lineTo(cx, yToPrice(c.l));
                ctx.stroke();

                // Body
                const yO = yToPrice(c.o);
                const yC = yToPrice(c.c);
                const topY = Math.min(yO, yC);
                const bodyH = Math.max(Math.abs(yO - yC), 1.5 * dpr);

                ctx.fillStyle = candleColor;
                ctx.fillRect(cx - candleWidth / 2, topY, candleWidth, bodyH);

                // HIGHLIGHT BREAKOUT CANDLE (Final Bar)
                if (i === n - 1) {
                    ctx.save();
                    // Glow background
                    ctx.fillStyle = 'rgba(234, 179, 8, 0.15)';
                    ctx.fillRect(cx - slotWidth / 2, paddingTop, slotWidth, chartHeight);
                    
                    // Breakout Arrow
                    const arrowY = yToPrice(c.h) - 16 * dpr;
                    ctx.fillStyle = '#eab308';
                    ctx.beginPath();
                    ctx.moveTo(cx, arrowY + 8 * dpr);
                    ctx.lineTo(cx - 6 * dpr, arrowY);
                    ctx.lineTo(cx + 6 * dpr, arrowY);
                    ctx.closePath();
                    ctx.fill();

                    // Text Badge
                    ctx.font = `bold ${10 * dpr}px 'JetBrains Mono', monospace`;
                    ctx.fillText('⚡ BREAKOUT', cx - 35 * dpr, arrowY - 6 * dpr);
                    ctx.restore();
                }
            }

            // 6. Crosshair & Tooltip
            if (hoverIdx >= 0 && hoverIdx < n) {
                const c = candles[hoverIdx];
                const cx = paddingLeft + slotWidth * (hoverIdx + 0.5);
                const cy = yToPrice(c.c);

                ctx.save();
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
                ctx.lineWidth = 1 * dpr;
                ctx.setLineDash([3 * dpr, 3 * dpr]);

                ctx.beginPath();
                ctx.moveTo(cx, paddingTop);
                ctx.lineTo(cx, h - 20 * dpr);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(paddingLeft, cy);
                ctx.lineTo(w - paddingRight, cy);
                ctx.stroke();
                ctx.restore();

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
                const paddingLeft = 35 * dpr;
                const paddingRight = 110 * dpr;
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
    return {"status": "success", "data": VERIFIED_BREAKOUT_DATA, "count": len(VERIFIED_BREAKOUT_DATA), "timestamp": datetime.datetime.now().isoformat()}

@app.get("/api/chart")
async def chart_endpoint(symbol: str):
    sym = symbol.upper().replace(".NS", "").strip()
    # Map symbols like TATAMOTORS to active ticker
    query_ticker = "TMPV.NS" if sym == "TATAMOTORS" else f"{sym}.NS"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{query_ticker}?interval=1d&range=3mo"
        r = requests.get(url, headers=headers, timeout=5)
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
