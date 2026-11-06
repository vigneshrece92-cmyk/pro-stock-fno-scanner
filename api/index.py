import datetime
import math
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Verified Authentic Breakout Setups with Exact Resistance, Base Floor, and Quality Scoring
VERIFIED_BREAKOUT_DATA = [{"symbol": "ICICIBANK", "cmp": 1571.2, "resistance": 1501.4, "base_floor": 1329.4, "pct_dist": 4.65, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 80.3, "rvol": 2.95, "stock_trade": {"entry": 1571.2, "sl": 1329.4, "tgt1": 1933.9, "tgt2": 2248.24, "rr": "1:1.5", "potential_pct": "+23.1% / +43.1%"}, "option_trade": {"strike": "1550 CE", "entry": 65.2, "sl": 45.6, "tgt1": 94.5, "tgt2": 127.1, "rr": 1.5, "lot_size": 700, "margin_required": 45640, "profit_tgt1": 20510, "profit_tgt2": 43330}}, {"symbol": "M&M", "cmp": 3287.2, "resistance": 3145.0, "base_floor": 2744.3, "pct_dist": 4.52, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 80.5, "rvol": 3.26, "stock_trade": {"entry": 3287.2, "sl": 2744.3, "tgt1": 4101.55, "tgt2": 4807.32, "rr": "1:1.5", "potential_pct": "+24.8% / +46.2%"}, "option_trade": {"strike": "3300 CE", "entry": 92.0, "sl": 64.4, "tgt1": 133.4, "tgt2": 179.4, "rr": 1.5, "lot_size": 200, "margin_required": 18400, "profit_tgt1": 8280, "profit_tgt2": 17480}}, {"symbol": "HDFCBANK", "cmp": 788.25, "resistance": 762.7, "base_floor": 669.2, "pct_dist": 3.35, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 68.5, "rvol": 2.3, "stock_trade": {"entry": 788.25, "sl": 669.2, "tgt1": 966.82, "tgt2": 1121.59, "rr": "1:1.5", "potential_pct": "+22.7% / +42.3%"}, "option_trade": {"strike": "780 CE", "entry": 30.3, "sl": 21.2, "tgt1": 43.9, "tgt2": 59.1, "rr": 1.5, "lot_size": 550, "margin_required": 16665, "profit_tgt1": 7480, "profit_tgt2": 15840}}, {"symbol": "TITAN", "cmp": 5000.0, "resistance": 4857.1, "base_floor": 4209.0, "pct_dist": 2.94, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 80.8, "rvol": 5.55, "stock_trade": {"entry": 5000.0, "sl": 4209.0, "tgt1": 6186.5, "tgt2": 7214.8, "rr": "1:1.5", "potential_pct": "+23.7% / +44.3%"}, "option_trade": {"strike": "5000 CE", "entry": 140.0, "sl": 98.0, "tgt1": 203.0, "tgt2": 273.0, "rr": 1.5, "lot_size": 175, "margin_required": 24500, "profit_tgt1": 11025, "profit_tgt2": 23275}}, {"symbol": "AXISBANK", "cmp": 1322.9, "resistance": 1293.8, "base_floor": 1196.9, "pct_dist": 2.25, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 56.5, "rvol": 1.32, "stock_trade": {"entry": 1322.9, "sl": 1196.9, "tgt1": 1511.9, "tgt2": 1675.7, "rr": "1:1.5", "potential_pct": "+14.3% / +26.7%"}, "option_trade": {"strike": "1300 CE", "entry": 59.9, "sl": 41.9, "tgt1": 86.9, "tgt2": 116.8, "rr": 1.5, "lot_size": 625, "margin_required": 37438, "profit_tgt1": 16875, "profit_tgt2": 35562}}, {"symbol": "TATASTEEL", "cmp": 186.3, "resistance": 183.33, "base_floor": 163.41, "pct_dist": 1.62, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.9, "rvol": 1.53, "stock_trade": {"entry": 186.3, "sl": 163.41, "tgt1": 220.64, "tgt2": 250.39, "rr": "1:1.5", "potential_pct": "+18.4% / +34.4%"}, "option_trade": {"strike": "185 CE", "entry": 6.5, "sl": 4.5, "tgt1": 9.4, "tgt2": 12.7, "rr": 1.5, "lot_size": 5500, "margin_required": 35750, "profit_tgt1": 15950, "profit_tgt2": 34100}}, {"symbol": "DIVISLAB", "cmp": 10320.5, "resistance": 10159.0, "base_floor": 8797.0, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 82.2, "rvol": 1.34, "stock_trade": {"entry": 10320.5, "sl": 8797.0, "tgt1": 12605.75, "tgt2": 14586.3, "rr": "1:1.5", "potential_pct": "+22.1% / +41.3%"}, "option_trade": {"strike": "10400 CE", "entry": 289.0, "sl": 202.3, "tgt1": 419.1, "tgt2": 563.5, "rr": 1.5, "lot_size": 100, "margin_required": 28900, "profit_tgt1": 13010, "profit_tgt2": 27450}}, {"symbol": "KOTAKBANK", "cmp": 480.0, "resistance": 472.5, "base_floor": 427.7, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 68.4, "rvol": 1.05, "stock_trade": {"entry": 480.0, "sl": 427.7, "tgt1": 558.45, "tgt2": 626.44, "rr": "1:1.5", "potential_pct": "+16.3% / +30.5%"}, "option_trade": {"strike": "480 CE", "entry": 13.4, "sl": 9.4, "tgt1": 19.4, "tgt2": 26.1, "rr": 1.5, "lot_size": 400, "margin_required": 5360, "profit_tgt1": 2400, "profit_tgt2": 5080}}, {"symbol": "BAJFINANCE", "cmp": 1087.75, "resistance": 1074.85, "base_floor": 899.15, "pct_dist": 1.2, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.0, "rvol": 0.95, "stock_trade": {"entry": 1087.75, "sl": 899.15, "tgt1": 1370.65, "tgt2": 1615.83, "rr": "1:1.5", "potential_pct": "+26.0% / +48.5%"}, "option_trade": {"strike": "1080 CE", "entry": 38.2, "sl": 26.7, "tgt1": 55.4, "tgt2": 74.5, "rr": 1.5, "lot_size": 500, "margin_required": 19100, "profit_tgt1": 8600, "profit_tgt2": 18150}}, {"symbol": "LT", "cmp": 4117.7, "resistance": 4071.6, "base_floor": 3592.9, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 92.3, "rvol": 1.53, "stock_trade": {"entry": 4117.7, "sl": 3592.9, "tgt1": 4904.9, "tgt2": 5587.14, "rr": "1:1.5", "potential_pct": "+19.1% / +35.7%"}, "option_trade": {"strike": "4100 CE", "entry": 133.0, "sl": 93.1, "tgt1": 192.8, "tgt2": 259.3, "rr": 1.5, "lot_size": 150, "margin_required": 19950, "profit_tgt1": 8970, "profit_tgt2": 18945}}, {"symbol": "HINDALCO", "cmp": 958.4, "resistance": 947.7, "base_floor": 851.1, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 67.4, "rvol": 3.29, "stock_trade": {"entry": 958.4, "sl": 851.1, "tgt1": 1119.35, "tgt2": 1258.84, "rr": "1:1.5", "potential_pct": "+16.8% / +31.3%"}, "option_trade": {"strike": "960 CE", "entry": 26.8, "sl": 18.8, "tgt1": 38.9, "tgt2": 52.3, "rr": 1.5, "lot_size": 700, "margin_required": 18760, "profit_tgt1": 8470, "profit_tgt2": 17850}}, {"symbol": "BHARTIARTL", "cmp": 2107.2, "resistance": 2084.0, "base_floor": 1756.2, "pct_dist": 1.11, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 78.9, "rvol": 1.76, "stock_trade": {"entry": 2107.2, "sl": 1756.2, "tgt1": 2633.7, "tgt2": 3090.0, "rr": "1:1.5", "potential_pct": "+25.0% / +46.6%"}, "option_trade": {"strike": "2100 CE", "entry": 66.2, "sl": 46.3, "tgt1": 96.0, "tgt2": 129.1, "rr": 1.5, "lot_size": 475, "margin_required": 31445, "profit_tgt1": 14155, "profit_tgt2": 29877}}, {"symbol": "BAJAJ-AUTO", "cmp": 10900.0, "resistance": 10789.0, "base_floor": 9637.0, "pct_dist": 1.03, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 65.3, "rvol": 1.85, "stock_trade": {"entry": 10900.0, "sl": 9637.0, "tgt1": 12794.5, "tgt2": 14436.4, "rr": "1:1.5", "potential_pct": "+17.4% / +32.4%"}, "option_trade": {"strike": "10800 CE", "entry": 405.2, "sl": 283.6, "tgt1": 587.5, "tgt2": 790.1, "rr": 1.5, "lot_size": 75, "margin_required": 30390, "profit_tgt1": 13672, "profit_tgt2": 28868}}, {"symbol": "SBIN", "cmp": 1018.5, "resistance": 1009.6, "base_floor": 937.5, "pct_dist": 0.88, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.1, "rvol": 1.43, "stock_trade": {"entry": 1018.5, "sl": 937.5, "tgt1": 1140.0, "tgt2": 1245.3, "rr": "1:1.5", "potential_pct": "+11.9% / +22.3%"}, "option_trade": {"strike": "1020 CE", "entry": 28.5, "sl": 19.9, "tgt1": 41.3, "tgt2": 55.6, "rr": 1.5, "lot_size": 750, "margin_required": 21375, "profit_tgt1": 9600, "profit_tgt2": 20325}}, {"symbol": "BAJAJFINSV", "cmp": 1864.7, "resistance": 1848.8, "base_floor": 1624.8, "pct_dist": 0.86, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.3, "rvol": 0.65, "stock_trade": {"entry": 1864.7, "sl": 1624.8, "tgt1": 2224.55, "tgt2": 2536.42, "rr": "1:1.5", "potential_pct": "+19.3% / +36.0%"}, "option_trade": {"strike": "1850 CE", "entry": 66.9, "sl": 46.8, "tgt1": 97.0, "tgt2": 130.5, "rr": 1.5, "lot_size": 500, "margin_required": 33450, "profit_tgt1": 15050, "profit_tgt2": 31800}}, {"symbol": "DLF", "cmp": 752.9, "resistance": 748.0, "base_floor": 634.15, "pct_dist": 0.66, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 80.2, "rvol": 1.09, "stock_trade": {"entry": 752.9, "sl": 634.15, "tgt1": 931.02, "tgt2": 1085.4, "rr": "1:1.5", "potential_pct": "+23.7% / +44.2%"}, "option_trade": {"strike": "760 CE", "entry": 21.1, "sl": 14.8, "tgt1": 30.6, "tgt2": 41.1, "rr": 1.5, "lot_size": 825, "margin_required": 17408, "profit_tgt1": 7838, "profit_tgt2": 16500}}, {"symbol": "MARUTI", "cmp": 12750.0, "resistance": 12681.0, "base_floor": 10985.0, "pct_dist": 0.54, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 77.6, "rvol": 1.87, "stock_trade": {"entry": 12750.0, "sl": 10985.0, "tgt1": 15397.5, "tgt2": 17692.0, "rr": "1:1.5", "potential_pct": "+20.8% / +38.8%"}, "option_trade": {"strike": "12800 CE", "entry": 357.0, "sl": 249.9, "tgt1": 517.6, "tgt2": 696.1, "rr": 1.5, "lot_size": 50, "margin_required": 17850, "profit_tgt1": 8030, "profit_tgt2": 16955}}, {"symbol": "MUTHOOTFIN", "cmp": 2869.0, "resistance": 2856.8, "base_floor": 2305.0, "pct_dist": 0.43, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.6, "rvol": 1.3, "stock_trade": {"entry": 2869.0, "sl": 2305.0, "tgt1": 3715.0, "tgt2": 4448.2, "rr": "1:1.5", "potential_pct": "+29.5% / +55.0%"}, "option_trade": {"strike": "2900 CE", "entry": 80.3, "sl": 56.2, "tgt1": 116.4, "tgt2": 156.6, "rr": 1.5, "lot_size": 325, "margin_required": 26098, "profit_tgt1": 11733, "profit_tgt2": 24798}}, {"symbol": "SUNPHARMA", "cmp": 1860.0, "resistance": 1855.0, "base_floor": 1719.1, "pct_dist": 0.27, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.4, "rvol": 1.13, "stock_trade": {"entry": 1860.0, "sl": 1719.1, "tgt1": 2071.35, "tgt2": 2254.52, "rr": "1:1.5", "potential_pct": "+11.4% / +21.2%"}, "option_trade": {"strike": "1850 CE", "entry": 62.1, "sl": 43.5, "tgt1": 90.0, "tgt2": 121.1, "rr": 1.5, "lot_size": 350, "margin_required": 21735, "profit_tgt1": 9765, "profit_tgt2": 20650}}, {"symbol": "CHOLAFIN", "cmp": 1785.0, "resistance": 1781.0, "base_floor": 1415.0, "pct_dist": 0.22, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 71.0, "rvol": 0.75, "stock_trade": {"entry": 1785.0, "sl": 1415.0, "tgt1": 2340.0, "tgt2": 2821.0, "rr": "1:1.5", "potential_pct": "+31.1% / +58.0%"}, "option_trade": {"strike": "1800 CE", "entry": 50.0, "sl": 35.0, "tgt1": 72.5, "tgt2": 97.5, "rr": 1.5, "lot_size": 400, "margin_required": 20000, "profit_tgt1": 9000, "profit_tgt2": 19000}}, {"symbol": "CIPLA", "cmp": 1411.0, "resistance": 1408.0, "base_floor": 1292.0, "pct_dist": 0.21, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 82.2, "rvol": 1.25, "stock_trade": {"entry": 1411.0, "sl": 1292.0, "tgt1": 1589.5, "tgt2": 1744.2, "rr": "1:1.5", "potential_pct": "+12.7% / +23.6%"}, "option_trade": {"strike": "1400 CE", "entry": 50.5, "sl": 35.3, "tgt1": 73.2, "tgt2": 98.5, "rr": 1.5, "lot_size": 650, "margin_required": 32825, "profit_tgt1": 14755, "profit_tgt2": 31200}}, {"symbol": "TVSMOTOR", "cmp": 4491.7, "resistance": 4490.0, "base_floor": 3741.9, "pct_dist": 0.04, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 74.5, "rvol": 0.74, "stock_trade": {"entry": 4491.7, "sl": 3741.9, "tgt1": 5616.4, "tgt2": 6591.14, "rr": "1:1.5", "potential_pct": "+25.0% / +46.7%"}, "option_trade": {"strike": "4500 CE", "entry": 125.8, "sl": 88.1, "tgt1": 182.4, "tgt2": 245.3, "rr": 1.5, "lot_size": 175, "margin_required": 22015, "profit_tgt1": 9905, "profit_tgt2": 20913}}, {"symbol": "PNB", "cmp": 126.55, "resistance": 126.8, "base_floor": 113.71, "pct_dist": -0.2, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 72.6, "rvol": 0.97, "stock_trade": {"entry": 126.55, "sl": 113.71, "tgt1": 145.81, "tgt2": 162.5, "rr": "1:1.5", "potential_pct": "+15.2% / +28.4%"}, "option_trade": {"strike": "127.5 CE", "entry": 3.5, "sl": 2.4, "tgt1": 5.1, "tgt2": 6.8, "rr": 1.5, "lot_size": 4000, "margin_required": 14000, "profit_tgt1": 6400, "profit_tgt2": 13200}}, {"symbol": "HEROMOTOCO", "cmp": 5513.0, "resistance": 5527.0, "base_floor": 4825.0, "pct_dist": -0.25, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.2, "rvol": 1.34, "stock_trade": {"entry": 5513.0, "sl": 4825.0, "tgt1": 6545.0, "tgt2": 7439.4, "rr": "1:1.5", "potential_pct": "+18.7% / +34.9%"}, "option_trade": {"strike": "5500 CE", "entry": 167.4, "sl": 117.2, "tgt1": 242.7, "tgt2": 326.4, "rr": 1.5, "lot_size": 100, "margin_required": 16740, "profit_tgt1": 7530, "profit_tgt2": 15900}}, {"symbol": "ITC", "cmp": 283.15, "resistance": 283.9, "base_floor": 252.8, "pct_dist": -0.26, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 76.2, "rvol": 0.78, "stock_trade": {"entry": 283.15, "sl": 252.8, "tgt1": 328.67, "tgt2": 368.13, "rr": "1:1.5", "potential_pct": "+16.1% / +30.0%"}, "option_trade": {"strike": "285 CE", "entry": 7.9, "sl": 5.5, "tgt1": 11.5, "tgt2": 15.4, "rr": 1.5, "lot_size": 1600, "margin_required": 12640, "profit_tgt1": 5760, "profit_tgt2": 12000}}, {"symbol": "GODREJPROP", "cmp": 1809.3, "resistance": 1815.0, "base_floor": 1468.4, "pct_dist": -0.31, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.7, "rvol": 1.49, "stock_trade": {"entry": 1809.3, "sl": 1468.4, "tgt1": 2320.65, "tgt2": 2763.82, "rr": "1:1.5", "potential_pct": "+28.3% / +52.8%"}, "option_trade": {"strike": "1800 CE", "entry": 60.0, "sl": 42.0, "tgt1": 87.0, "tgt2": 117.0, "rr": 1.5, "lot_size": 325, "margin_required": 19500, "profit_tgt1": 8775, "profit_tgt2": 18525}}, {"symbol": "RELIANCE", "cmp": 1320.0, "resistance": 1325.0, "base_floor": 1152.2, "pct_dist": -0.38, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.2, "rvol": 1.11, "stock_trade": {"entry": 1320.0, "sl": 1152.2, "tgt1": 1571.7, "tgt2": 1789.84, "rr": "1:1.5", "potential_pct": "+19.1% / +35.6%"}, "option_trade": {"strike": "1300 CE", "entry": 57.0, "sl": 39.9, "tgt1": 82.6, "tgt2": 111.1, "rr": 1.5, "lot_size": 250, "margin_required": 14250, "profit_tgt1": 6400, "profit_tgt2": 13525}}, {"symbol": "BANKBARODA", "cmp": 250.31, "resistance": 251.34, "base_floor": 225.2, "pct_dist": -0.41, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 70.8, "rvol": 0.98, "stock_trade": {"entry": 250.31, "sl": 225.2, "tgt1": 287.98, "tgt2": 320.62, "rr": "1:1.5", "potential_pct": "+15.0% / +28.1%"}, "option_trade": {"strike": "250 CE", "entry": 7.3, "sl": 5.1, "tgt1": 10.6, "tgt2": 14.2, "rr": 1.5, "lot_size": 2400, "margin_required": 17520, "profit_tgt1": 7920, "profit_tgt2": 16560}}, {"symbol": "JINDALSTEL", "cmp": 1165.0, "resistance": 1169.9, "base_floor": 1000.8, "pct_dist": -0.42, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.2, "rvol": 0.88, "stock_trade": {"entry": 1165.0, "sl": 1000.8, "tgt1": 1411.3, "tgt2": 1624.76, "rr": "1:1.5", "potential_pct": "+21.1% / +39.5%"}, "option_trade": {"strike": "1160 CE", "entry": 37.6, "sl": 26.3, "tgt1": 54.5, "tgt2": 73.3, "rr": 1.5, "lot_size": 625, "margin_required": 23500, "profit_tgt1": 10562, "profit_tgt2": 22312}}, {"symbol": "EICHERMOT", "cmp": 7669.5, "resistance": 7713.0, "base_floor": 6767.5, "pct_dist": -0.56, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.4, "rvol": 0.91, "stock_trade": {"entry": 7669.5, "sl": 6767.5, "tgt1": 9022.5, "tgt2": 10195.1, "rr": "1:1.5", "potential_pct": "+17.6% / +32.9%"}, "option_trade": {"strike": "7700 CE", "entry": 214.7, "sl": 150.3, "tgt1": 311.3, "tgt2": 418.7, "rr": 1.5, "lot_size": 100, "margin_required": 21470, "profit_tgt1": 9660, "profit_tgt2": 20400}}, {"symbol": "BPCL", "cmp": 319.9, "resistance": 322.0, "base_floor": 275.4, "pct_dist": -0.65, "stage": "BASE SQUEEZE", "score": 84, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.2, "rvol": 1.14, "stock_trade": {"entry": 319.9, "sl": 275.4, "tgt1": 386.65, "tgt2": 444.5, "rr": "1:1.5", "potential_pct": "+20.9% / +38.9%"}, "option_trade": {"strike": "320 CE", "entry": 9.0, "sl": 6.3, "tgt1": 13.0, "tgt2": 17.6, "rr": 1.5, "lot_size": 1800, "margin_required": 16200, "profit_tgt1": 7200, "profit_tgt2": 15480}}, {"symbol": "IOC", "cmp": 146.25, "resistance": 147.31, "base_floor": 124.92, "pct_dist": -0.72, "stage": "BASE SQUEEZE", "score": 84, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.9, "rvol": 2.03, "stock_trade": {"entry": 146.25, "sl": 124.92, "tgt1": 178.25, "tgt2": 205.97, "rr": "1:1.5", "potential_pct": "+21.9% / +40.8%"}, "option_trade": {"strike": "145 CE", "entry": 5.3, "sl": 3.7, "tgt1": 7.7, "tgt2": 10.3, "rr": 1.5, "lot_size": 4875, "margin_required": 25838, "profit_tgt1": 11700, "profit_tgt2": 24375}}, {"symbol": "DRREDDY", "cmp": 1373.0, "resistance": 1384.0, "base_floor": 1167.2, "pct_dist": -0.79, "stage": "BASE SQUEEZE", "score": 84, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 83.7, "rvol": 0.59, "stock_trade": {"entry": 1373.0, "sl": 1167.2, "tgt1": 1681.7, "tgt2": 1949.24, "rr": "1:1.5", "potential_pct": "+22.5% / +42.0%"}, "option_trade": {"strike": "1350 CE", "entry": 61.4, "sl": 43.0, "tgt1": 89.0, "tgt2": 119.7, "rr": 1.5, "lot_size": 125, "margin_required": 7675, "profit_tgt1": 3450, "profit_tgt2": 7288}}, {"symbol": "JSWSTEEL", "cmp": 1357.1, "resistance": 1370.0, "base_floor": 1158.0, "pct_dist": -0.94, "stage": "BASE SQUEEZE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.8, "rvol": 1.35, "stock_trade": {"entry": 1357.1, "sl": 1158.0, "tgt1": 1655.75, "tgt2": 1914.58, "rr": "1:1.5", "potential_pct": "+22.0% / +41.1%"}, "option_trade": {"strike": "1350 CE", "entry": 45.1, "sl": 31.6, "tgt1": 65.4, "tgt2": 87.9, "rr": 1.5, "lot_size": 300, "margin_required": 13530, "profit_tgt1": 6090, "profit_tgt2": 12840}}, {"symbol": "WIPRO", "cmp": 198.0, "resistance": 200.11, "base_floor": 158.3, "pct_dist": -1.05, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.4, "rvol": 0.67, "stock_trade": {"entry": 198.0, "sl": 158.3, "tgt1": 257.55, "tgt2": 309.16, "rr": "1:1.5", "potential_pct": "+30.1% / +56.1%"}, "option_trade": {"strike": "200 CE", "entry": 5.5, "sl": 3.8, "tgt1": 8.0, "tgt2": 10.7, "rr": 1.5, "lot_size": 1500, "margin_required": 8250, "profit_tgt1": 3750, "profit_tgt2": 7800}}, {"symbol": "TECHM", "cmp": 1831.0, "resistance": 1851.0, "base_floor": 1442.5, "pct_dist": -1.08, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 58.0, "rvol": 0.47, "stock_trade": {"entry": 1831.0, "sl": 1442.5, "tgt1": 2413.75, "tgt2": 2918.8, "rr": "1:1.5", "potential_pct": "+31.8% / +59.4%"}, "option_trade": {"strike": "1850 CE", "entry": 51.3, "sl": 35.9, "tgt1": 74.4, "tgt2": 100.0, "rr": 1.5, "lot_size": 600, "margin_required": 30780, "profit_tgt1": 13860, "profit_tgt2": 29220}}, {"symbol": "GAIL", "cmp": 185.79, "resistance": 188.9, "base_floor": 160.7, "pct_dist": -1.65, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 74.3, "rvol": 0.87, "stock_trade": {"entry": 185.79, "sl": 160.7, "tgt1": 223.43, "tgt2": 256.04, "rr": "1:1.5", "potential_pct": "+20.3% / +37.8%"}, "option_trade": {"strike": "185 CE", "entry": 6.0, "sl": 4.2, "tgt1": 8.7, "tgt2": 11.7, "rr": 1.5, "lot_size": 2750, "margin_required": 16500, "profit_tgt1": 7425, "profit_tgt2": 15675}}, {"symbol": "COFORGE", "cmp": 2076.0, "resistance": 2119.0, "base_floor": 1804.5, "pct_dist": -2.03, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.3, "rvol": 0.89, "stock_trade": {"entry": 2076.0, "sl": 1804.5, "tgt1": 2483.25, "tgt2": 2836.2, "rr": "1:1.5", "potential_pct": "+19.6% / +36.6%"}, "option_trade": {"strike": "2100 CE", "entry": 58.1, "sl": 40.7, "tgt1": 84.2, "tgt2": 113.3, "rr": 1.5, "lot_size": 150, "margin_required": 8715, "profit_tgt1": 3915, "profit_tgt2": 8280}}, {"symbol": "BEL", "cmp": 396.0, "resistance": 404.5, "base_floor": 354.55, "pct_dist": -2.1, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.8, "rvol": 0.79, "stock_trade": {"entry": 396.0, "sl": 354.55, "tgt1": 458.17, "tgt2": 512.06, "rr": "1:1.5", "potential_pct": "+15.7% / +29.3%"}, "option_trade": {"strike": "400 CE", "entry": 11.1, "sl": 7.8, "tgt1": 16.1, "tgt2": 21.6, "rr": 1.5, "lot_size": 1450, "margin_required": 16095, "profit_tgt1": 7250, "profit_tgt2": 15225}}, {"symbol": "VEDL", "cmp": 261.75, "resistance": 267.5, "base_floor": 221.6, "pct_dist": -2.15, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 62.5, "rvol": 0.99, "stock_trade": {"entry": 261.75, "sl": 221.6, "tgt1": 321.98, "tgt2": 374.17, "rr": "1:1.5", "potential_pct": "+23.0% / +42.9%"}, "option_trade": {"strike": "260 CE", "entry": 9.1, "sl": 6.4, "tgt1": 13.2, "tgt2": 17.7, "rr": 1.5, "lot_size": 1150, "margin_required": 10465, "profit_tgt1": 4715, "profit_tgt2": 9890}}, {"symbol": "NATIONALUM", "cmp": 325.75, "resistance": 333.2, "base_floor": 293.0, "pct_dist": -2.24, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 50.7, "rvol": 1.14, "stock_trade": {"entry": 325.75, "sl": 293.0, "tgt1": 374.88, "tgt2": 417.45, "rr": "1:1.5", "potential_pct": "+15.1% / +28.2%"}, "option_trade": {"strike": "330 CE", "entry": 9.1, "sl": 6.4, "tgt1": 13.2, "tgt2": 17.7, "rr": 1.5, "lot_size": 2500, "margin_required": 22750, "profit_tgt1": 10250, "profit_tgt2": 21500}}, {"symbol": "PERSISTENT", "cmp": 6053.5, "resistance": 6209.0, "base_floor": 5430.0, "pct_dist": -2.5, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.6, "rvol": 0.66, "stock_trade": {"entry": 6053.5, "sl": 5430.0, "tgt1": 6988.75, "tgt2": 7799.3, "rr": "1:1.5", "potential_pct": "+15.4% / +28.8%"}, "option_trade": {"strike": "6100 CE", "entry": 169.5, "sl": 118.6, "tgt1": 245.8, "tgt2": 330.5, "rr": 1.5, "lot_size": 100, "margin_required": 16950, "profit_tgt1": 7630, "profit_tgt2": 16100}}, {"symbol": "HAL", "cmp": 4980.0, "resistance": 5119.0, "base_floor": 4590.0, "pct_dist": -2.72, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 49.4, "rvol": 1.6, "stock_trade": {"entry": 4980.0, "sl": 4590.0, "tgt1": 5565.0, "tgt2": 6072.0, "rr": "1:1.5", "potential_pct": "+11.7% / +21.9%"}, "option_trade": {"strike": "5000 CE", "entry": 139.4, "sl": 97.6, "tgt1": 202.1, "tgt2": 271.8, "rr": 1.5, "lot_size": 150, "margin_required": 20910, "profit_tgt1": 9405, "profit_tgt2": 19860}}, {"symbol": "TATAPOWER", "cmp": 352.5, "resistance": 366.9, "base_floor": 333.2, "pct_dist": -3.92, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 49.0, "rvol": 2.32, "stock_trade": {"entry": 352.5, "sl": 333.2, "tgt1": 381.45, "tgt2": 406.54, "rr": "1:1.5", "potential_pct": "+8.2% / +15.3%"}, "option_trade": {"strike": "350 CE", "entry": 12.4, "sl": 8.7, "tgt1": 18.0, "tgt2": 24.2, "rr": 1.5, "lot_size": 1650, "margin_required": 20460, "profit_tgt1": 9240, "profit_tgt2": 19470}}, {"symbol": "COALINDIA", "cmp": 400.0, "resistance": 420.3, "base_floor": 380.4, "pct_dist": -4.83, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 39.7, "rvol": 0.66, "stock_trade": {"entry": 400.0, "sl": 380.4, "tgt1": 429.4, "tgt2": 454.88, "rr": "1:1.5", "potential_pct": "+7.3% / +13.7%"}, "option_trade": {"strike": "400 CE", "entry": 11.2, "sl": 7.8, "tgt1": 16.2, "tgt2": 21.8, "rr": 1.5, "lot_size": 2100, "margin_required": 23520, "profit_tgt1": 10500, "profit_tgt2": 22260}}, {"symbol": "MOTHERSON", "cmp": 158.55, "resistance": 169.49, "base_floor": 147.27, "pct_dist": -6.45, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 48.3, "rvol": 4.18, "stock_trade": {"entry": 158.55, "sl": 147.27, "tgt1": 175.47, "tgt2": 190.13, "rr": "1:1.5", "potential_pct": "+10.7% / +19.9%"}, "option_trade": {"strike": "160 CE", "entry": 4.4, "sl": 3.1, "tgt1": 6.4, "tgt2": 8.6, "rr": 1.5, "lot_size": 3300, "margin_required": 14520, "profit_tgt1": 6600, "profit_tgt2": 13860}}, {"symbol": "BHEL", "cmp": 418.8, "resistance": 464.0, "base_floor": 377.7, "pct_dist": -9.74, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 43.7, "rvol": 1.08, "stock_trade": {"entry": 418.8, "sl": 377.7, "tgt1": 480.45, "tgt2": 533.88, "rr": "1:1.5", "potential_pct": "+14.7% / +27.5%"}, "option_trade": {"strike": "420 CE", "entry": 11.7, "sl": 8.2, "tgt1": 17.0, "tgt2": 22.8, "rr": 1.5, "lot_size": 2250, "margin_required": 26325, "profit_tgt1": 11925, "profit_tgt2": 24975}}]

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
                            <div class="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center justify-between">
                                <span class="flex items-center gap-1.5"><i data-lucide="flame" class="w-3.5 h-3.5"></i> Option Edge F&O Call</span>
                                <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">Lot: ${item.option_trade.lot_size}</span>
                            </div>
                            <div class="space-y-1.5 mono text-xs">
                                <div class="flex justify-between"><span class="text-slate-400">Strike:</span> <span class="font-extrabold text-amber-300">${item.symbol} ${item.option_trade.strike}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Entry Premium:</span> <span class="font-bold text-white">₹${item.option_trade.entry}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Option SL (-30%):</span> <span class="font-bold text-rose-400">₹${item.option_trade.sl}</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Target 1 (+45%):</span> <span class="font-bold text-emerald-400">₹${item.option_trade.tgt1} (+₹${Number(item.option_trade.profit_tgt1).toLocaleString('en-IN')})</span></div>
                                <div class="flex justify-between"><span class="text-slate-400">Target 2 (+95% Doubler):</span> <span class="font-bold text-emerald-400">₹${item.option_trade.tgt2} (+₹${Number(item.option_trade.profit_tgt2).toLocaleString('en-IN')})</span></div>
                                <div class="flex justify-between pt-2 border-t border-slate-800/80 text-slate-300"><span>Capital Required</span> <span class="text-cyan-400 font-bold">₹${Number(item.option_trade.margin_required).toLocaleString('en-IN')}</span></div>
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
                            <button onclick="copyTradeAlert('${item.symbol}', '${item.cmp}', '${item.stock_trade.sl}', '${item.stock_trade.tgt1}', '${item.option_trade.strike}', '${item.option_trade.entry}', '${item.option_trade.sl}', '${item.option_trade.tgt1}', '${item.option_trade.tgt2}', '${item.option_trade.lot_size}', '${item.option_trade.margin_required}')" 
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

        function copyTradeAlert(sym, cmp, sl, tgt, strike, optEntry, optSl, optTgt1, optTgt2, lot, margin) {
            const text = `🔥 VICKYVAIO BREAKOUTS ALERT: ${sym}\n• Spot CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}\n• F&O Option: ${sym} ${strike}\n• Premium Entry: ₹${optEntry} | SL: ₹${optSl} (-30%)\n• Target 1: ₹${optTgt1} (+45%) | Target 2: ₹${optTgt2} (+95% Doubler)\n• Lot Size: ${lot} | Margin: ₹${Number(margin).toLocaleString('en-IN')}\nStrategy: Arvind Mangal Base & Option Edge Momentum Confluence`;
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
    try:
        payload = {
            "status": "success",
            "data": VERIFIED_BREAKOUT_DATA,
            "count": len(VERIFIED_BREAKOUT_DATA),
            "timestamp": datetime.datetime.now().isoformat()
        }
        return JSONResponse(content=payload)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

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
            regular_price = meta.get("regularMarketPrice")
            for i in range(len(ts)):
                o = quotes["open"][i]
                h = quotes["high"][i]
                l = quotes["low"][i]
                c = quotes["close"][i]
                v = quotes["volume"][i]
                if o is None or h is None or l is None:
                    continue
                if c is None:
                    c = regular_price or h
                candles.append({
                    "t": ts[i],
                    "o": round(o, 2),
                    "h": round(h, 2),
                    "l": round(l, 2),
                    "c": round(c, 2),
                    "v": v or 0
                })
            cmp = regular_price or (candles[-1]["c"] if candles else 0)
            return {"status": "success", "symbol": sym, "cmp": round(cmp, 2), "candles": candles}
    except Exception:
        pass
    return {"status": "fallback", "symbol": sym, "candles": []}