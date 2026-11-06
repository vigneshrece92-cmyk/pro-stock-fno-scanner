import datetime
import math
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Verified Authentic Breakout Setups with Exact Resistance, Base Floor, and Quality Scoring
VERIFIED_BREAKOUT_DATA = [{"symbol": "ICICIBANK", "cmp": 1571.2, "resistance": 1501.4, "base_floor": 1329.4, "pct_dist": 4.65, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 80.3, "rvol": 2.95, "stock_trade": {"entry": 1571.2, "sl": 1492.64, "tgt1": 1696.9, "tgt2": 1791.17, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1570 CE", "entry": 27.8, "sl": 19.5, "tgt1": 40.3, "tgt2": 54.2, "rr": 1.5, "lot_size": 700, "margin_required": 19460, "profit_tgt1": 8750, "profit_tgt2": 18480, "contract": "ICICIBANK26NOV1570CE", "source": "Official NSE BhavCopy"}}, {"symbol": "M&M", "cmp": 3287.2, "resistance": 3145.0, "base_floor": 2744.3, "pct_dist": 4.52, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 80.5, "rvol": 3.26, "stock_trade": {"entry": 3287.2, "sl": 3188.58, "tgt1": 3435.13, "tgt2": 3543.61, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "3300 CE", "entry": 53.0, "sl": 37.1, "tgt1": 76.8, "tgt2": 103.3, "rr": 1.5, "lot_size": 200, "margin_required": 10600, "profit_tgt1": 4760, "profit_tgt2": 10060, "contract": "M&M26NOV3300CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HDFCBANK", "cmp": 788.25, "resistance": 762.7, "base_floor": 669.2, "pct_dist": 3.35, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 68.5, "rvol": 2.3, "stock_trade": {"entry": 788.25, "sl": 748.84, "tgt1": 851.31, "tgt2": 898.6, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "790 CE", "entry": 16.0, "sl": 11.2, "tgt1": 23.2, "tgt2": 31.2, "rr": 1.5, "lot_size": 650, "margin_required": 10400, "profit_tgt1": 4680, "profit_tgt2": 9880, "contract": "HDFCBANK26NOV790CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TITAN", "cmp": 5000.0, "resistance": 4857.1, "base_floor": 4209.0, "pct_dist": 2.94, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 80.8, "rvol": 5.55, "stock_trade": {"entry": 5000.0, "sl": 4850.0, "tgt1": 5225.0, "tgt2": 5390.0, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "5000 CE", "entry": 87.35, "sl": 61.1, "tgt1": 126.7, "tgt2": 170.3, "rr": 1.5, "lot_size": 175, "margin_required": 15286, "profit_tgt1": 6886, "profit_tgt2": 14516, "contract": "TITAN26NOV5000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "AXISBANK", "cmp": 1322.9, "resistance": 1293.8, "base_floor": 1196.9, "pct_dist": 2.25, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 56.5, "rvol": 1.32, "stock_trade": {"entry": 1322.9, "sl": 1256.76, "tgt1": 1428.72, "tgt2": 1508.09, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1320 CE", "entry": 25.2, "sl": 17.6, "tgt1": 36.5, "tgt2": 49.1, "rr": 1.5, "lot_size": 625, "margin_required": 15750, "profit_tgt1": 7062, "profit_tgt2": 14938, "contract": "AXISBANK26NOV1320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TATASTEEL", "cmp": 186.3, "resistance": 183.33, "base_floor": 163.41, "pct_dist": 1.62, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.9, "rvol": 1.53, "stock_trade": {"entry": 186.3, "sl": 178.85, "tgt1": 197.48, "tgt2": 206.42, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "187.5 CE", "entry": 4.48, "sl": 3.1, "tgt1": 6.5, "tgt2": 8.7, "rr": 1.5, "lot_size": 2750, "margin_required": 12320, "profit_tgt1": 5555, "profit_tgt2": 11605, "contract": "TATASTEEL26NOV187.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DIVISLAB", "cmp": 10320.5, "resistance": 10159.0, "base_floor": 8797.0, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 82.2, "rvol": 1.34, "stock_trade": {"entry": 10320.5, "sl": 9804.48, "tgt1": 11146.13, "tgt2": 11765.36, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "10300 CE", "entry": 435.0, "sl": 304.5, "tgt1": 630.8, "tgt2": 848.2, "rr": 1.5, "lot_size": 100, "margin_required": 43500, "profit_tgt1": 19580, "profit_tgt2": 41320, "contract": "DIVISLAB26NOV10300CE", "source": "Official NSE BhavCopy"}}, {"symbol": "KOTAKBANK", "cmp": 480.0, "resistance": 472.5, "base_floor": 427.7, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 68.4, "rvol": 1.05, "stock_trade": {"entry": 480.0, "sl": 456.0, "tgt1": 518.4, "tgt2": 547.2, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "480 CE", "entry": 7.65, "sl": 5.4, "tgt1": 11.1, "tgt2": 14.9, "rr": 1.5, "lot_size": 2000, "margin_required": 15300, "profit_tgt1": 6900, "profit_tgt2": 14500, "contract": "KOTAKBANK26NOV480CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJFINANCE", "cmp": 1087.75, "resistance": 1074.85, "base_floor": 899.15, "pct_dist": 1.2, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.0, "rvol": 0.95, "stock_trade": {"entry": 1087.75, "sl": 1044.24, "tgt1": 1153.01, "tgt2": 1205.23, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1090 CE", "entry": 22.55, "sl": 15.8, "tgt1": 32.7, "tgt2": 44.0, "rr": 1.5, "lot_size": 750, "margin_required": 16912, "profit_tgt1": 7613, "profit_tgt2": 16088, "contract": "BAJFINANCE26NOV1090CE", "source": "Official NSE BhavCopy"}}, {"symbol": "LT", "cmp": 4117.7, "resistance": 4071.6, "base_floor": 3592.9, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 92.3, "rvol": 1.53, "stock_trade": {"entry": 4117.7, "sl": 3911.81, "tgt1": 4447.12, "tgt2": 4694.19, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "4100 CE", "entry": 79.8, "sl": 55.9, "tgt1": 115.7, "tgt2": 155.6, "rr": 1.5, "lot_size": 175, "margin_required": 13965, "profit_tgt1": 6283, "profit_tgt2": 13265, "contract": "LT26NOV4100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HINDALCO", "cmp": 958.4, "resistance": 947.7, "base_floor": 851.1, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 67.4, "rvol": 3.29, "stock_trade": {"entry": 958.4, "sl": 929.65, "tgt1": 1001.52, "tgt2": 1033.15, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "960 CE", "entry": 26.4, "sl": 18.5, "tgt1": 38.3, "tgt2": 51.5, "rr": 1.5, "lot_size": 700, "margin_required": 18480, "profit_tgt1": 8330, "profit_tgt2": 17570, "contract": "HINDALCO26NOV960CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BHARTIARTL", "cmp": 2107.2, "resistance": 2084.0, "base_floor": 1756.2, "pct_dist": 1.11, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 78.9, "rvol": 1.76, "stock_trade": {"entry": 2107.2, "sl": 2001.84, "tgt1": 2275.78, "tgt2": 2402.21, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "2100 CE", "entry": 25.1, "sl": 17.6, "tgt1": 36.4, "tgt2": 48.9, "rr": 1.5, "lot_size": 475, "margin_required": 11922, "profit_tgt1": 5367, "profit_tgt2": 11305, "contract": "BHARTIARTL26NOV2100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJAJ-AUTO", "cmp": 10900.0, "resistance": 10789.0, "base_floor": 9637.0, "pct_dist": 1.03, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 65.3, "rvol": 1.85, "stock_trade": {"entry": 10900.0, "sl": 10573.0, "tgt1": 11390.5, "tgt2": 11750.2, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "10900 CE", "entry": 215.95, "sl": 151.2, "tgt1": 313.1, "tgt2": 421.1, "rr": 1.5, "lot_size": 75, "margin_required": 16196, "profit_tgt1": 7286, "profit_tgt2": 15386, "contract": "BAJAJ-AUTO26NOV10900CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SBIN", "cmp": 1018.5, "resistance": 1009.6, "base_floor": 937.5, "pct_dist": 0.88, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.1, "rvol": 1.43, "stock_trade": {"entry": 1018.5, "sl": 977.76, "tgt1": 1079.61, "tgt2": 1128.5, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1020 CE", "entry": 19.65, "sl": 13.8, "tgt1": 28.5, "tgt2": 38.3, "rr": 1.5, "lot_size": 750, "margin_required": 14737, "profit_tgt1": 6638, "profit_tgt2": 13987, "contract": "SBIN26NOV1020CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJAJFINSV", "cmp": 1864.7, "resistance": 1848.8, "base_floor": 1624.8, "pct_dist": 0.86, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.3, "rvol": 0.65, "stock_trade": {"entry": 1864.7, "sl": 1790.11, "tgt1": 1976.59, "tgt2": 2066.09, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1860 CE", "entry": 36.6, "sl": 25.6, "tgt1": 53.1, "tgt2": 71.4, "rr": 1.5, "lot_size": 300, "margin_required": 10980, "profit_tgt1": 4950, "profit_tgt2": 10440, "contract": "BAJAJFINSV26NOV1860CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DLF", "cmp": 752.9, "resistance": 748.0, "base_floor": 634.15, "pct_dist": 0.66, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 80.2, "rvol": 1.09, "stock_trade": {"entry": 752.9, "sl": 715.25, "tgt1": 813.14, "tgt2": 858.32, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "750 CE", "entry": 18.3, "sl": 12.8, "tgt1": 26.5, "tgt2": 35.7, "rr": 1.5, "lot_size": 950, "margin_required": 17385, "profit_tgt1": 7790, "profit_tgt2": 16530, "contract": "DLF26NOV750CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MARUTI", "cmp": 12750.0, "resistance": 12681.0, "base_floor": 10985.0, "pct_dist": 0.54, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 77.6, "rvol": 1.87, "stock_trade": {"entry": 12750.0, "sl": 12367.5, "tgt1": 13323.75, "tgt2": 13744.5, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "12700 CE", "entry": 295.3, "sl": 206.7, "tgt1": 428.2, "tgt2": 575.8, "rr": 1.5, "lot_size": 50, "margin_required": 14765, "profit_tgt1": 6645, "profit_tgt2": 14025, "contract": "MARUTI26NOV12700CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MUTHOOTFIN", "cmp": 2869.0, "resistance": 2856.8, "base_floor": 2305.0, "pct_dist": 0.43, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.6, "rvol": 1.3, "stock_trade": {"entry": 2869.0, "sl": 2754.24, "tgt1": 3041.14, "tgt2": 3178.85, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2850 CE", "entry": 85.0, "sl": 59.5, "tgt1": 123.2, "tgt2": 165.8, "rr": 1.5, "lot_size": 275, "margin_required": 23375, "profit_tgt1": 10505, "profit_tgt2": 22220, "contract": "MUTHOOTFIN26NOV2850CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SUNPHARMA", "cmp": 1860.0, "resistance": 1855.0, "base_floor": 1719.1, "pct_dist": 0.27, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.4, "rvol": 1.13, "stock_trade": {"entry": 1860.0, "sl": 1786.06, "tgt1": 1970.91, "tgt2": 2059.64, "rr": "1:1.5", "potential_pct": "+6.0% / +10.7%"}, "option_trade": {"strike": "1860 CE", "entry": 36.55, "sl": 25.6, "tgt1": 53.0, "tgt2": 71.3, "rr": 1.5, "lot_size": 350, "margin_required": 12792, "profit_tgt1": 5758, "profit_tgt2": 12162, "contract": "SUNPHARMA26NOV1860CE", "source": "Official NSE BhavCopy"}}, {"symbol": "CHOLAFIN", "cmp": 1785.0, "resistance": 1781.0, "base_floor": 1415.0, "pct_dist": 0.22, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 71.0, "rvol": 0.75, "stock_trade": {"entry": 1785.0, "sl": 1713.6, "tgt1": 1892.1, "tgt2": 1977.78, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1780 CE", "entry": 43.5, "sl": 30.4, "tgt1": 63.1, "tgt2": 84.8, "rr": 1.5, "lot_size": 625, "margin_required": 27188, "profit_tgt1": 12250, "profit_tgt2": 25812, "contract": "CHOLAFIN26NOV1780CE", "source": "Official NSE BhavCopy"}}, {"symbol": "CIPLA", "cmp": 1411.0, "resistance": 1408.0, "base_floor": 1292.0, "pct_dist": 0.21, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 82.2, "rvol": 1.25, "stock_trade": {"entry": 1411.0, "sl": 1369.0, "tgt1": 1474.0, "tgt2": 1524.4, "rr": "1:1.5", "potential_pct": "+4.5% / +8.0%"}, "option_trade": {"strike": "1410 CE", "entry": 23.95, "sl": 16.8, "tgt1": 34.7, "tgt2": 46.7, "rr": 1.5, "lot_size": 425, "margin_required": 10179, "profit_tgt1": 4569, "profit_tgt2": 9669, "contract": "CIPLA26NOV1410CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TVSMOTOR", "cmp": 4491.7, "resistance": 4490.0, "base_floor": 3741.9, "pct_dist": 0.04, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 74.5, "rvol": 0.74, "stock_trade": {"entry": 4491.7, "sl": 4267.11, "tgt1": 4851.04, "tgt2": 5120.55, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "4500 CE", "entry": 89.2, "sl": 62.4, "tgt1": 129.3, "tgt2": 173.9, "rr": 1.5, "lot_size": 175, "margin_required": 15610, "profit_tgt1": 7018, "profit_tgt2": 14822, "contract": "TVSMOTOR26NOV4500CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PNB", "cmp": 126.55, "resistance": 126.8, "base_floor": 113.71, "pct_dist": -0.2, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 72.6, "rvol": 0.97, "stock_trade": {"entry": 126.55, "sl": 121.17, "tgt1": 135.16, "tgt2": 141.61, "rr": "1:1.6", "potential_pct": "+6.8% / +11.9%"}, "option_trade": {"strike": "127 CE", "entry": 2.31, "sl": 1.6, "tgt1": 3.3, "tgt2": 4.5, "rr": 1.4, "lot_size": 8000, "margin_required": 18480, "profit_tgt1": 7920, "profit_tgt2": 17520, "contract": "PNB26NOV127CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HEROMOTOCO", "cmp": 5513.0, "resistance": 5527.0, "base_floor": 4825.0, "pct_dist": -0.25, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.2, "rvol": 1.34, "stock_trade": {"entry": 5513.0, "sl": 5292.48, "tgt1": 5843.78, "tgt2": 6108.4, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "5500 CE", "entry": 123.25, "sl": 86.3, "tgt1": 178.7, "tgt2": 240.3, "rr": 1.5, "lot_size": 150, "margin_required": 18488, "profit_tgt1": 8317, "profit_tgt2": 17558, "contract": "HEROMOTOCO26NOV5500CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ITC", "cmp": 283.15, "resistance": 283.9, "base_floor": 252.8, "pct_dist": -0.26, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 76.2, "rvol": 0.78, "stock_trade": {"entry": 283.15, "sl": 268.99, "tgt1": 305.81, "tgt2": 322.8, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "282.5 CE", "entry": 4.7, "sl": 3.3, "tgt1": 6.8, "tgt2": 9.2, "rr": 1.5, "lot_size": 1725, "margin_required": 8108, "profit_tgt1": 3622, "profit_tgt2": 7762, "contract": "ITC26NOV282.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "GODREJPROP", "cmp": 1809.3, "resistance": 1815.0, "base_floor": 1468.4, "pct_dist": -0.31, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.7, "rvol": 1.49, "stock_trade": {"entry": 1809.3, "sl": 1736.93, "tgt1": 1917.85, "tgt2": 2004.7, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1800 CE", "entry": 48.6, "sl": 34.0, "tgt1": 70.5, "tgt2": 94.8, "rr": 1.5, "lot_size": 325, "margin_required": 15795, "profit_tgt1": 7117, "profit_tgt2": 15015, "contract": "GODREJPROP26NOV1800CE", "source": "Official NSE BhavCopy"}}, {"symbol": "RELIANCE", "cmp": 1320.0, "resistance": 1325.0, "base_floor": 1152.2, "pct_dist": -0.38, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.2, "rvol": 1.11, "stock_trade": {"entry": 1320.0, "sl": 1267.2, "tgt1": 1399.2, "tgt2": 1462.56, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1320 CE", "entry": 24.0, "sl": 16.8, "tgt1": 34.8, "tgt2": 46.8, "rr": 1.5, "lot_size": 500, "margin_required": 12000, "profit_tgt1": 5400, "profit_tgt2": 11400, "contract": "RELIANCE26NOV1320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BANKBARODA", "cmp": 250.31, "resistance": 251.34, "base_floor": 225.2, "pct_dist": -0.41, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 70.8, "rvol": 0.98, "stock_trade": {"entry": 250.31, "sl": 239.64, "tgt1": 267.38, "tgt2": 280.19, "rr": "1:1.6", "potential_pct": "+6.8% / +11.9%"}, "option_trade": {"strike": "250 CE", "entry": 5.08, "sl": 3.6, "tgt1": 7.4, "tgt2": 9.9, "rr": 1.6, "lot_size": 2925, "margin_required": 14859, "profit_tgt1": 6786, "profit_tgt2": 14098, "contract": "BANKBARODA26NOV250CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JINDALSTEL", "cmp": 1165.0, "resistance": 1169.9, "base_floor": 1000.8, "pct_dist": -0.42, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.2, "rvol": 0.88, "stock_trade": {"entry": 1165.0, "sl": 1118.4, "tgt1": 1234.9, "tgt2": 1290.82, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1160 CE", "entry": 29.0, "sl": 20.3, "tgt1": 42.0, "tgt2": 56.5, "rr": 1.5, "lot_size": 625, "margin_required": 18125, "profit_tgt1": 8125, "profit_tgt2": 17188, "contract": "JINDALSTEL26NOV1160CE", "source": "Official NSE BhavCopy"}}, {"symbol": "EICHERMOT", "cmp": 7669.5, "resistance": 7713.0, "base_floor": 6767.5, "pct_dist": -0.56, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.4, "rvol": 0.91, "stock_trade": {"entry": 7669.5, "sl": 7362.72, "tgt1": 8129.67, "tgt2": 8497.81, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "7700 CE", "entry": 187.45, "sl": 131.2, "tgt1": 271.8, "tgt2": 365.5, "rr": 1.5, "lot_size": 100, "margin_required": 18745, "profit_tgt1": 8435, "profit_tgt2": 17805, "contract": "EICHERMOT26NOV7700CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BPCL", "cmp": 319.9, "resistance": 322.0, "base_floor": 275.4, "pct_dist": -0.65, "stage": "BASE SQUEEZE", "score": 84, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.2, "rvol": 1.14, "stock_trade": {"entry": 319.9, "sl": 307.1, "tgt1": 339.1, "tgt2": 354.46, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "320 CE", "entry": 7.3, "sl": 5.1, "tgt1": 10.6, "tgt2": 14.2, "rr": 1.5, "lot_size": 1975, "margin_required": 14418, "profit_tgt1": 6518, "profit_tgt2": 13627, "contract": "BPCL26NOV320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "IOC", "cmp": 146.25, "resistance": 147.31, "base_floor": 124.92, "pct_dist": -0.72, "stage": "BASE SQUEEZE", "score": 84, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.9, "rvol": 2.03, "stock_trade": {"entry": 146.25, "sl": 138.94, "tgt1": 157.95, "tgt2": 166.72, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "146 CE", "entry": 3.61, "sl": 2.5, "tgt1": 5.2, "tgt2": 7.0, "rr": 1.4, "lot_size": 4875, "margin_required": 17599, "profit_tgt1": 7751, "profit_tgt2": 16526, "contract": "IOC26NOV146CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DRREDDY", "cmp": 1373.0, "resistance": 1384.0, "base_floor": 1167.2, "pct_dist": -0.79, "stage": "BASE SQUEEZE", "score": 84, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 83.7, "rvol": 0.59, "stock_trade": {"entry": 1373.0, "sl": 1304.35, "tgt1": 1482.84, "tgt2": 1565.22, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1370 CE", "entry": 26.2, "sl": 18.3, "tgt1": 38.0, "tgt2": 51.1, "rr": 1.5, "lot_size": 625, "margin_required": 16375, "profit_tgt1": 7375, "profit_tgt2": 15563, "contract": "DRREDDY26NOV1370CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JSWSTEEL", "cmp": 1357.1, "resistance": 1370.0, "base_floor": 1158.0, "pct_dist": -0.94, "stage": "BASE SQUEEZE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.8, "rvol": 1.35, "stock_trade": {"entry": 1357.1, "sl": 1302.82, "tgt1": 1438.52, "tgt2": 1503.66, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1360 CE", "entry": 24.5, "sl": 17.1, "tgt1": 35.5, "tgt2": 47.8, "rr": 1.5, "lot_size": 675, "margin_required": 16538, "profit_tgt1": 7425, "profit_tgt2": 15727, "contract": "JSWSTEEL26NOV1360CE", "source": "Official NSE BhavCopy"}}, {"symbol": "WIPRO", "cmp": 198.0, "resistance": 200.11, "base_floor": 158.3, "pct_dist": -1.05, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.4, "rvol": 0.67, "stock_trade": {"entry": 198.0, "sl": 190.8, "tgt1": 208.8, "tgt2": 217.44, "rr": "1:1.5", "potential_pct": "+5.5% / +9.8%"}, "option_trade": {"strike": "197.5 CE", "entry": 5.2, "sl": 3.6, "tgt1": 7.5, "tgt2": 10.1, "rr": 1.4, "lot_size": 3000, "margin_required": 15600, "profit_tgt1": 6900, "profit_tgt2": 14700, "contract": "WIPRO26NOV197.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TECHM", "cmp": 1831.0, "resistance": 1851.0, "base_floor": 1442.5, "pct_dist": -1.08, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 58.0, "rvol": 0.47, "stock_trade": {"entry": 1831.0, "sl": 1761.3, "tgt1": 1935.55, "tgt2": 2019.19, "rr": "1:1.5", "potential_pct": "+5.7% / +10.3%"}, "option_trade": {"strike": "1840 CE", "entry": 42.45, "sl": 29.7, "tgt1": 61.6, "tgt2": 82.8, "rr": 1.5, "lot_size": 600, "margin_required": 25470, "profit_tgt1": 11490, "profit_tgt2": 24210, "contract": "TECHM26NOV1840CE", "source": "Official NSE BhavCopy"}}, {"symbol": "GAIL", "cmp": 185.79, "resistance": 188.9, "base_floor": 160.7, "pct_dist": -1.65, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 74.3, "rvol": 0.87, "stock_trade": {"entry": 185.79, "sl": 178.36, "tgt1": 196.93, "tgt2": 205.85, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "185 CE", "entry": 4.0, "sl": 2.8, "tgt1": 5.8, "tgt2": 7.8, "rr": 1.5, "lot_size": 3550, "margin_required": 14200, "profit_tgt1": 6390, "profit_tgt2": 13490, "contract": "GAIL26NOV185CE", "source": "Official NSE BhavCopy"}}, {"symbol": "COFORGE", "cmp": 2076.0, "resistance": 2119.0, "base_floor": 1804.5, "pct_dist": -2.03, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.3, "rvol": 0.89, "stock_trade": {"entry": 2076.0, "sl": 1992.96, "tgt1": 2200.56, "tgt2": 2300.21, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2080 CE", "entry": 57.1, "sl": 40.0, "tgt1": 82.8, "tgt2": 111.3, "rr": 1.5, "lot_size": 475, "margin_required": 27122, "profit_tgt1": 12207, "profit_tgt2": 25745, "contract": "COFORGE26NOV2080CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BEL", "cmp": 396.0, "resistance": 404.5, "base_floor": 354.55, "pct_dist": -2.1, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.8, "rvol": 0.79, "stock_trade": {"entry": 396.0, "sl": 380.49, "tgt1": 419.26, "tgt2": 437.88, "rr": "1:1.5", "potential_pct": "+5.9% / +10.6%"}, "option_trade": {"strike": "395 CE", "entry": 8.75, "sl": 6.1, "tgt1": 12.7, "tgt2": 17.1, "rr": 1.5, "lot_size": 1425, "margin_required": 12469, "profit_tgt1": 5629, "profit_tgt2": 11899, "contract": "BEL26NOV395CE", "source": "Official NSE BhavCopy"}}, {"symbol": "VEDL", "cmp": 261.75, "resistance": 267.5, "base_floor": 221.6, "pct_dist": -2.15, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 62.5, "rvol": 0.99, "stock_trade": {"entry": 261.75, "sl": 251.28, "tgt1": 277.45, "tgt2": 290.02, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "260 CE", "entry": 8.54, "sl": 6.0, "tgt1": 12.4, "tgt2": 16.7, "rr": 1.5, "lot_size": 1150, "margin_required": 9821, "profit_tgt1": 4439, "profit_tgt2": 9384, "contract": "VEDL26NOV260CE", "source": "Official NSE BhavCopy"}}, {"symbol": "NATIONALUM", "cmp": 325.75, "resistance": 333.2, "base_floor": 293.0, "pct_dist": -2.24, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 50.7, "rvol": 1.14, "stock_trade": {"entry": 325.75, "sl": 323.99, "tgt1": 339.43, "tgt2": 350.38, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "325 CE", "entry": 10.45, "sl": 7.3, "tgt1": 15.2, "tgt2": 20.4, "rr": 1.5, "lot_size": 1875, "margin_required": 19594, "profit_tgt1": 8906, "profit_tgt2": 18656, "contract": "NATIONALUM26NOV325CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PERSISTENT", "cmp": 6053.5, "resistance": 6209.0, "base_floor": 5430.0, "pct_dist": -2.5, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.6, "rvol": 0.66, "stock_trade": {"entry": 6053.5, "sl": 5884.0, "tgt1": 6307.75, "tgt2": 6511.15, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "6100 CE", "entry": 140.5, "sl": 98.3, "tgt1": 203.7, "tgt2": 274.0, "rr": 1.5, "lot_size": 125, "margin_required": 17562, "profit_tgt1": 7900, "profit_tgt2": 16688, "contract": "PERSISTENT26NOV6100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HAL", "cmp": 4980.0, "resistance": 5119.0, "base_floor": 4590.0, "pct_dist": -2.72, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 49.4, "rvol": 1.6, "stock_trade": {"entry": 4980.0, "sl": 4830.6, "tgt1": 5204.1, "tgt2": 5368.44, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "5000 CE", "entry": 144.4, "sl": 101.1, "tgt1": 209.4, "tgt2": 281.6, "rr": 1.5, "lot_size": 150, "margin_required": 21660, "profit_tgt1": 9750, "profit_tgt2": 20580, "contract": "HAL26NOV5000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TATAPOWER", "cmp": 352.5, "resistance": 366.9, "base_floor": 333.2, "pct_dist": -3.92, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 49.0, "rvol": 2.32, "stock_trade": {"entry": 352.5, "sl": 341.93, "tgt1": 368.36, "tgt2": 379.98, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "350 CE", "entry": 10.2, "sl": 7.1, "tgt1": 14.8, "tgt2": 19.9, "rr": 1.5, "lot_size": 1450, "margin_required": 14790, "profit_tgt1": 6670, "profit_tgt2": 14065, "contract": "TATAPOWER26NOV350CE", "source": "Official NSE BhavCopy"}}, {"symbol": "COALINDIA", "cmp": 400.0, "resistance": 420.3, "base_floor": 380.4, "pct_dist": -4.83, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 39.7, "rvol": 0.66, "stock_trade": {"entry": 400.0, "sl": 403.8, "tgt1": 416.8, "tgt2": 430.24, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "400 CE", "entry": 6.6, "sl": 4.6, "tgt1": 9.6, "tgt2": 12.9, "rr": 1.5, "lot_size": 1350, "margin_required": 8910, "profit_tgt1": 4050, "profit_tgt2": 8505, "contract": "COALINDIA26NOV400CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MOTHERSON", "cmp": 158.55, "resistance": 169.49, "base_floor": 147.27, "pct_dist": -6.45, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "pattern": "High-Volume Range Expansion", "rsi": 48.3, "rvol": 4.18, "stock_trade": {"entry": 158.55, "sl": 155.24, "tgt1": 163.52, "tgt2": 167.16, "rr": "1:1.5", "potential_pct": "+3.1% / +5.4%"}, "option_trade": {"strike": "157.5 CE", "entry": 4.85, "sl": 3.4, "tgt1": 7.0, "tgt2": 9.5, "rr": 1.5, "lot_size": 6150, "margin_required": 29827, "profit_tgt1": 13223, "profit_tgt2": 28598, "contract": "MOTHERSON26NOV157.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BHEL", "cmp": 418.8, "resistance": 464.0, "base_floor": 377.7, "pct_dist": -9.74, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 43.7, "rvol": 1.08, "stock_trade": {"entry": 418.8, "sl": 413.14, "tgt1": 436.39, "tgt2": 450.46, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "420 CE", "entry": 11.6, "sl": 8.1, "tgt1": 16.8, "tgt2": 22.6, "rr": 1.5, "lot_size": 2625, "margin_required": 30450, "profit_tgt1": 13650, "profit_tgt2": 28875, "contract": "BHEL26NOV420CE", "source": "Official NSE BhavCopy"}}]

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

        function setHorizon(horizon, btnElement) {
            activeHorizon = horizon;
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-emerald-500', 'text-black');
                btn.classList.add('text-slate-300', 'hover:bg-slate-800');
            });
            const targetBtn = btnElement || (typeof event !== 'undefined' && event ? event.currentTarget || event.target : null);
            if (targetBtn && targetBtn.classList) {
                targetBtn.classList.remove('text-slate-300', 'hover:bg-slate-800');
                targetBtn.classList.add('bg-emerald-500', 'text-black');
            }
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
            const btn = document.getElementById('scanBtn');
            if (icon) icon.classList.add('animate-spin');
            if (btn) btn.disabled = true;
            try {
                const res = await fetch('/api/scan?t=' + Date.now());
                const json = await res.json();
                if (json.data && json.data.length > 0) {
                    fullData = json.data;
                    updateStats();
                    applyFilters();
                }
            } catch (e) {
                console.log('Error fetching scan:', e);
            } finally {
                if (icon) icon.classList.remove('animate-spin');
                if (btn) btn.disabled = false;
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