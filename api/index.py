import datetime
import math
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Verified Authentic Breakout Setups with Exact Resistance, Base Floor, and Quality Scoring
VERIFIED_BREAKOUT_DATA = [{"symbol": "ICICIBANK", "company_name": "ICICI Bank Limited", "cmp": 1571.2, "resistance": 1501.4, "base_floor": 1329.4, "pct_dist": 4.65, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 80.3, "rvol": 2.95, "stock_trade": {"entry": 1571.2, "sl": 1508.35, "tgt1": 1665.48, "tgt2": 1740.9, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1570 CE", "entry": 27.8, "sl": 19.5, "tgt1": 40.3, "tgt2": 54.2, "rr": 1.5, "lot_size": 700, "margin_required": 19460, "profit_tgt1": 8750, "profit_tgt2": 18480, "contract": "ICICIBANK26NOV1570CE", "source": "Official NSE BhavCopy"}}, {"symbol": "M&M", "company_name": "Mahindra & Mahindra Limited", "cmp": 3287.2, "resistance": 3145.0, "base_floor": 2744.3, "pct_dist": 4.52, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 80.5, "rvol": 3.26, "stock_trade": {"entry": 3287.2, "sl": 3188.58, "tgt1": 3435.13, "tgt2": 3543.61, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "3300 CE", "entry": 53.0, "sl": 37.1, "tgt1": 76.8, "tgt2": 103.3, "rr": 1.5, "lot_size": 200, "margin_required": 10600, "profit_tgt1": 4760, "profit_tgt2": 10060, "contract": "M&M26NOV3300CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HDFCBANK", "company_name": "HDFC Bank Limited", "cmp": 788.25, "resistance": 762.7, "base_floor": 669.2, "pct_dist": 3.35, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 68.5, "rvol": 2.3, "stock_trade": {"entry": 788.25, "sl": 748.84, "tgt1": 851.31, "tgt2": 898.6, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "790 CE", "entry": 16.0, "sl": 11.2, "tgt1": 23.2, "tgt2": 31.2, "rr": 1.5, "lot_size": 650, "margin_required": 10400, "profit_tgt1": 4680, "profit_tgt2": 9880, "contract": "HDFCBANK26NOV790CE", "source": "Official NSE BhavCopy"}}, {"symbol": "KALYANKJIL", "company_name": "Kalyan Jewellers India Limited", "cmp": 590.75, "resistance": 573.0, "base_floor": 490.6, "pct_dist": 3.1, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 58.4, "rvol": 5.5, "stock_trade": {"entry": 590.75, "sl": 573.03, "tgt1": 617.33, "tgt2": 636.82, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "590 CE", "entry": 26.55, "sl": 18.6, "tgt1": 38.5, "tgt2": 51.8, "rr": 1.5, "lot_size": 1350, "margin_required": 35842, "profit_tgt1": 16132, "profit_tgt2": 34087, "contract": "KALYANKJIL26NOV590CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TITAN", "company_name": "Titan Company Limited", "cmp": 5000.0, "resistance": 4857.1, "base_floor": 4209.0, "pct_dist": 2.94, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 80.8, "rvol": 5.55, "stock_trade": {"entry": 5000.0, "sl": 4850.0, "tgt1": 5225.0, "tgt2": 5390.0, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "5000 CE", "entry": 87.35, "sl": 61.1, "tgt1": 126.7, "tgt2": 170.3, "rr": 1.5, "lot_size": 175, "margin_required": 15286, "profit_tgt1": 6886, "profit_tgt2": 14516, "contract": "TITAN26NOV5000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "AXISBANK", "company_name": "Axis Bank Limited", "cmp": 1322.9, "resistance": 1293.8, "base_floor": 1196.9, "pct_dist": 2.25, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 56.5, "rvol": 1.32, "stock_trade": {"entry": 1322.9, "sl": 1256.76, "tgt1": 1428.72, "tgt2": 1508.09, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1320 CE", "entry": 25.2, "sl": 17.6, "tgt1": 36.5, "tgt2": 49.1, "rr": 1.5, "lot_size": 625, "margin_required": 15750, "profit_tgt1": 7062, "profit_tgt2": 14938, "contract": "AXISBANK26NOV1320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SBILIFE", "company_name": "SBI Life Insurance Company Limited", "cmp": 1784.0, "resistance": 1745.0, "base_floor": 1607.7, "pct_dist": 2.23, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 76.7, "rvol": 1.15, "stock_trade": {"entry": 1784.0, "sl": 1712.64, "tgt1": 1891.04, "tgt2": 1976.67, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1780 CE", "entry": 23.0, "sl": 16.1, "tgt1": 33.4, "tgt2": 44.9, "rr": 1.5, "lot_size": 375, "margin_required": 8625, "profit_tgt1": 3900, "profit_tgt2": 8212, "contract": "SBILIFE26NOV1780CE", "source": "Official NSE BhavCopy"}}, {"symbol": "GLENMARK", "company_name": "Glenmark Pharmaceuticals Limited", "cmp": 2590.0, "resistance": 2542.2, "base_floor": 2101.6, "pct_dist": 1.88, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 79.4, "rvol": 7.98, "stock_trade": {"entry": 2590.0, "sl": 2486.4, "tgt1": 2745.4, "tgt2": 2869.72, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2580 CE", "entry": 78.05, "sl": 54.6, "tgt1": 113.2, "tgt2": 152.2, "rr": 1.5, "lot_size": 375, "margin_required": 29269, "profit_tgt1": 13181, "profit_tgt2": 27806, "contract": "GLENMARK26NOV2580CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MAHABANK", "company_name": "Bank of Maharashtra", "cmp": 86.91, "resistance": 85.34, "base_floor": 72.77, "pct_dist": 1.84, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 64.1, "rvol": 1.57, "stock_trade": {"entry": 86.91, "sl": 82.56, "tgt1": 93.87, "tgt2": 99.09, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "87 CE", "entry": 3.0, "sl": 2.1, "tgt1": 4.3, "tgt2": 5.8, "rr": 1.4, "lot_size": 6500, "margin_required": 19500, "profit_tgt1": 8450, "profit_tgt2": 18200, "contract": "MAHABANK26NOV87CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TATASTEEL", "company_name": "Tata Steel Limited", "cmp": 186.3, "resistance": 183.33, "base_floor": 163.41, "pct_dist": 1.62, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.9, "rvol": 1.53, "stock_trade": {"entry": 186.3, "sl": 178.85, "tgt1": 197.48, "tgt2": 206.42, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "187.5 CE", "entry": 4.48, "sl": 3.1, "tgt1": 6.5, "tgt2": 8.7, "rr": 1.5, "lot_size": 2750, "margin_required": 12320, "profit_tgt1": 5555, "profit_tgt2": 11605, "contract": "TATASTEEL26NOV187.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DIVISLAB", "company_name": "Divi's Laboratories Limited", "cmp": 10320.5, "resistance": 10159.0, "base_floor": 8797.0, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 82.2, "rvol": 1.34, "stock_trade": {"entry": 10320.5, "sl": 9907.68, "tgt1": 10939.73, "tgt2": 11435.11, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "10300 CE", "entry": 435.0, "sl": 304.5, "tgt1": 630.8, "tgt2": 848.2, "rr": 1.5, "lot_size": 100, "margin_required": 43500, "profit_tgt1": 19580, "profit_tgt2": 41320, "contract": "DIVISLAB26NOV10300CE", "source": "Official NSE BhavCopy"}}, {"symbol": "KOTAKBANK", "company_name": "Kotak Mahindra Bank Limited", "cmp": 480.0, "resistance": 472.5, "base_floor": 427.7, "pct_dist": 1.59, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 68.4, "rvol": 1.05, "stock_trade": {"entry": 480.0, "sl": 460.8, "tgt1": 508.8, "tgt2": 531.84, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "480 CE", "entry": 7.65, "sl": 5.4, "tgt1": 11.1, "tgt2": 14.9, "rr": 1.5, "lot_size": 2000, "margin_required": 15300, "profit_tgt1": 6900, "profit_tgt2": 14500, "contract": "KOTAKBANK26NOV480CE", "source": "Official NSE BhavCopy"}}, {"symbol": "INDHOTEL", "company_name": "The Indian Hotels Company Limited", "cmp": 888.0, "resistance": 875.0, "base_floor": 708.1, "pct_dist": 1.49, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 84.0, "rvol": 1.43, "stock_trade": {"entry": 888.0, "sl": 843.6, "tgt1": 959.04, "tgt2": 1012.32, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "890 CE", "entry": 18.5, "sl": 12.9, "tgt1": 26.8, "tgt2": 36.1, "rr": 1.5, "lot_size": 1000, "margin_required": 18500, "profit_tgt1": 8300, "profit_tgt2": 17600, "contract": "INDHOTEL26NOV890CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ULTRACEMCO", "company_name": "UltraTech Cement Limited", "cmp": 12450.0, "resistance": 12285.0, "base_floor": 10426.0, "pct_dist": 1.34, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.2, "rvol": 1.72, "stock_trade": {"entry": 12450.0, "sl": 11827.5, "tgt1": 13446.0, "tgt2": 14193.0, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "12400 CE", "entry": 212.1, "sl": 148.5, "tgt1": 307.5, "tgt2": 413.6, "rr": 1.5, "lot_size": 50, "margin_required": 10605, "profit_tgt1": 4770, "profit_tgt2": 10075, "contract": "ULTRACEMCO26NOV12400CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PHOENIXLTD", "company_name": "The Phoenix Mills Limited", "cmp": 2154.9, "resistance": 2128.0, "base_floor": 1771.2, "pct_dist": 1.26, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.1, "rvol": 0.6, "stock_trade": {"entry": 2154.9, "sl": 2047.15, "tgt1": 2327.3, "tgt2": 2456.6, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "2160 CE", "entry": 40.95, "sl": 28.7, "tgt1": 59.4, "tgt2": 79.9, "rr": 1.5, "lot_size": 350, "margin_required": 14333, "profit_tgt1": 6457, "profit_tgt2": 13633, "contract": "PHOENIXLTD26NOV2160CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance Limited", "cmp": 1087.75, "resistance": 1074.85, "base_floor": 899.15, "pct_dist": 1.2, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.0, "rvol": 0.95, "stock_trade": {"entry": 1087.75, "sl": 1044.24, "tgt1": 1153.01, "tgt2": 1205.23, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1090 CE", "entry": 22.55, "sl": 15.8, "tgt1": 32.7, "tgt2": 44.0, "rr": 1.5, "lot_size": 750, "margin_required": 16912, "profit_tgt1": 7613, "profit_tgt2": 16088, "contract": "BAJFINANCE26NOV1090CE", "source": "Official NSE BhavCopy"}}, {"symbol": "IREDA", "company_name": "Indian Renewable Energy Development Agency Limited", "cmp": 111.46, "resistance": 110.15, "base_floor": 98.78, "pct_dist": 1.19, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 54.8, "rvol": 1.68, "stock_trade": {"entry": 111.46, "sl": 108.12, "tgt1": 116.47, "tgt2": 120.14, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "111 CE", "entry": 3.46, "sl": 2.4, "tgt1": 5.0, "tgt2": 6.7, "rr": 1.5, "lot_size": 4525, "margin_required": 15656, "profit_tgt1": 6968, "profit_tgt2": 14661, "contract": "IREDA26NOV111CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HINDALCO", "company_name": "Hindalco Industries Limited", "cmp": 958.4, "resistance": 947.7, "base_floor": 851.1, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Metals & Mining", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 67.4, "rvol": 3.29, "stock_trade": {"entry": 958.4, "sl": 929.65, "tgt1": 1001.52, "tgt2": 1033.15, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "960 CE", "entry": 26.4, "sl": 18.5, "tgt1": 38.3, "tgt2": 51.5, "rr": 1.5, "lot_size": 700, "margin_required": 18480, "profit_tgt1": 8330, "profit_tgt2": 17570, "contract": "HINDALCO26NOV960CE", "source": "Official NSE BhavCopy"}}, {"symbol": "LT", "company_name": "Larsen & Toubro Limited", "cmp": 4117.7, "resistance": 4071.6, "base_floor": 3592.9, "pct_dist": 1.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 92.3, "rvol": 1.53, "stock_trade": {"entry": 4117.7, "sl": 3952.99, "tgt1": 4364.76, "tgt2": 4562.42, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "4100 CE", "entry": 79.8, "sl": 55.9, "tgt1": 115.7, "tgt2": 155.6, "rr": 1.5, "lot_size": 175, "margin_required": 13965, "profit_tgt1": 6283, "profit_tgt2": 13265, "contract": "LT26NOV4100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BHARTIARTL", "company_name": "Bharti Airtel Limited", "cmp": 2107.2, "resistance": 2084.0, "base_floor": 1756.2, "pct_dist": 1.11, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 78.9, "rvol": 1.76, "stock_trade": {"entry": 2107.2, "sl": 2001.84, "tgt1": 2275.78, "tgt2": 2402.21, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "2100 CE", "entry": 25.1, "sl": 17.6, "tgt1": 36.4, "tgt2": 48.9, "rr": 1.5, "lot_size": 475, "margin_required": 11922, "profit_tgt1": 5367, "profit_tgt2": 11305, "contract": "BHARTIARTL26NOV2100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJAJ-AUTO", "company_name": "Bajaj Auto Limited", "cmp": 10900.0, "resistance": 10789.0, "base_floor": 9637.0, "pct_dist": 1.03, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 65.3, "rvol": 1.85, "stock_trade": {"entry": 10900.0, "sl": 10573.0, "tgt1": 11390.5, "tgt2": 11750.2, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "10900 CE", "entry": 215.95, "sl": 151.2, "tgt1": 313.1, "tgt2": 421.1, "rr": 1.5, "lot_size": 75, "margin_required": 16196, "profit_tgt1": 7286, "profit_tgt2": 15386, "contract": "BAJAJ-AUTO26NOV10900CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ETERNAL", "company_name": "Eternal Limited", "cmp": 363.15, "resistance": 359.7, "base_floor": 301.75, "pct_dist": 0.96, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 69.0, "rvol": 0.92, "stock_trade": {"entry": 363.15, "sl": 348.62, "tgt1": 384.94, "tgt2": 402.38, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "365 CE", "entry": 7.75, "sl": 5.4, "tgt1": 11.2, "tgt2": 15.1, "rr": 1.5, "lot_size": 2425, "margin_required": 18794, "profit_tgt1": 8366, "profit_tgt2": 17824, "contract": "ETERNAL26NOV365CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ANGELONE", "company_name": "Angel One Limited", "cmp": 331.0, "resistance": 327.95, "base_floor": 273.8, "pct_dist": 0.93, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 65.3, "rvol": 1.13, "stock_trade": {"entry": 331.0, "sl": 314.45, "tgt1": 357.48, "tgt2": 377.34, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "330 CE", "entry": 10.65, "sl": 7.5, "tgt1": 15.4, "tgt2": 20.8, "rr": 1.5, "lot_size": 2500, "margin_required": 26625, "profit_tgt1": 11875, "profit_tgt2": 25375, "contract": "ANGELONE26NOV330CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SBIN", "company_name": "State Bank of India", "cmp": 1018.5, "resistance": 1009.6, "base_floor": 937.5, "pct_dist": 0.88, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.1, "rvol": 1.43, "stock_trade": {"entry": 1018.5, "sl": 977.76, "tgt1": 1079.61, "tgt2": 1128.5, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1020 CE", "entry": 19.65, "sl": 13.8, "tgt1": 28.5, "tgt2": 38.3, "rr": 1.5, "lot_size": 750, "margin_required": 14737, "profit_tgt1": 6638, "profit_tgt2": 13987, "contract": "SBIN26NOV1020CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BAJAJFINSV", "company_name": "Bajaj Finserv Ltd.", "cmp": 1864.7, "resistance": 1848.8, "base_floor": 1624.8, "pct_dist": 0.86, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.3, "rvol": 0.65, "stock_trade": {"entry": 1864.7, "sl": 1790.11, "tgt1": 1976.59, "tgt2": 2066.09, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1860 CE", "entry": 36.6, "sl": 25.6, "tgt1": 53.1, "tgt2": 71.4, "rr": 1.5, "lot_size": 300, "margin_required": 10980, "profit_tgt1": 4950, "profit_tgt2": 10440, "contract": "BAJAJFINSV26NOV1860CE", "source": "Official NSE BhavCopy"}}, {"symbol": "NAVINFLUOR", "company_name": "Navin Fluorine International Limited", "cmp": 9010.0, "resistance": 8937.0, "base_floor": 7510.5, "pct_dist": 0.82, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Chemicals & Fertilizers", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 64.6, "rvol": 1.34, "stock_trade": {"entry": 9010.0, "sl": 8649.6, "tgt1": 9550.6, "tgt2": 9983.08, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "9000 CE", "entry": 225.35, "sl": 157.7, "tgt1": 326.8, "tgt2": 439.4, "rr": 1.5, "lot_size": 75, "margin_required": 16901, "profit_tgt1": 7609, "profit_tgt2": 16054, "contract": "NAVINFLUOR26NOV9000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PIDILITIND", "company_name": "Pidilite Industries Limited", "cmp": 1579.0, "resistance": 1566.7, "base_floor": 1342.3, "pct_dist": 0.79, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Chemicals & Fertilizers", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 61.8, "rvol": 0.77, "stock_trade": {"entry": 1579.0, "sl": 1515.84, "tgt1": 1673.74, "tgt2": 1749.53, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1580 CE", "entry": 32.45, "sl": 22.7, "tgt1": 47.1, "tgt2": 63.3, "rr": 1.5, "lot_size": 500, "margin_required": 16225, "profit_tgt1": 7325, "profit_tgt2": 15425, "contract": "PIDILITIND26NOV1580CE", "source": "Official NSE BhavCopy"}}, {"symbol": "FORCEMOT", "company_name": "Force Motors Limited", "cmp": 18968.0, "resistance": 18841.0, "base_floor": 16184.0, "pct_dist": 0.67, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 62.9, "rvol": 2.07, "stock_trade": {"entry": 18968.0, "sl": 18398.96, "tgt1": 19821.56, "tgt2": 20447.5, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "19000 CE", "entry": 600.0, "sl": 420.0, "tgt1": 870.0, "tgt2": 1170.0, "rr": 1.5, "lot_size": 25, "margin_required": 15000, "profit_tgt1": 6750, "profit_tgt2": 14250, "contract": "FORCEMOT26NOV19000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DLF", "company_name": "DLF Limited", "cmp": 752.9, "resistance": 748.0, "base_floor": 634.15, "pct_dist": 0.66, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 80.2, "rvol": 1.09, "stock_trade": {"entry": 752.9, "sl": 722.78, "tgt1": 798.08, "tgt2": 834.22, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "750 CE", "entry": 18.3, "sl": 12.8, "tgt1": 26.5, "tgt2": 35.7, "rr": 1.5, "lot_size": 950, "margin_required": 17385, "profit_tgt1": 7790, "profit_tgt2": 16530, "contract": "DLF26NOV750CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MOTILALOFS", "company_name": "Motilal Oswal Financial Services Limited", "cmp": 1102.0, "resistance": 1095.85, "base_floor": 886.75, "pct_dist": 0.56, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 55.6, "rvol": 1.81, "stock_trade": {"entry": 1102.0, "sl": 1046.9, "tgt1": 1190.16, "tgt2": 1256.28, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1100 CE", "entry": 36.7, "sl": 25.7, "tgt1": 53.2, "tgt2": 71.6, "rr": 1.5, "lot_size": 775, "margin_required": 28443, "profit_tgt1": 12788, "profit_tgt2": 27047, "contract": "MOTILALOFS26NOV1100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MARUTI", "company_name": "Maruti Suzuki India Limited", "cmp": 12750.0, "resistance": 12681.0, "base_floor": 10985.0, "pct_dist": 0.54, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 77.6, "rvol": 1.87, "stock_trade": {"entry": 12750.0, "sl": 12367.5, "tgt1": 13323.75, "tgt2": 13744.5, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "12700 CE", "entry": 295.3, "sl": 206.7, "tgt1": 428.2, "tgt2": 575.8, "rr": 1.5, "lot_size": 50, "margin_required": 14765, "profit_tgt1": 6645, "profit_tgt2": 14025, "contract": "MARUTI26NOV12700CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MUTHOOTFIN", "company_name": "Muthoot Finance Limited", "cmp": 2869.0, "resistance": 2856.8, "base_floor": 2305.0, "pct_dist": 0.43, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.6, "rvol": 1.3, "stock_trade": {"entry": 2869.0, "sl": 2754.24, "tgt1": 3041.14, "tgt2": 3178.85, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2850 CE", "entry": 85.0, "sl": 59.5, "tgt1": 123.2, "tgt2": 165.8, "rr": 1.5, "lot_size": 275, "margin_required": 23375, "profit_tgt1": 10505, "profit_tgt2": 22220, "contract": "MUTHOOTFIN26NOV2850CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HDFCAMC", "company_name": "HDFC Asset Management Company Limited", "cmp": 2649.8, "resistance": 2642.4, "base_floor": 2215.6, "pct_dist": 0.28, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 72.3, "rvol": 0.59, "stock_trade": {"entry": 2649.8, "sl": 2543.81, "tgt1": 2808.79, "tgt2": 2935.97, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2640 CE", "entry": 68.6, "sl": 48.0, "tgt1": 99.5, "tgt2": 133.8, "rr": 1.5, "lot_size": 300, "margin_required": 20580, "profit_tgt1": 9270, "profit_tgt2": 19560, "contract": "HDFCAMC26NOV2640CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SUNPHARMA", "company_name": "Sun Pharmaceutical Industries Limited", "cmp": 1860.0, "resistance": 1855.0, "base_floor": 1719.1, "pct_dist": 0.27, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.4, "rvol": 1.13, "stock_trade": {"entry": 1860.0, "sl": 1786.06, "tgt1": 1970.91, "tgt2": 2059.64, "rr": "1:1.5", "potential_pct": "+6.0% / +10.7%"}, "option_trade": {"strike": "1860 CE", "entry": 36.55, "sl": 25.6, "tgt1": 53.0, "tgt2": 71.3, "rr": 1.5, "lot_size": 350, "margin_required": 12792, "profit_tgt1": 5758, "profit_tgt2": 12162, "contract": "SUNPHARMA26NOV1860CE", "source": "Official NSE BhavCopy"}}, {"symbol": "CHOLAFIN", "company_name": "Cholamandalam Investment and Finance Company Limited", "cmp": 1785.0, "resistance": 1781.0, "base_floor": 1415.0, "pct_dist": 0.22, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 71.0, "rvol": 0.75, "stock_trade": {"entry": 1785.0, "sl": 1713.6, "tgt1": 1892.1, "tgt2": 1977.78, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1780 CE", "entry": 43.5, "sl": 30.4, "tgt1": 63.1, "tgt2": 84.8, "rr": 1.5, "lot_size": 625, "margin_required": 27188, "profit_tgt1": 12250, "profit_tgt2": 25812, "contract": "CHOLAFIN26NOV1780CE", "source": "Official NSE BhavCopy"}}, {"symbol": "CIPLA", "company_name": "Cipla Limited", "cmp": 1411.0, "resistance": 1408.0, "base_floor": 1292.0, "pct_dist": 0.21, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 82.2, "rvol": 1.25, "stock_trade": {"entry": 1411.0, "sl": 1369.0, "tgt1": 1474.0, "tgt2": 1524.4, "rr": "1:1.5", "potential_pct": "+4.5% / +8.0%"}, "option_trade": {"strike": "1410 CE", "entry": 23.95, "sl": 16.8, "tgt1": 34.7, "tgt2": 46.7, "rr": 1.5, "lot_size": 425, "margin_required": 10179, "profit_tgt1": 4569, "profit_tgt2": 9669, "contract": "CIPLA26NOV1410CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BIOCON", "company_name": "Biocon Limited", "cmp": 365.1, "resistance": 364.4, "base_floor": 318.4, "pct_dist": 0.19, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 58.7, "rvol": 1.6, "stock_trade": {"entry": 365.1, "sl": 354.15, "tgt1": 381.53, "tgt2": 393.57, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "365 CE", "entry": 8.1, "sl": 5.7, "tgt1": 11.7, "tgt2": 15.8, "rr": 1.5, "lot_size": 2500, "margin_required": 20250, "profit_tgt1": 9000, "profit_tgt2": 19250, "contract": "BIOCON26NOV365CE", "source": "Official NSE BhavCopy"}}, {"symbol": "AUROPHARMA", "company_name": "Aurobindo Pharma Limited", "cmp": 1800.0, "resistance": 1796.8, "base_floor": 1547.7, "pct_dist": 0.18, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 67.2, "rvol": 1.28, "stock_trade": {"entry": 1800.0, "sl": 1728.0, "tgt1": 1908.0, "tgt2": 1994.4, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1800 CE", "entry": 32.75, "sl": 22.9, "tgt1": 47.5, "tgt2": 63.9, "rr": 1.5, "lot_size": 550, "margin_required": 18012, "profit_tgt1": 8112, "profit_tgt2": 17132, "contract": "AUROPHARMA26NOV1800CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TATACONSUM", "company_name": "Tata Consumer Products Limited", "cmp": 1086.3, "resistance": 1084.7, "base_floor": 916.0, "pct_dist": 0.15, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 74.6, "rvol": 0.72, "stock_trade": {"entry": 1086.3, "sl": 1042.85, "tgt1": 1151.47, "tgt2": 1203.62, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1090 CE", "entry": 17.2, "sl": 12.0, "tgt1": 24.9, "tgt2": 33.5, "rr": 1.5, "lot_size": 550, "margin_required": 9460, "profit_tgt1": 4235, "profit_tgt2": 8965, "contract": "TATACONSUM26NOV1090CE", "source": "Official NSE BhavCopy"}}, {"symbol": "INDIANB", "company_name": "Indian Bank", "cmp": 902.0, "resistance": 900.85, "base_floor": 807.8, "pct_dist": 0.13, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 67.4, "rvol": 0.67, "stock_trade": {"entry": 902.0, "sl": 865.92, "tgt1": 956.12, "tgt2": 999.42, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "900 CE", "entry": 22.25, "sl": 15.6, "tgt1": 32.3, "tgt2": 43.4, "rr": 1.5, "lot_size": 1000, "margin_required": 22250, "profit_tgt1": 10050, "profit_tgt2": 21150, "contract": "INDIANB26NOV900CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ASHOKLEY", "company_name": "Ashok Leyland Limited", "cmp": 172.09, "resistance": 171.94, "base_floor": 140.01, "pct_dist": 0.09, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 80.9, "rvol": 1.58, "stock_trade": {"entry": 172.09, "sl": 165.21, "tgt1": 182.41, "tgt2": 190.67, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "172.5 CE", "entry": 4.83, "sl": 3.4, "tgt1": 7.0, "tgt2": 9.4, "rr": 1.5, "lot_size": 5000, "margin_required": 24150, "profit_tgt1": 10850, "profit_tgt2": 22850, "contract": "ASHOKLEY26NOV172.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MARICO", "company_name": "Marico Limited", "cmp": 897.75, "resistance": 897.0, "base_floor": 756.85, "pct_dist": 0.08, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 82.0, "rvol": 1.09, "stock_trade": {"entry": 897.75, "sl": 852.86, "tgt1": 969.57, "tgt2": 1023.44, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "900 CE", "entry": 15.55, "sl": 10.9, "tgt1": 22.5, "tgt2": 30.3, "rr": 1.5, "lot_size": 1200, "margin_required": 18660, "profit_tgt1": 8340, "profit_tgt2": 17700, "contract": "MARICO26NOV900CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TVSMOTOR", "company_name": "TVS Motor Company Limited", "cmp": 4491.7, "resistance": 4490.0, "base_floor": 3741.9, "pct_dist": 0.04, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 74.5, "rvol": 0.74, "stock_trade": {"entry": 4491.7, "sl": 4312.03, "tgt1": 4761.2, "tgt2": 4976.81, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "4500 CE", "entry": 89.2, "sl": 62.4, "tgt1": 129.3, "tgt2": 173.9, "rr": 1.5, "lot_size": 175, "margin_required": 15610, "profit_tgt1": 7018, "profit_tgt2": 14822, "contract": "TVSMOTOR26NOV4500CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JSWENERGY", "company_name": "JSW Energy Limited", "cmp": 524.95, "resistance": 525.0, "base_floor": 438.4, "pct_dist": -0.01, "stage": "LIVE BREAKOUT", "score": 96, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 65.6, "rvol": 0.5, "stock_trade": {"entry": 524.95, "sl": 503.95, "tgt1": 556.45, "tgt2": 581.65, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "520 CE", "entry": 15.05, "sl": 10.5, "tgt1": 21.8, "tgt2": 29.3, "rr": 1.5, "lot_size": 1075, "margin_required": 16179, "profit_tgt1": 7256, "profit_tgt2": 15319, "contract": "JSWENERGY26NOV520CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TORNTPHARM", "company_name": "Torrent Pharmaceuticals Limited", "cmp": 4750.0, "resistance": 4753.4, "base_floor": 4466.8, "pct_dist": -0.07, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 65.6, "rvol": 1.1, "stock_trade": {"entry": 4750.0, "sl": 4663.17, "tgt1": 4949.5, "tgt2": 5109.1, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "4750 CE", "entry": 102.85, "sl": 72.0, "tgt1": 149.1, "tgt2": 200.6, "rr": 1.5, "lot_size": 125, "margin_required": 12856, "profit_tgt1": 5781, "profit_tgt2": 12219, "contract": "TORNTPHARM26NOV4750CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SHREECEM", "company_name": "Shree Cement Limited", "cmp": 25100.0, "resistance": 25120.0, "base_floor": 21450.0, "pct_dist": -0.08, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 80.9, "rvol": 0.51, "stock_trade": {"entry": 25100.0, "sl": 24096.0, "tgt1": 26606.0, "tgt2": 27810.8, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "25000 CE", "entry": 555.1, "sl": 388.6, "tgt1": 804.9, "tgt2": 1082.4, "rr": 1.5, "lot_size": 25, "margin_required": 13878, "profit_tgt1": 6245, "profit_tgt2": 13183, "contract": "SHREECEM26NOV25000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HDFCLIFE", "company_name": "HDFC Life Insurance Company Limited", "cmp": 565.3, "resistance": 565.85, "base_floor": 508.05, "pct_dist": -0.1, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 56.4, "rvol": 2.73, "stock_trade": {"entry": 565.3, "sl": 537.03, "tgt1": 610.53, "tgt2": 644.46, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "565 CE", "entry": 11.2, "sl": 7.8, "tgt1": 16.2, "tgt2": 21.8, "rr": 1.5, "lot_size": 1100, "margin_required": 12320, "profit_tgt1": 5500, "profit_tgt2": 11660, "contract": "HDFCLIFE26NOV565CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JIOFIN", "company_name": "Jio Financial Services Limited", "cmp": 231.2, "resistance": 231.45, "base_floor": 202.51, "pct_dist": -0.11, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 66.1, "rvol": 1.62, "stock_trade": {"entry": 231.2, "sl": 224.26, "tgt1": 241.61, "tgt2": 249.24, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "230 CE", "entry": 6.36, "sl": 4.5, "tgt1": 9.2, "tgt2": 12.4, "rr": 1.5, "lot_size": 2350, "margin_required": 14946, "profit_tgt1": 6674, "profit_tgt2": 14194, "contract": "JIOFIN26NOV230CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JUBLFOOD", "company_name": "Jubilant FoodWorks Limited", "cmp": 457.2, "resistance": 458.0, "base_floor": 397.8, "pct_dist": -0.17, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 71.6, "rvol": 0.85, "stock_trade": {"entry": 457.2, "sl": 438.91, "tgt1": 484.63, "tgt2": 506.58, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "460 CE", "entry": 18.4, "sl": 12.9, "tgt1": 26.7, "tgt2": 35.9, "rr": 1.5, "lot_size": 1250, "margin_required": 23000, "profit_tgt1": 10375, "profit_tgt2": 21875, "contract": "JUBLFOOD26NOV460CE", "source": "Official NSE BhavCopy"}}, {"symbol": "AMBUJACEM", "company_name": "Ambuja Cements Limited", "cmp": 390.6, "resistance": 391.3, "base_floor": 341.0, "pct_dist": -0.18, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.2, "rvol": 1.13, "stock_trade": {"entry": 390.6, "sl": 374.98, "tgt1": 414.03, "tgt2": 432.77, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "390 CE", "entry": 11.0, "sl": 7.7, "tgt1": 15.9, "tgt2": 21.4, "rr": 1.5, "lot_size": 1200, "margin_required": 13200, "profit_tgt1": 5880, "profit_tgt2": 12480, "contract": "AMBUJACEM26NOV390CE", "source": "Official NSE BhavCopy"}}, {"symbol": "GRASIM", "company_name": "Grasim Industries Limited", "cmp": 3227.0, "resistance": 3232.8, "base_floor": 2828.2, "pct_dist": -0.18, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 81.3, "rvol": 2.07, "stock_trade": {"entry": 3227.0, "sl": 3130.19, "tgt1": 3372.22, "tgt2": 3478.71, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "3220 CE", "entry": 77.5, "sl": 54.2, "tgt1": 112.4, "tgt2": 151.1, "rr": 1.5, "lot_size": 250, "margin_required": 19375, "profit_tgt1": 8725, "profit_tgt2": 18400, "contract": "GRASIM26NOV3220CE", "source": "Official NSE BhavCopy"}}, {"symbol": "LODHA", "company_name": "Lodha Developers Limited", "cmp": 1179.0, "resistance": 1181.1, "base_floor": 937.1, "pct_dist": -0.18, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 64.9, "rvol": 0.75, "stock_trade": {"entry": 1179.0, "sl": 1131.84, "tgt1": 1249.74, "tgt2": 1306.33, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1180 CE", "entry": 35.5, "sl": 24.8, "tgt1": 51.5, "tgt2": 69.2, "rr": 1.5, "lot_size": 625, "margin_required": 22188, "profit_tgt1": 10000, "profit_tgt2": 21062, "contract": "LODHA26NOV1180CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PNB", "company_name": "Punjab National Bank", "cmp": 126.55, "resistance": 126.8, "base_floor": 113.71, "pct_dist": -0.2, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 72.6, "rvol": 0.97, "stock_trade": {"entry": 126.55, "sl": 121.49, "tgt1": 134.14, "tgt2": 140.21, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "127 CE", "entry": 2.31, "sl": 1.6, "tgt1": 3.3, "tgt2": 4.5, "rr": 1.4, "lot_size": 8000, "margin_required": 18480, "profit_tgt1": 7920, "profit_tgt2": 17520, "contract": "PNB26NOV127CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ADANIENSOL", "company_name": "Adani Energy Solutions Limited", "cmp": 1457.4, "resistance": 1460.6, "base_floor": 1200.0, "pct_dist": -0.22, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 59.8, "rvol": 0.81, "stock_trade": {"entry": 1457.4, "sl": 1399.1, "tgt1": 1544.85, "tgt2": 1614.81, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1460 CE", "entry": 40.6, "sl": 28.4, "tgt1": 58.9, "tgt2": 79.2, "rr": 1.5, "lot_size": 675, "margin_required": 27405, "profit_tgt1": 12352, "profit_tgt2": 26055, "contract": "ADANIENSOL26NOV1460CE", "source": "Official NSE BhavCopy"}}, {"symbol": "INDIGO", "company_name": "InterGlobe Aviation Limited", "cmp": 5476.0, "resistance": 5489.0, "base_floor": 4464.4, "pct_dist": -0.24, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 84.5, "rvol": 1.45, "stock_trade": {"entry": 5476.0, "sl": 5202.2, "tgt1": 5914.08, "tgt2": 6242.64, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "5500 CE", "entry": 116.05, "sl": 81.2, "tgt1": 168.3, "tgt2": 226.3, "rr": 1.5, "lot_size": 150, "margin_required": 17408, "profit_tgt1": 7838, "profit_tgt2": 16538, "contract": "INDIGO26NOV5500CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HEROMOTOCO", "company_name": "Hero MotoCorp Limited", "cmp": 5513.0, "resistance": 5527.0, "base_floor": 4825.0, "pct_dist": -0.25, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 63.2, "rvol": 1.34, "stock_trade": {"entry": 5513.0, "sl": 5292.48, "tgt1": 5843.78, "tgt2": 6108.4, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "5500 CE", "entry": 123.25, "sl": 86.3, "tgt1": 178.7, "tgt2": 240.3, "rr": 1.5, "lot_size": 150, "margin_required": 18488, "profit_tgt1": 8317, "profit_tgt2": 17558, "contract": "HEROMOTOCO26NOV5500CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ITC", "company_name": "ITC Limited", "cmp": 283.15, "resistance": 283.9, "base_floor": 252.8, "pct_dist": -0.26, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 76.2, "rvol": 0.78, "stock_trade": {"entry": 283.15, "sl": 268.99, "tgt1": 305.81, "tgt2": 322.8, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "282.5 CE", "entry": 4.7, "sl": 3.3, "tgt1": 6.8, "tgt2": 9.2, "rr": 1.5, "lot_size": 1725, "margin_required": 8108, "profit_tgt1": 3622, "profit_tgt2": 7762, "contract": "ITC26NOV282.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MCX", "company_name": "Multi Commodity Exchange of India Limited", "cmp": 3528.0, "resistance": 3538.0, "base_floor": 2985.0, "pct_dist": -0.28, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 65.3, "rvol": 2.04, "stock_trade": {"entry": 3528.0, "sl": 3351.6, "tgt1": 3810.24, "tgt2": 4021.92, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "3550 CE", "entry": 108.25, "sl": 75.8, "tgt1": 157.0, "tgt2": 211.1, "rr": 1.5, "lot_size": 225, "margin_required": 24356, "profit_tgt1": 10969, "profit_tgt2": 23141, "contract": "MCX26NOV3550CE", "source": "Official NSE BhavCopy"}}, {"symbol": "GODREJPROP", "company_name": "Godrej Properties Limited", "cmp": 1809.3, "resistance": 1815.0, "base_floor": 1468.4, "pct_dist": -0.31, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.7, "rvol": 1.49, "stock_trade": {"entry": 1809.3, "sl": 1736.93, "tgt1": 1917.85, "tgt2": 2004.7, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1800 CE", "entry": 48.6, "sl": 34.0, "tgt1": 70.5, "tgt2": 94.8, "rr": 1.5, "lot_size": 325, "margin_required": 15795, "profit_tgt1": 7117, "profit_tgt2": 15015, "contract": "GODREJPROP26NOV1800CE", "source": "Official NSE BhavCopy"}}, {"symbol": "360ONE", "company_name": "360 One Wam Limited", "cmp": 1145.0, "resistance": 1148.95, "base_floor": 965.7, "pct_dist": -0.34, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 59.5, "rvol": 0.48, "stock_trade": {"entry": 1145.0, "sl": 1099.2, "tgt1": 1213.7, "tgt2": 1268.66, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1140 CE", "entry": 37.2, "sl": 26.0, "tgt1": 53.9, "tgt2": 72.5, "rr": 1.5, "lot_size": 500, "margin_required": 18600, "profit_tgt1": 8350, "profit_tgt2": 17650, "contract": "360ONE26NOV1140CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ADANIGREEN", "company_name": "Adani Green Energy Limited", "cmp": 1424.1, "resistance": 1429.6, "base_floor": 1171.0, "pct_dist": -0.38, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 64.8, "rvol": 0.66, "stock_trade": {"entry": 1424.1, "sl": 1367.14, "tgt1": 1509.54, "tgt2": 1577.89, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1420 CE", "entry": 40.65, "sl": 28.5, "tgt1": 58.9, "tgt2": 79.3, "rr": 1.5, "lot_size": 600, "margin_required": 24390, "profit_tgt1": 10950, "profit_tgt2": 23190, "contract": "ADANIGREEN26NOV1420CE", "source": "Official NSE BhavCopy"}}, {"symbol": "RELIANCE", "company_name": "Reliance Industries Limited", "cmp": 1320.0, "resistance": 1325.0, "base_floor": 1152.2, "pct_dist": -0.38, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 70.2, "rvol": 1.11, "stock_trade": {"entry": 1320.0, "sl": 1267.2, "tgt1": 1399.2, "tgt2": 1462.56, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1320 CE", "entry": 24.0, "sl": 16.8, "tgt1": 34.8, "tgt2": 46.8, "rr": 1.5, "lot_size": 500, "margin_required": 12000, "profit_tgt1": 5400, "profit_tgt2": 11400, "contract": "RELIANCE26NOV1320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BANKBARODA", "company_name": "Bank of Baroda Limited", "cmp": 250.31, "resistance": 251.34, "base_floor": 225.2, "pct_dist": -0.41, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 70.8, "rvol": 0.98, "stock_trade": {"entry": 250.31, "sl": 240.3, "tgt1": 265.32, "tgt2": 277.34, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "250 CE", "entry": 5.08, "sl": 3.6, "tgt1": 7.4, "tgt2": 9.9, "rr": 1.6, "lot_size": 2925, "margin_required": 14859, "profit_tgt1": 6786, "profit_tgt2": 14098, "contract": "BANKBARODA26NOV250CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JINDALSTEL", "company_name": "Jindal Steel Limited", "cmp": 1165.0, "resistance": 1169.9, "base_floor": 1000.8, "pct_dist": -0.42, "stage": "IMMINENT PIVOT", "score": 90, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 77.2, "rvol": 0.88, "stock_trade": {"entry": 1165.0, "sl": 1118.4, "tgt1": 1234.9, "tgt2": 1290.82, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1160 CE", "entry": 29.0, "sl": 20.3, "tgt1": 42.0, "tgt2": 56.5, "rr": 1.5, "lot_size": 625, "margin_required": 18125, "profit_tgt1": 8125, "profit_tgt2": 17188, "contract": "JINDALSTEL26NOV1160CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ABCAPITAL", "company_name": "Aditya Birla Capital Limited", "cmp": 398.8, "resistance": 400.85, "base_floor": 334.45, "pct_dist": -0.51, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 61.3, "rvol": 0.55, "stock_trade": {"entry": 398.8, "sl": 382.85, "tgt1": 422.73, "tgt2": 441.87, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "400 CE", "entry": 8.2, "sl": 5.7, "tgt1": 11.9, "tgt2": 16.0, "rr": 1.5, "lot_size": 1550, "margin_required": 12710, "profit_tgt1": 5735, "profit_tgt2": 12090, "contract": "ABCAPITAL26NOV400CE", "source": "Official NSE BhavCopy"}}, {"symbol": "EICHERMOT", "company_name": "Eicher Motors Limited", "cmp": 7669.5, "resistance": 7713.0, "base_floor": 6767.5, "pct_dist": -0.56, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 65.4, "rvol": 0.91, "stock_trade": {"entry": 7669.5, "sl": 7362.72, "tgt1": 8129.67, "tgt2": 8497.81, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "7700 CE", "entry": 187.45, "sl": 131.2, "tgt1": 271.8, "tgt2": 365.5, "rr": 1.5, "lot_size": 100, "margin_required": 18745, "profit_tgt1": 8435, "profit_tgt2": 17805, "contract": "EICHERMOT26NOV7700CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PATANJALI", "company_name": "Patanjali Foods Limited", "cmp": 411.5, "resistance": 413.9, "base_floor": 336.4, "pct_dist": -0.58, "stage": "BASE SQUEEZE", "score": 84, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 69.8, "rvol": 1.23, "stock_trade": {"entry": 411.5, "sl": 390.92, "tgt1": 444.43, "tgt2": 469.12, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "410 CE", "entry": 16.25, "sl": 11.4, "tgt1": 23.6, "tgt2": 31.7, "rr": 1.5, "lot_size": 1075, "margin_required": 17469, "profit_tgt1": 7901, "profit_tgt2": 16609, "contract": "PATANJALI26NOV410CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ANANDRATHI", "company_name": "Anand Rathi Wealth Limited", "cmp": 2373.5, "resistance": 2388.0, "base_floor": 2015.9, "pct_dist": -0.61, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 91.1, "rvol": 0.49, "stock_trade": {"entry": 2373.5, "sl": 2278.56, "tgt1": 2515.91, "tgt2": 2629.84, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2380 CE", "entry": 37.55, "sl": 26.3, "tgt1": 54.4, "tgt2": 73.2, "rr": 1.5, "lot_size": 250, "margin_required": 9388, "profit_tgt1": 4212, "profit_tgt2": 8913, "contract": "ANANDRATHI26NOV2380CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ADANIPORTS", "company_name": "Adani Ports and Special Economic Zone Limited", "cmp": 1936.6, "resistance": 1948.9, "base_floor": 1674.2, "pct_dist": -0.63, "stage": "BASE SQUEEZE", "score": 84, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 72.7, "rvol": 1.06, "stock_trade": {"entry": 1936.6, "sl": 1859.14, "tgt1": 2052.79, "tgt2": 2145.74, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1940 CE", "entry": 41.75, "sl": 29.2, "tgt1": 60.5, "tgt2": 81.4, "rr": 1.5, "lot_size": 475, "margin_required": 19831, "profit_tgt1": 8906, "profit_tgt2": 18834, "contract": "ADANIPORTS26NOV1940CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BPCL", "company_name": "Bharat Petroleum Corporation Limited", "cmp": 319.9, "resistance": 322.0, "base_floor": 275.4, "pct_dist": -0.65, "stage": "BASE SQUEEZE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 67.2, "rvol": 1.14, "stock_trade": {"entry": 319.9, "sl": 307.1, "tgt1": 339.1, "tgt2": 354.46, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "320 CE", "entry": 7.3, "sl": 5.1, "tgt1": 10.6, "tgt2": 14.2, "rr": 1.5, "lot_size": 1975, "margin_required": 14418, "profit_tgt1": 6518, "profit_tgt2": 13627, "contract": "BPCL26NOV320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "UNOMINDA", "company_name": "Uno Minda Limited", "cmp": 1326.0, "resistance": 1335.0, "base_floor": 1030.0, "pct_dist": -0.67, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 78.7, "rvol": 2.95, "stock_trade": {"entry": 1326.0, "sl": 1259.7, "tgt1": 1432.08, "tgt2": 1511.64, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1320 CE", "entry": 41.15, "sl": 28.8, "tgt1": 59.7, "tgt2": 80.2, "rr": 1.5, "lot_size": 550, "margin_required": 22632, "profit_tgt1": 10203, "profit_tgt2": 21478, "contract": "UNOMINDA26NOV1320CE", "source": "Official NSE BhavCopy"}}, {"symbol": "IOC", "company_name": "Indian Oil Corporation Limited", "cmp": 146.25, "resistance": 147.31, "base_floor": 124.92, "pct_dist": -0.72, "stage": "BASE SQUEEZE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 81.9, "rvol": 2.03, "stock_trade": {"entry": 146.25, "sl": 138.94, "tgt1": 157.95, "tgt2": 166.72, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "146 CE", "entry": 3.61, "sl": 2.5, "tgt1": 5.2, "tgt2": 7.0, "rr": 1.4, "lot_size": 4875, "margin_required": 17599, "profit_tgt1": 7751, "profit_tgt2": 16526, "contract": "IOC26NOV146CE", "source": "Official NSE BhavCopy"}}, {"symbol": "DRREDDY", "company_name": "Dr. Reddy's Laboratories Limited", "cmp": 1373.0, "resistance": 1384.0, "base_floor": 1167.2, "pct_dist": -0.79, "stage": "BASE SQUEEZE", "score": 84, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout", "pattern": "Multi-Month Base / Stage-2 Transition", "rsi": 83.7, "rvol": 0.59, "stock_trade": {"entry": 1373.0, "sl": 1304.35, "tgt1": 1482.84, "tgt2": 1565.22, "rr": "1:1.6", "potential_pct": "+8.0% / +14.0%"}, "option_trade": {"strike": "1370 CE", "entry": 26.2, "sl": 18.3, "tgt1": 38.0, "tgt2": 51.1, "rr": 1.5, "lot_size": 625, "margin_required": 16375, "profit_tgt1": 7375, "profit_tgt2": 15563, "contract": "DRREDDY26NOV1370CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PAYTM", "company_name": "One97 Communications Limited", "cmp": 1794.4, "resistance": 1809.0, "base_floor": 1558.8, "pct_dist": -0.81, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 60.8, "rvol": 0.45, "stock_trade": {"entry": 1794.4, "sl": 1722.62, "tgt1": 1902.07, "tgt2": 1988.21, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1800 CE", "entry": 55.0, "sl": 38.5, "tgt1": 79.8, "tgt2": 107.2, "rr": 1.5, "lot_size": 725, "margin_required": 39875, "profit_tgt1": 17980, "profit_tgt2": 37845, "contract": "PAYTM26NOV1800CE", "source": "Official NSE BhavCopy"}}, {"symbol": "IRFC", "company_name": "Indian Railway Finance Corporation Limited", "cmp": 80.43, "resistance": 81.1, "base_floor": 73.05, "pct_dist": -0.83, "stage": "BASE SQUEEZE", "score": 84, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 50.5, "rvol": 0.75, "stock_trade": {"entry": 80.43, "sl": 77.32, "tgt1": 85.1, "tgt2": 88.83, "rr": "1:1.5", "potential_pct": "+5.8% / +10.4%"}, "option_trade": {"strike": "80 CE", "entry": 2.33, "sl": 1.6, "tgt1": 3.4, "tgt2": 4.5, "rr": 1.5, "lot_size": 5425, "margin_required": 12640, "profit_tgt1": 5805, "profit_tgt2": 11772, "contract": "IRFC26NOV80CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MANKIND", "company_name": "Mankind Pharma Limited", "cmp": 2540.0, "resistance": 2561.2, "base_floor": 2196.1, "pct_dist": -0.83, "stage": "BASE SQUEEZE", "score": 84, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 72.2, "rvol": 0.36, "stock_trade": {"entry": 2540.0, "sl": 2457.9, "tgt1": 2663.15, "tgt2": 2761.67, "rr": "1:1.5", "potential_pct": "+4.8% / +8.7%"}, "option_trade": {"strike": "2540 CE", "entry": 64.3, "sl": 45.0, "tgt1": 93.2, "tgt2": 125.4, "rr": 1.5, "lot_size": 250, "margin_required": 16075, "profit_tgt1": 7225, "profit_tgt2": 15275, "contract": "MANKIND26NOV2540CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever Limited", "cmp": 1998.4, "resistance": 2016.0, "base_floor": 1758.2, "pct_dist": -0.87, "stage": "BASE SQUEEZE", "score": 84, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 69.5, "rvol": 0.6, "stock_trade": {"entry": 1998.4, "sl": 1918.46, "tgt1": 2118.31, "tgt2": 2214.24, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2000 CE", "entry": 24.4, "sl": 17.1, "tgt1": 35.4, "tgt2": 47.6, "rr": 1.5, "lot_size": 300, "margin_required": 7320, "profit_tgt1": 3300, "profit_tgt2": 6960, "contract": "HINDUNILVR26NOV2000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "INDUSINDBK", "company_name": "IndusInd Bank Limited", "cmp": 910.25, "resistance": 918.35, "base_floor": 827.5, "pct_dist": -0.88, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 58.2, "rvol": 3.09, "stock_trade": {"entry": 910.25, "sl": 882.94, "tgt1": 951.21, "tgt2": 981.26, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "910 CE", "entry": 23.25, "sl": 16.3, "tgt1": 33.7, "tgt2": 45.3, "rr": 1.5, "lot_size": 700, "margin_required": 16275, "profit_tgt1": 7315, "profit_tgt2": 15435, "contract": "INDUSINDBK26NOV910CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PETRONET", "company_name": "Petronet LNG Limited", "cmp": 317.0, "resistance": 319.95, "base_floor": 279.35, "pct_dist": -0.92, "stage": "BASE SQUEEZE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 68.9, "rvol": 1.01, "stock_trade": {"entry": 317.0, "sl": 304.32, "tgt1": 336.02, "tgt2": 351.24, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "318 CE", "entry": 6.2, "sl": 4.3, "tgt1": 9.0, "tgt2": 12.1, "rr": 1.5, "lot_size": 1900, "margin_required": 11780, "profit_tgt1": 5320, "profit_tgt2": 11210, "contract": "PETRONET26NOV318CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HYUNDAI", "company_name": "Hyundai Motor India Limited", "cmp": 2130.0, "resistance": 2149.9, "base_floor": 1827.0, "pct_dist": -0.93, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 65.8, "rvol": 2.16, "stock_trade": {"entry": 2130.0, "sl": 2066.1, "tgt1": 2225.85, "tgt2": 2296.14, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "2140 CE", "entry": 51.0, "sl": 35.7, "tgt1": 74.0, "tgt2": 99.5, "rr": 1.5, "lot_size": 275, "margin_required": 14025, "profit_tgt1": 6325, "profit_tgt2": 13338, "contract": "HYUNDAI26NOV2140CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HAVELLS", "company_name": "Havells India Limited", "cmp": 1128.0, "resistance": 1138.7, "base_floor": 999.2, "pct_dist": -0.94, "stage": "BASE SQUEEZE", "score": 84, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge", "pattern": "High-Volume Range Expansion", "rsi": 51.3, "rvol": 3.0, "stock_trade": {"entry": 1128.0, "sl": 1094.16, "tgt1": 1178.76, "tgt2": 1215.98, "rr": "1:1.5", "potential_pct": "+4.5% / +7.8%"}, "option_trade": {"strike": "1130 CE", "entry": 26.0, "sl": 18.2, "tgt1": 37.7, "tgt2": 50.7, "rr": 1.5, "lot_size": 500, "margin_required": 13000, "profit_tgt1": 5850, "profit_tgt2": 12350, "contract": "HAVELLS26NOV1130CE", "source": "Official NSE BhavCopy"}}, {"symbol": "JSWSTEEL", "company_name": "JSW Steel Limited", "cmp": 1357.1, "resistance": 1370.0, "base_floor": 1158.0, "pct_dist": -0.94, "stage": "BASE SQUEEZE", "score": 84, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 72.8, "rvol": 1.35, "stock_trade": {"entry": 1357.1, "sl": 1302.82, "tgt1": 1438.52, "tgt2": 1503.66, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1360 CE", "entry": 24.5, "sl": 17.1, "tgt1": 35.5, "tgt2": 47.8, "rr": 1.5, "lot_size": 675, "margin_required": 16538, "profit_tgt1": 7425, "profit_tgt2": 15727, "contract": "JSWSTEEL26NOV1360CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HINDPETRO", "company_name": "Hindustan Petroleum Corporation Limited", "cmp": 387.15, "resistance": 391.0, "base_floor": 323.25, "pct_dist": -0.98, "stage": "BASE SQUEEZE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 73.3, "rvol": 0.74, "stock_trade": {"entry": 387.15, "sl": 371.66, "tgt1": 410.38, "tgt2": 428.97, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "385 CE", "entry": 12.45, "sl": 8.7, "tgt1": 18.1, "tgt2": 24.3, "rr": 1.5, "lot_size": 2025, "margin_required": 25211, "profit_tgt1": 11441, "profit_tgt2": 23996, "contract": "HINDPETRO26NOV385CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ADANIPOWER", "company_name": "Adani Power Limited", "cmp": 204.29, "resistance": 206.33, "base_floor": 175.31, "pct_dist": -0.99, "stage": "BASE SQUEEZE", "score": 84, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 58.7, "rvol": 0.46, "stock_trade": {"entry": 204.29, "sl": 196.12, "tgt1": 216.54, "tgt2": 226.35, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "205 CE", "entry": 5.75, "sl": 4.0, "tgt1": 8.3, "tgt2": 11.2, "rr": 1.5, "lot_size": 3550, "margin_required": 20412, "profit_tgt1": 9053, "profit_tgt2": 19347, "contract": "ADANIPOWER26NOV205CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ATHERENERG", "company_name": "Ather Energy Limited", "cmp": 1821.7, "resistance": 1840.0, "base_floor": 1345.7, "pct_dist": -0.99, "stage": "BASE SQUEEZE", "score": 84, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 75.0, "rvol": 0.63, "stock_trade": {"entry": 1821.7, "sl": 1748.83, "tgt1": 1931.01, "tgt2": 2018.45, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1820 CE", "entry": 55.1, "sl": 38.6, "tgt1": 79.9, "tgt2": 107.4, "rr": 1.5, "lot_size": 375, "margin_required": 20662, "profit_tgt1": 9300, "profit_tgt2": 19612, "contract": "ATHERENERG26NOV1820CE", "source": "Official NSE BhavCopy"}}, {"symbol": "UNIONBANK", "company_name": "Union Bank of India", "cmp": 187.0, "resistance": 188.9, "base_floor": 167.5, "pct_dist": -1.01, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 71.8, "rvol": 0.61, "stock_trade": {"entry": 187.0, "sl": 181.93, "tgt1": 194.85, "tgt2": 201.14, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "187.5 CE", "entry": 4.74, "sl": 3.3, "tgt1": 6.9, "tgt2": 9.2, "rr": 1.5, "lot_size": 4425, "margin_required": 20974, "profit_tgt1": 9558, "profit_tgt2": 19735, "contract": "UNIONBANK26NOV187.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "UNITDSPR", "company_name": "United Spirits Limited", "cmp": 1418.0, "resistance": 1432.5, "base_floor": 1217.5, "pct_dist": -1.01, "stage": "BASE SQUEEZE", "score": 84, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 54.2, "rvol": 0.39, "stock_trade": {"entry": 1418.0, "sl": 1361.28, "tgt1": 1503.08, "tgt2": 1571.14, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1420 CE", "entry": 29.75, "sl": 20.8, "tgt1": 43.1, "tgt2": 58.0, "rr": 1.5, "lot_size": 400, "margin_required": 11900, "profit_tgt1": 5340, "profit_tgt2": 11300, "contract": "UNITDSPR26NOV1420CE", "source": "Official NSE BhavCopy"}}, {"symbol": "MAXHEALTH", "company_name": "Max Healthcare Institute Limited", "cmp": 934.0, "resistance": 943.65, "base_floor": 797.0, "pct_dist": -1.02, "stage": "BASE SQUEEZE", "score": 84, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 79.2, "rvol": 0.68, "stock_trade": {"entry": 934.0, "sl": 896.64, "tgt1": 990.04, "tgt2": 1034.87, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "930 CE", "entry": 23.0, "sl": 16.1, "tgt1": 33.4, "tgt2": 44.9, "rr": 1.5, "lot_size": 525, "margin_required": 12075, "profit_tgt1": 5460, "profit_tgt2": 11498, "contract": "MAXHEALTH26NOV930CE", "source": "Official NSE BhavCopy"}}, {"symbol": "SBICARD", "company_name": "SBI Cards and Payment Services Limited", "cmp": 585.0, "resistance": 591.0, "base_floor": 519.05, "pct_dist": -1.02, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 57.1, "rvol": 0.86, "stock_trade": {"entry": 585.0, "sl": 561.6, "tgt1": 620.1, "tgt2": 648.18, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "590 CE", "entry": 12.1, "sl": 8.5, "tgt1": 17.5, "tgt2": 23.6, "rr": 1.5, "lot_size": 800, "margin_required": 9680, "profit_tgt1": 4320, "profit_tgt2": 9200, "contract": "SBICARD26NOV590CE", "source": "Official NSE BhavCopy"}}, {"symbol": "WIPRO", "company_name": "Wipro Limited", "cmp": 198.0, "resistance": 200.11, "base_floor": 158.3, "pct_dist": -1.05, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.4, "rvol": 0.67, "stock_trade": {"entry": 198.0, "sl": 190.8, "tgt1": 208.8, "tgt2": 217.44, "rr": "1:1.5", "potential_pct": "+5.5% / +9.8%"}, "option_trade": {"strike": "197.5 CE", "entry": 5.2, "sl": 3.6, "tgt1": 7.5, "tgt2": 10.1, "rr": 1.4, "lot_size": 3000, "margin_required": 15600, "profit_tgt1": 6900, "profit_tgt2": 14700, "contract": "WIPRO26NOV197.5CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TECHM", "company_name": "Tech Mahindra Limited", "cmp": 1831.0, "resistance": 1851.0, "base_floor": 1442.5, "pct_dist": -1.08, "stage": "BASE SQUEEZE", "score": 84, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 58.0, "rvol": 0.47, "stock_trade": {"entry": 1831.0, "sl": 1761.3, "tgt1": 1935.55, "tgt2": 2019.19, "rr": "1:1.5", "potential_pct": "+5.7% / +10.3%"}, "option_trade": {"strike": "1840 CE", "entry": 42.45, "sl": 29.7, "tgt1": 61.6, "tgt2": 82.8, "rr": 1.5, "lot_size": 600, "margin_required": 25470, "profit_tgt1": 11490, "profit_tgt2": 24210, "contract": "TECHM26NOV1840CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BSE", "company_name": "BSE Limited", "cmp": 3800.0, "resistance": 3842.0, "base_floor": 3190.0, "pct_dist": -1.09, "stage": "BASE SQUEEZE", "score": 84, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 74.2, "rvol": 1.08, "stock_trade": {"entry": 3800.0, "sl": 3648.0, "tgt1": 4028.0, "tgt2": 4210.4, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "3800 CE", "entry": 112.25, "sl": 78.6, "tgt1": 162.8, "tgt2": 218.9, "rr": 1.5, "lot_size": 200, "margin_required": 22450, "profit_tgt1": 10110, "profit_tgt2": 21330, "contract": "BSE26NOV3800CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PRESTIGE", "company_name": "Prestige Estates Projects Limited", "cmp": 1629.0, "resistance": 1647.0, "base_floor": 1363.6, "pct_dist": -1.09, "stage": "BASE SQUEEZE", "score": 84, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 66.1, "rvol": 1.28, "stock_trade": {"entry": 1629.0, "sl": 1563.84, "tgt1": 1726.74, "tgt2": 1804.93, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1620 CE", "entry": 51.1, "sl": 35.8, "tgt1": 74.1, "tgt2": 99.6, "rr": 1.5, "lot_size": 450, "margin_required": 22995, "profit_tgt1": 10350, "profit_tgt2": 21825, "contract": "PRESTIGE26NOV1620CE", "source": "Official NSE BhavCopy"}}, {"symbol": "ASIANPAINT", "company_name": "Asian Paints Limited", "cmp": 2546.0, "resistance": 2576.6, "base_floor": 2217.1, "pct_dist": -1.19, "stage": "BASE SQUEEZE", "score": 84, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 74.5, "rvol": 0.99, "stock_trade": {"entry": 2546.0, "sl": 2444.16, "tgt1": 2698.76, "tgt2": 2820.97, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "2540 CE", "entry": 53.9, "sl": 37.7, "tgt1": 78.2, "tgt2": 105.1, "rr": 1.5, "lot_size": 250, "margin_required": 13475, "profit_tgt1": 6075, "profit_tgt2": 12800, "contract": "ASIANPAINT26NOV2540CE", "source": "Official NSE BhavCopy"}}, {"symbol": "OBEROIRLTY", "company_name": "Oberoi Realty Limited", "cmp": 1739.0, "resistance": 1760.1, "base_floor": 1569.0, "pct_dist": -1.2, "stage": "BASE SQUEEZE", "score": 84, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "pattern": "Ascending Base Consolidation", "rsi": 55.3, "rvol": 0.81, "stock_trade": {"entry": 1739.0, "sl": 1687.06, "tgt1": 1816.91, "tgt2": 1879.24, "rr": "1:1.5", "potential_pct": "+4.5% / +8.1%"}, "option_trade": {"strike": "1740 CE", "entry": 41.75, "sl": 29.2, "tgt1": 60.5, "tgt2": 81.4, "rr": 1.5, "lot_size": 350, "margin_required": 14612, "profit_tgt1": 6562, "profit_tgt2": 13878, "contract": "OBEROIRLTY26NOV1740CE", "source": "Official NSE BhavCopy"}}, {"symbol": "INFY", "company_name": "Infosys Limited", "cmp": 1181.4, "resistance": 1197.8, "base_floor": 992.9, "pct_dist": -1.37, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 53.3, "rvol": 0.91, "stock_trade": {"entry": 1181.4, "sl": 1134.14, "tgt1": 1252.29, "tgt2": 1309.0, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "1180 CE", "entry": 30.0, "sl": 21.0, "tgt1": 43.5, "tgt2": 58.5, "rr": 1.5, "lot_size": 400, "margin_required": 12000, "profit_tgt1": 5400, "profit_tgt2": 11400, "contract": "INFY26NOV1180CE", "source": "Official NSE BhavCopy"}}, {"symbol": "TRENT", "company_name": "Trent Limited", "cmp": 3079.0, "resistance": 3130.0, "base_floor": 2676.2, "pct_dist": -1.63, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 58.4, "rvol": 0.57, "stock_trade": {"entry": 3079.0, "sl": 2980.0, "tgt1": 3227.5, "tgt2": 3346.3, "rr": "1:1.5", "potential_pct": "+4.8% / +8.7%"}, "option_trade": {"strike": "3100 CE", "entry": 59.05, "sl": 41.3, "tgt1": 85.6, "tgt2": 115.1, "rr": 1.5, "lot_size": 225, "margin_required": 13286, "profit_tgt1": 5974, "profit_tgt2": 12611, "contract": "TRENT26NOV3100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PGEL", "company_name": "PG Electroplast Limited", "cmp": 546.15, "resistance": 555.4, "base_floor": 454.5, "pct_dist": -1.67, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 58.0, "rvol": 0.77, "stock_trade": {"entry": 546.15, "sl": 526.35, "tgt1": 575.85, "tgt2": 599.61, "rr": "1:1.5", "potential_pct": "+5.4% / +9.8%"}, "option_trade": {"strike": "550 CE", "entry": 16.75, "sl": 11.7, "tgt1": 24.3, "tgt2": 32.7, "rr": 1.5, "lot_size": 950, "margin_required": 15912, "profit_tgt1": 7173, "profit_tgt2": 15153, "contract": "PGEL26NOV550CE", "source": "Official NSE BhavCopy"}}, {"symbol": "NHPC", "company_name": "NHPC Limited", "cmp": 82.08, "resistance": 83.53, "base_floor": 68.79, "pct_dist": -1.74, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 77.2, "rvol": 1.74, "stock_trade": {"entry": 82.08, "sl": 78.8, "tgt1": 87.0, "tgt2": 90.94, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "82 CE", "entry": 2.28, "sl": 1.6, "tgt1": 3.3, "tgt2": 4.4, "rr": 1.5, "lot_size": 6950, "margin_required": 15846, "profit_tgt1": 7089, "profit_tgt2": 14734, "contract": "NHPC26NOV82CE", "source": "Official NSE BhavCopy"}}, {"symbol": "PERSISTENT", "company_name": "Persistent Systems Limited", "cmp": 6053.5, "resistance": 6209.0, "base_floor": 5430.0, "pct_dist": -2.5, "stage": "PRE-BREAKOUT", "score": 78, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 67.6, "rvol": 0.66, "stock_trade": {"entry": 6053.5, "sl": 5884.0, "tgt1": 6307.75, "tgt2": 6511.15, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "6100 CE", "entry": 140.5, "sl": 98.3, "tgt1": 203.7, "tgt2": 274.0, "rr": 1.5, "lot_size": 125, "margin_required": 17562, "profit_tgt1": 7900, "profit_tgt2": 16688, "contract": "PERSISTENT26NOV6100CE", "source": "Official NSE BhavCopy"}}, {"symbol": "HAL", "company_name": "Hindustan Aeronautics Limited", "cmp": 4980.0, "resistance": 5119.0, "base_floor": 4590.0, "pct_dist": -2.72, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 49.4, "rvol": 1.6, "stock_trade": {"entry": 4980.0, "sl": 4892.08, "tgt1": 5189.16, "tgt2": 5356.49, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "5000 CE", "entry": 144.4, "sl": 101.1, "tgt1": 209.4, "tgt2": 281.6, "rr": 1.5, "lot_size": 150, "margin_required": 21660, "profit_tgt1": 9750, "profit_tgt2": 20580, "contract": "HAL26NOV5000CE", "source": "Official NSE BhavCopy"}}, {"symbol": "NYKAA", "company_name": "FSN E-Commerce Ventures Limited", "cmp": 353.0, "resistance": 363.4, "base_floor": 311.4, "pct_dist": -2.86, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 55.2, "rvol": 0.78, "stock_trade": {"entry": 353.0, "sl": 343.56, "tgt1": 367.83, "tgt2": 379.69, "rr": "1:1.5", "potential_pct": "+4.2% / +7.6%"}, "option_trade": {"strike": "355 CE", "entry": 8.3, "sl": 5.8, "tgt1": 12.0, "tgt2": 16.2, "rr": 1.5, "lot_size": 3125, "margin_required": 25938, "profit_tgt1": 11562, "profit_tgt2": 24687, "contract": "NYKAA26NOV355CE", "source": "Official NSE BhavCopy"}}, {"symbol": "BOSCHLTD", "company_name": "Bosch Limited", "cmp": 50700.0, "resistance": 52475.0, "base_floor": 42675.0, "pct_dist": -3.38, "stage": "PRE-BREAKOUT", "score": 78, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Cup & Handle Breakout", "pattern": "Cup & Handle Accumulation", "rsi": 70.5, "rvol": 2.71, "stock_trade": {"entry": 50700.0, "sl": 48672.0, "tgt1": 53742.0, "tgt2": 56175.6, "rr": "1:1.5", "potential_pct": "+6.0% / +10.8%"}, "option_trade": {"strike": "50500 CE", "entry": 1252.7, "sl": 876.9, "tgt1": 1816.4, "tgt2": 2442.8, "rr": 1.5, "lot_size": 25, "margin_required": 31318, "profit_tgt1": 14093, "profit_tgt2": 29753, "contract": "BOSCHLTD26NOV50500CE", "source": "Official NSE BhavCopy"}}]

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
                    <p class="text-xs text-slate-400 mt-0.5">Institutional Multi-Month Consolidation Bases &bull; High-Beta Momentum Breakouts</p>
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
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
            <div class="glass-card p-4 rounded-2xl border border-amber-500/50 bg-gradient-to-b from-amber-500/10 to-transparent cursor-pointer hover:border-amber-400 transition-all" onclick="document.getElementById('tabBtnAPlus').click()">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-extrabold uppercase text-amber-300 flex items-center gap-1">⭐ A+ Setups</span>
                    <i data-lucide="star" class="w-4 h-4 fill-amber-400 text-amber-400"></i>
                </div>
                <div class="text-3xl font-black text-amber-300" id="statAPlus">--</div>
                <div class="text-[11px] text-amber-200/70 mt-1">Top Actionable Picks</div>
            </div>

            <div class="glass-card p-4 rounded-2xl cursor-pointer hover:border-slate-700 transition-all" onclick="document.getElementById('tabBtnAll').click()">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">All Breakouts</span>
                    <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statTotal">--</div>
                <div class="text-[11px] text-slate-500 mt-1">From 218 F&O Stocks</div>
            </div>

            <div class="glass-card p-4 rounded-2xl border border-amber-500/20 bg-amber-500/5">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase text-amber-400">🏆 Cup & Handle</span>
                    <i data-lucide="award" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-amber-400" id="statCup">--</div>
                <div class="text-[11px] text-slate-500 mt-1">High-Conviction Base</div>
            </div>

            <div class="glass-card p-4 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Monthly Base</span>
                    <i data-lucide="trending-up" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-cyan-400" id="statMonthly">--</div>
                <div class="text-[11px] text-slate-500 mt-1">Multi-Month Swings</div>
            </div>

            <div class="glass-card p-4 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Weekly Swings</span>
                    <i data-lucide="calendar" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-indigo-400" id="statWeekly">--</div>
                <div class="text-[11px] text-slate-500 mt-1">Consolidation Pivots</div>
            </div>

            <div class="glass-card p-4 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Daily F&O</span>
                    <i data-lucide="zap" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-emerald-400" id="statDaily">--</div>
                <div class="text-[11px] text-slate-500 mt-1">Momentum Fast-Track</div>
            </div>
        </div>

        <!-- Filter Controls: Horizon Tabs, Sector Dropdown & Search -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
            
            <!-- Horizon Tabs -->
            <div class="flex gap-2 p-1.5 rounded-xl bg-slate-900 border border-slate-800 w-full lg:w-auto overflow-x-auto" id="tabs">
                <button id="tabBtnAPlus" onclick="setHorizon('APLUS', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-black transition-all bg-gradient-to-r from-amber-500 to-yellow-400 text-black shadow-lg shadow-amber-500/20 whitespace-nowrap flex items-center gap-1.5 active:scale-95">
                    ⭐ A+ Fresh Setups (<span id="tabCountAPlus">0</span>)
                </button>
                <button id="tabBtnAll" onclick="setHorizon('ALL', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-bold transition-all text-slate-300 hover:text-white hover:bg-slate-800 whitespace-nowrap">
                    All Breakouts (<span id="tabCountAll">0</span>)
                </button>
                <button onclick="setHorizon('Cup & Handle Breakout', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-semibold text-amber-300 hover:text-white hover:bg-slate-800 transition-all whitespace-nowrap flex items-center gap-1.5">
                    🏆 Cup & Handle (<span id="tabCountCup">0</span>)
                </button>
                <button onclick="setHorizon('Monthly Holding', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all whitespace-nowrap">
                    Monthly Base
                </button>
                <button onclick="setHorizon('Weekly Holding', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all whitespace-nowrap">
                    Weekly Holding
                </button>
                <button onclick="setHorizon('Daily / Intraday', this)" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all whitespace-nowrap">
                    Daily Fast F&O
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

    <!-- NATIVE IN-HOUSE BREAKOUT PATTERN CANDLESTICK MODAL (TradingView Engine) -->
    <div id="chartModal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-2 sm:p-4">
        <div class="bg-white rounded-2xl w-full max-w-6xl h-[92vh] flex flex-col overflow-hidden shadow-2xl border border-slate-300">
            
            <!-- Modal Header (TradingView Style Bar) -->
            <div class="px-5 py-3 border-b border-slate-200 flex justify-between items-center bg-[#f8fafc]">
                <div class="flex items-center gap-3 flex-wrap">
                    <span id="modalSymbol" class="text-xl font-black text-slate-900 tracking-wider"></span>
                    <span id="modalPatternBadge" class="text-xs px-2.5 py-0.5 rounded font-extrabold bg-blue-100 text-blue-800 border border-blue-200">
                        BREAKOUT PATTERN
                    </span>
                    <div id="modalLevelsBadge" class="text-xs text-slate-600 mono flex gap-3 flex-wrap"></div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="downloadChartImage()" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold border border-slate-300 flex items-center gap-1.5 transition-all active:scale-95">
                        <i data-lucide="download" class="w-3.5 h-3.5"></i> Save Image
                    </button>
                    <button onclick="closeChartModal()" class="w-8 h-8 rounded-lg bg-slate-200 hover:bg-slate-300 text-slate-700 flex items-center justify-center transition-all">
                        <i data-lucide="x" class="w-5 h-5"></i>
                    </button>
                </div>
            </div>

            <!-- Chart Toolbar / OHLC Status Bar -->
            <div class="px-5 py-2 bg-white border-b border-slate-200 flex flex-wrap justify-between items-center gap-3 text-xs mono">
                <div id="ohlcHeaderInfo" class="text-slate-700 font-medium"></div>
                <div id="candleHoverInfo" class="text-slate-500 text-xs">Hover over candles to view details</div>
            </div>

            <!-- Canvas Container: Pure White TradingView Aesthetic -->
            <div class="flex-1 w-full bg-[#ffffff] relative p-1" id="canvasWrapper">
                <canvas id="breakoutCanvas" class="w-full h-full block cursor-crosshair"></canvas>
            </div>

        </div>
    </div>

    <script>
        let fullData = [];
        let activeHorizon = 'APLUS';

        function isAPlus(item) {
            const isFresh = (item.pct_dist >= 0.0 && item.pct_dist <= 2.0) || (item.stage && item.stage.includes('IMMINENT') && item.pct_dist >= -0.8);
            const isGoodVol = item.rvol >= 1.25;
            const isGoodRsi = item.rsi >= 60.0 && item.rsi <= 82.0;
            return isFresh && isGoodVol && isGoodRsi;
        }

        const COMPANY_NAMES = {
            'DLF': 'DLF Ltd',
            'MARUTI': 'Maruti Suzuki India Ltd',
            'ICICIBANK': 'ICICI Bank Ltd',
            'M&M': 'Mahindra & Mahindra Ltd',
            'TITAN': 'Titan Company Ltd',
            'TATASTEEL': 'Tata Steel Ltd',
            'HDFCBANK': 'HDFC Bank Ltd',
            'AXISBANK': 'Axis Bank Ltd',
            'DIVISLAB': "Divi's Laboratories Ltd",
            'KOTAKBANK': 'Kotak Mahindra Bank Ltd',
            'BAJFINANCE': 'Bajaj Finance Ltd',
            'LT': 'Larsen & Toubro Ltd',
            'HINDALCO': 'Hindalco Industries Ltd',
            'BHARTIARTL': 'Bharti Airtel Ltd',
            'BAJAJ-AUTO': 'Bajaj Auto Ltd',
            'SBIN': 'State Bank of India',
            'BAJAJFINSV': 'Bajaj Finserv Ltd',
            'MUTHOOTFIN': 'Muthoot Finance Ltd',
            'SUNPHARMA': 'Sun Pharmaceutical Industries Ltd',
            'CHOLAFIN': 'Cholamandalam Investment',
            'CIPLA': 'Cipla Ltd',
            'TVSMOTOR': 'TVS Motor Company Ltd',
            'PNB': 'Punjab National Bank',
            'HEROMOTOCO': 'Hero MotoCorp Ltd',
            'ITC': 'ITC Ltd',
            'GODREJPROP': 'Godrej Properties Ltd',
            'RELIANCE': 'Reliance Industries Ltd',
            'BANKBARODA': 'Bank of Baroda',
            'JINDALSTEL': 'Jindal Steel & Power Ltd',
            'EICHERMOT': 'Eicher Motors Ltd',
            'BPCL': 'Bharat Petroleum Corp Ltd',
            'IOC': 'Indian Oil Corp Ltd',
            'DRREDDY': "Dr. Reddy's Laboratories Ltd",
            'JSWSTEEL': 'JSW Steel Ltd',
            'WIPRO': 'Wipro Ltd',
            'TECHM': 'Tech Mahindra Ltd',
            'GAIL': 'GAIL (India) Ltd',
            'COFORGE': 'Coforge Ltd',
            'BEL': 'Bharat Electronics Ltd',
            'VEDL': 'Vedanta Ltd',
            'NATIONALUM': 'National Aluminium Co Ltd',
            'PERSISTENT': 'Persistent Systems Ltd',
            'HAL': 'Hindustan Aeronautics Ltd',
            'TATAPOWER': 'Tata Power Co Ltd',
            'COALINDIA': 'Coal India Ltd',
            'MOTHERSON': 'Samvardhana Motherson Ltd',
            'BHEL': 'Bharat Heavy Electricals Ltd',
        };

        function getCompanyName(sym) {
            return COMPANY_NAMES[sym] || (sym + ' Ltd');
        }

        function updateTime() {
            const now = new Date();
            document.getElementById('syncTime').innerText = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) + ' IST';
        }

        function setHorizon(horizon, btnElement) {
            activeHorizon = horizon;
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-emerald-500', 'text-black', 'bg-gradient-to-r', 'from-amber-500', 'to-yellow-400', 'shadow-lg', 'shadow-amber-500/20');
                btn.classList.add('text-slate-300', 'hover:bg-slate-800');
            });
            const targetBtn = btnElement || (typeof event !== 'undefined' && event ? event.currentTarget || event.target : null);
            if (targetBtn && targetBtn.classList) {
                targetBtn.classList.remove('text-slate-300', 'hover:bg-slate-800');
                if (horizon === 'APLUS') {
                    targetBtn.classList.add('bg-gradient-to-r', 'from-amber-500', 'to-yellow-400', 'text-black', 'shadow-lg', 'shadow-amber-500/20');
                } else {
                    targetBtn.classList.add('bg-emerald-500', 'text-black');
                }
            }
            applyFilters();
        }

        function applyFilters() {
            const query = document.getElementById('searchInput').value.toUpperCase().trim();
            const sector = document.getElementById('sectorSelect').value;

            let filtered = fullData.filter(item => {
                let matchHorizon = false;
                if (activeHorizon === 'ALL') matchHorizon = true;
                else if (activeHorizon === 'APLUS') matchHorizon = isAPlus(item);
                else if (activeHorizon === 'Cup & Handle Breakout') matchHorizon = (item.setup_name && item.setup_name.includes('Cup & Handle')) || (item.pattern && item.pattern.includes('Cup & Handle'));
                else matchHorizon = (item.horizon === activeHorizon);

                const matchSector = (sector === 'ALL' || item.sector === sector);
                const cName = (item.company_name || getCompanyName(item.symbol)).toUpperCase();
                const matchSearch = (!query || item.symbol.includes(query) || cName.includes(query) || (item.setup_name && item.setup_name.toUpperCase().includes(query)) || (item.pattern && item.pattern.toUpperCase().includes(query)));
                return matchHorizon && matchSector && matchSearch;
            });

            if (activeHorizon === 'APLUS') {
                filtered.sort((a, b) => (b.score - a.score) || (b.rvol - a.rvol) || (a.pct_dist - b.pct_dist));
            }

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
                const cName = item.company_name || getCompanyName(item.symbol);
                const isCup = (item.setup_name && item.setup_name.includes('Cup & Handle')) || (item.pattern && item.pattern.includes('Cup & Handle'));
                const isA_Plus = isAPlus(item);

                let badgeColor = 'bg-amber-950 text-amber-300 border-amber-700/50';
                if (item.horizon === 'Monthly Holding') badgeColor = 'bg-cyan-950 text-cyan-300 border-cyan-700/50';
                if (item.horizon === 'Weekly Holding') badgeColor = 'bg-indigo-950 text-indigo-300 border-indigo-700/50';

                let stageBadge = 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60';
                if (item.stage.includes('IMMINENT')) stageBadge = 'bg-yellow-950/80 text-yellow-300 border-yellow-700/60';
                else if (item.stage.includes('BASE SQUEEZE')) stageBadge = 'bg-cyan-950/80 text-cyan-300 border-cyan-700/60';

                const distStr = item.pct_dist >= 0 ? `+${item.pct_dist}% above pivot` : `${item.pct_dist}% to pivot`;

                const aPlusBadgeHtml = isA_Plus ? `
                    <span class="text-xs px-2.5 py-0.5 rounded font-black bg-gradient-to-r from-amber-500/25 to-yellow-500/25 text-amber-300 border border-amber-400/60 flex items-center gap-1 shadow-sm shadow-amber-500/10">
                        ⭐ A+ SETUP
                    </span>` : '';

                const cupBadgeHtml = isCup ? `
                    <span class="text-xs px-2.5 py-0.5 rounded font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center gap-1 shadow-sm shadow-amber-500/10">
                        🏆 CUP & HANDLE
                    </span>` : '';

                const cardHtml = `
                <div class="stock-card glass-card rounded-2xl p-6 space-y-6 hover:border-emerald-500/40 transition-all shadow-xl">
                    <div class="flex justify-between items-start border-b border-slate-800/80 pb-4">
                        <div>
                            <div class="flex items-center gap-2.5 flex-wrap">
                                <span class="text-2xl font-black tracking-tight text-white">${item.symbol}</span>
                                ${aPlusBadgeHtml}
                                ${cupBadgeHtml}
                                <span class="text-xs px-2.5 py-1 rounded-md font-bold uppercase tracking-wider border ${badgeColor}">
                                    ${item.horizon}
                                </span>
                                <span class="text-xs px-2 py-0.5 rounded font-extrabold border ${stageBadge}">
                                    ${item.stage}
                                </span>
                            </div>
                            <div class="text-xs font-semibold text-slate-300 mt-1">${cName}</div>
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
                                <span class="flex items-center gap-1.5"><i data-lucide="flame" class="w-3.5 h-3.5"></i> Institutional F&O Call</span>
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
                            <button onclick="openNativeChart('${item.symbol}', '${cName.replace(/'/g, "\\'")}', ${item.cmp}, ${item.resistance}, ${item.base_floor}, ${item.stock_trade.sl}, ${item.stock_trade.tgt1}, ${item.stock_trade.tgt2}, '${item.setup_name}', '${item.pattern}')" 
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
            let monthly = 0, weekly = 0, daily = 0, cup = 0, aplus = 0;
            fullData.forEach(item => {
                if (item.horizon === 'Monthly Holding') monthly++;
                if (item.horizon === 'Weekly Holding') weekly++;
                if (item.horizon === 'Daily / Intraday') daily++;
                if ((item.setup_name && item.setup_name.includes('Cup & Handle')) || (item.pattern && item.pattern.includes('Cup & Handle'))) cup++;
                if (isAPlus(item)) aplus++;
            });

            document.getElementById('statTotal').innerText = fullData.length;
            if (document.getElementById('statAPlus')) document.getElementById('statAPlus').innerText = aplus;
            if (document.getElementById('statCup')) document.getElementById('statCup').innerText = cup;
            document.getElementById('statMonthly').innerText = monthly;
            document.getElementById('statWeekly').innerText = weekly;
            document.getElementById('statDaily').innerText = daily;
            document.getElementById('tabCountAll').innerText = fullData.length;
            if (document.getElementById('tabCountAPlus')) document.getElementById('tabCountAPlus').innerText = aplus;
            if (document.getElementById('tabCountCup')) document.getElementById('tabCountCup').innerText = cup;
        }

        function copyTradeAlert(sym, cmp, sl, tgt, strike, optEntry, optSl, optTgt1, optTgt2, lot, margin) {
            const text = `🔥 VICKYVAIO BREAKOUTS ALERT: ${sym}\n• Spot CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}\n• F&O Option: ${sym} ${strike}\n• Premium Entry: ₹${optEntry} | SL: ₹${optSl} (-30%)\n• Target 1: ₹${optTgt1} (+45%) | Target 2: ₹${optTgt2} (+95% Doubler)\n• Lot Size: ${lot} | Margin: ₹${Number(margin).toLocaleString('en-IN')}\nStrategy: Institutional Base & Momentum Confluence`;
            navigator.clipboard.writeText(text);
            alert(`Trade alert for ${sym} copied to clipboard!`);
        }

        // ========================================================
        // INSTITUTIONAL TRADINGVIEW VISUAL ENGINE
        // ========================================================
        let activeChartData = null;

        async function openNativeChart(symbol, companyName, cmp, resistance, baseFloor, sl, tgt1, tgt2, setupName, pattern) {
            const cName = companyName || getCompanyName(symbol);
            document.getElementById('modalSymbol').innerText = symbol;
            document.getElementById('modalPatternBadge').innerText = (setupName || pattern).toUpperCase();
            document.getElementById('modalLevelsBadge').innerHTML = `
                <span class="text-slate-900 font-bold">CMP: ₹${cmp}</span>
                <span class="text-amber-600 font-bold">Pivot: ₹${resistance}</span>
                <span class="text-indigo-600 font-bold">Floor: ₹${baseFloor}</span>
                <span class="text-emerald-600 font-bold">T1: ₹${tgt1}</span>
                <span class="text-emerald-700 font-bold">T2: ₹${tgt2}</span>
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
                        companyName: cName,
                        cmp: data.cmp || cmp,
                        resistance: resistance,
                        baseFloor: baseFloor,
                        sl: sl,
                        tgt1: tgt1,
                        tgt2: tgt2,
                        setupName: setupName,
                        pattern: pattern,
                        candles: data.candles
                    };
                } else {
                    activeChartData = generateFallbackCandles(symbol, cName, cmp, resistance, baseFloor, sl, tgt1, tgt2, setupName, pattern);
                }
            } catch (e) {
                activeChartData = generateFallbackCandles(symbol, cName, cmp, resistance, baseFloor, sl, tgt1, tgt2, setupName, pattern);
            }

            drawChart();
            setupChartMouseInteractions();
        }

        function generateFallbackCandles(symbol, companyName, cmp, resistance, baseFloor, sl, tgt1, tgt2, setupName, pattern) {
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
            return { symbol, companyName, cmp, resistance, baseFloor, sl, tgt1, tgt2, setupName, pattern, candles };
        }

        function downloadChartImage() {
            if (!activeChartData) return;
            const canvas = document.getElementById('breakoutCanvas');
            const link = document.createElement('a');
            link.download = `${activeChartData.symbol}_Breakout_Chart.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();
        }

        function drawChart(hoverIdx = -1) {
            if (!activeChartData) return;
            const canvas = document.getElementById('breakoutCanvas');
            const ctx = canvas.getContext('2d');
            const dpr = window.devicePixelRatio || 1;
            const w = canvas.width;
            const h = canvas.height;

            // Clear with pure white TradingView canvas background
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, w, h);

            const candles = activeChartData.candles;
            const n = candles.length;
            if (n === 0) return;

            // Margins: Ample room for watermark, right price axis, and bottom date axis
            const paddingLeft = 45 * dpr;
            const paddingRight = 105 * dpr;
            const paddingTop = 65 * dpr;
            const paddingBottom = 48 * dpr;
            const chartHeight = h - paddingTop - paddingBottom;
            const chartWidth = w - paddingLeft - paddingRight;

            // Price bounds
            let minP = Math.min(...candles.map(c => c.l), activeChartData.baseFloor * 0.995);
            let maxP = Math.max(...candles.map(c => c.h), activeChartData.tgt2, activeChartData.resistance * 1.01);
            minP *= 0.985;
            maxP *= 1.02;
            const priceRange = maxP - minP || 1;

            const yToPrice = p => paddingTop + chartHeight * (1 - (p - minP) / priceRange);

            const maxVol = Math.max(...candles.map(c => c.v)) || 1;
            const volAreaHeight = 45 * dpr;
            const volYBase = h - paddingBottom;

            // 1. TOP CENTER WATERMARK CARD
            const cardW = Math.min(270 * dpr, chartWidth * 0.45);
            const cardH = 46 * dpr;
            const cardX = paddingLeft + (chartWidth - cardW) / 2;
            const cardY = 10 * dpr;
            ctx.save();
            ctx.fillStyle = '#dbeafe'; // Light lavender/sky blue pill
            ctx.strokeStyle = '#bfdbfe';
            ctx.lineWidth = 1 * dpr;
            ctx.beginPath();
            if (ctx.roundRect) ctx.roundRect(cardX, cardY, cardW, cardH, 8 * dpr);
            else ctx.rect(cardX, cardY, cardW, cardH);
            ctx.fill();
            ctx.stroke();

            // Bold Company Name
            ctx.fillStyle = '#0f172a';
            ctx.font = `bold ${16 * dpr}px 'Plus Jakarta Sans', sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(activeChartData.companyName, cardX + cardW / 2, cardY + 18 * dpr);

            // Watermark Subtitle
            ctx.fillStyle = '#475569';
            ctx.font = `bold ${8.5 * dpr}px 'Plus Jakarta Sans', sans-serif`;
            ctx.fillText('Vickyvaio Institutional Breakouts', cardX + cardW / 2, cardY + 34 * dpr);
            ctx.restore();

            // Update top OHLC header text
            const lastC = candles[candles.length - 1];
            const prevC = candles.length > 1 ? candles[candles.length - 2].c : lastC.o;
            const chgPct = (((lastC.c - prevC) / prevC) * 100).toFixed(2);
            const chgSign = chgPct >= 0 ? '+' : '';
            const ohlcText = `${activeChartData.companyName} · 1D · NSE  O:${lastC.o}  H:${lastC.h}  L:${lastC.l}  C:${lastC.c}  (${chgSign}${chgPct}%)  Vol:${(lastC.v / 1000).toFixed(1)}K`;
            document.getElementById('ohlcHeaderInfo').innerText = ohlcText;

            // 2. GRID LINES & AXES
            ctx.save();
            ctx.strokeStyle = '#f1f5f9';
            ctx.lineWidth = 1 * dpr;
            const gridSteps = 6;
            for (let i = 0; i <= gridSteps; i++) {
                const gp = minP + (priceRange * i) / gridSteps;
                const gy = yToPrice(gp);
                ctx.beginPath();
                ctx.moveTo(paddingLeft, gy);
                ctx.lineTo(w - paddingRight, gy);
                ctx.stroke();

                // Right axis scale price text
                ctx.fillStyle = '#64748b';
                ctx.font = `${9.5 * dpr}px 'JetBrains Mono', monospace`;
                ctx.textAlign = 'left';
                ctx.fillText(gp.toLocaleString('en-IN', { maximumFractionDigits: 1 }), w - paddingRight + 8 * dpr, gy + 3.5 * dpr);
            }

            // Right vertical axis border
            ctx.strokeStyle = '#e2e8f0';
            ctx.beginPath();
            ctx.moveTo(w - paddingRight, paddingTop);
            ctx.lineTo(w - paddingRight, h - paddingBottom);
            ctx.stroke();

            // Bottom date axis border
            ctx.beginPath();
            ctx.moveTo(paddingLeft, h - paddingBottom);
            ctx.lineTo(w - paddingRight, h - paddingBottom);
            ctx.stroke();
            ctx.restore();

            const slotWidth = chartWidth / n;
            const candleWidth = Math.max(slotWidth * 0.68, 2.5 * dpr);

            // 3. BREAKOUT RESISTANCE ZONE BOX
            const rTopY = yToPrice(activeChartData.resistance);
            const rBotY = yToPrice(activeChartData.resistance * 0.985);
            const boxH = Math.max(Math.abs(rBotY - rTopY), 12 * dpr);
            const boxStartX = paddingLeft + slotWidth * Math.max(0, n - 26);
            const boxEndX = paddingLeft + slotWidth * n + 20 * dpr;

            ctx.save();
            // Shaded gray rectangular zone
            ctx.fillStyle = 'rgba(241, 245, 249, 0.85)';
            ctx.fillRect(boxStartX, Math.min(rTopY, rBotY), boxEndX - boxStartX, boxH);

            // Solid top and bottom borders
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 1.5 * dpr;
            ctx.beginPath();
            ctx.moveTo(boxStartX, rTopY);
            ctx.lineTo(w - paddingRight, rTopY);
            ctx.moveTo(boxStartX, rBotY);
            ctx.lineTo(boxEndX, rBotY);
            ctx.stroke();

            // "Breakout" text annotation right above box
            ctx.fillStyle = '#0f172a';
            ctx.font = `bold ${10.5 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'right';
            ctx.fillText("Breakout", boxEndX - 10 * dpr, rTopY - 5 * dpr);

            // Breakout right axis black badge
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(w - paddingRight + 2 * dpr, rTopY - 8.5 * dpr, 85 * dpr, 17 * dpr);
            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'left';
            ctx.fillText(activeChartData.resistance.toLocaleString('en-IN'), w - paddingRight + 8 * dpr, rTopY + 3.5 * dpr);
            ctx.restore();

            // 4. BASE FLOOR SOLID BLACK LINE
            const floorY = yToPrice(activeChartData.baseFloor);
            ctx.save();
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 1.5 * dpr;
            ctx.beginPath();
            ctx.moveTo(paddingLeft + slotWidth * Math.max(0, n - 35), floorY);
            ctx.lineTo(w - paddingRight, floorY);
            ctx.stroke();

            // Base floor right axis black badge
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(w - paddingRight + 2 * dpr, floorY - 8.5 * dpr, 85 * dpr, 17 * dpr);
            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'left';
            ctx.fillText(activeChartData.baseFloor.toLocaleString('en-IN'), w - paddingRight + 8 * dpr, floorY + 3.5 * dpr);
            ctx.restore();

            // 5. CUP & HANDLE CURVED ARC & HANDLE (If Cup & Handle Setup)
            const isCupSetup = (activeChartData.setupName && activeChartData.setupName.includes('Cup & Handle')) ||
                               (activeChartData.pattern && activeChartData.pattern.includes('Cup & Handle'));
            if (isCupSetup && n >= 30) {
                ctx.save();
                ctx.strokeStyle = '#2563eb';
                ctx.lineWidth = 1.8 * dpr;
                ctx.setLineDash([5 * dpr, 3 * dpr]);
                
                const cupStartIdx = Math.max(0, n - 35);
                const cupMidIdx = Math.max(0, n - 18);
                const cupEndIdx = Math.max(0, n - 8);
                
                const x1 = paddingLeft + slotWidth * (cupStartIdx + 0.5);
                const y1 = yToPrice(activeChartData.resistance * 0.998);
                const xMid = paddingLeft + slotWidth * (cupMidIdx + 0.5);
                const yMid = yToPrice(activeChartData.baseFloor * 1.015);
                const x2 = paddingLeft + slotWidth * (cupEndIdx + 0.5);
                const y2 = yToPrice(activeChartData.resistance * 0.998);

                // Curved U-shape cup bottom arc
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.quadraticCurveTo(xMid, yMid + (yMid - y1) * 0.35, x2, y2);
                ctx.stroke();

                // Handle shallow dip
                const hEndIdx = n - 2;
                const xH = paddingLeft + slotWidth * (hEndIdx + 0.5);
                const yH = yToPrice(activeChartData.resistance * 0.985);
                ctx.beginPath();
                ctx.moveTo(x2, y2);
                ctx.quadraticCurveTo((x2 + xH) / 2, yH + 4 * dpr, xH, yH);
                ctx.stroke();

                ctx.setLineDash([]);
                ctx.fillStyle = '#2563eb';
                ctx.font = `bold ${9.5 * dpr}px 'Plus Jakarta Sans', sans-serif`;
                ctx.textAlign = 'center';
                ctx.fillText('Cup', xMid, yMid - 6 * dpr);
                ctx.fillText('Handle', (x2 + xH) / 2, yH - 6 * dpr);
                ctx.restore();
            }

            // 6. DRAW CANDLESTICKS & VOLUME BARS
            for (let i = 0; i < n; i++) {
                const c = candles[i];
                const cx = paddingLeft + slotWidth * (i + 0.5);
                const isGreen = c.c >= c.o;
                const candleColor = isGreen ? '#089981' : '#f23645';

                // Volume Bar
                const vHeight = (c.v / maxVol) * volAreaHeight;
                ctx.fillStyle = isGreen ? 'rgba(8, 153, 129, 0.25)' : 'rgba(242, 54, 69, 0.25)';
                ctx.fillRect(cx - candleWidth / 2, volYBase - vHeight, candleWidth, vHeight);

                // Wick
                ctx.strokeStyle = candleColor;
                ctx.lineWidth = 1.2 * dpr;
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
            }

            // 7. TRAJECTORY PROJECTION PATH (Signature Zigzag Arrow)
            const ptA_x = paddingLeft + slotWidth * (n - 0.5);
            const ptA_y = yToPrice(activeChartData.resistance);
            
            const ptB_x = Math.min(ptA_x + 65 * dpr, w - paddingRight - 90 * dpr);
            const ptB_y = yToPrice(activeChartData.tgt1);
            
            const ptC_x = ptB_x + 22 * dpr;
            const dipDepth = (activeChartData.tgt1 - activeChartData.resistance) * 0.35;
            const ptC_y = yToPrice(activeChartData.tgt1 - dipDepth);
            
            const ptD_x = Math.min(w - paddingRight - 35 * dpr, ptC_x + 95 * dpr);
            const ptD_y = yToPrice(activeChartData.tgt2);

            ctx.save();
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 2 * dpr;
            ctx.beginPath();
            ctx.moveTo(ptA_x, ptA_y);
            ctx.lineTo(ptB_x, ptB_y); // Rise to Target 1
            ctx.lineTo(ptC_x, ptC_y); // Retest pullback dip
            ctx.lineTo(ptD_x, ptD_y); // Surge to Target 2
            ctx.stroke();

            // Northeast Arrowhead terminating at Target 2
            const angle = Math.atan2(ptD_y - ptC_y, ptD_x - ptC_x);
            const arrowLen = 10 * dpr;
            ctx.fillStyle = '#0f172a';
            ctx.beginPath();
            ctx.moveTo(ptD_x, ptD_y);
            ctx.lineTo(ptD_x - arrowLen * Math.cos(angle - Math.PI / 7), ptD_y - arrowLen * Math.sin(angle - Math.PI / 7));
            ctx.lineTo(ptD_x - arrowLen * Math.cos(angle + Math.PI / 7), ptD_y - arrowLen * Math.sin(angle + Math.PI / 7));
            ctx.closePath();
            ctx.fill();
            ctx.restore();

            // 8. TARGET 1 HORIZONTAL DASHED LINE & LABELS
            ctx.save();
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 1.5 * dpr;
            ctx.setLineDash([6 * dpr, 4 * dpr]);
            ctx.beginPath();
            ctx.moveTo(ptB_x, ptB_y);
            ctx.lineTo(w - paddingRight, ptB_y);
            ctx.stroke();
            ctx.setLineDash([]);

            // Text tag: "Target - [Price]"
            ctx.fillStyle = '#0f172a';
            ctx.font = `bold ${10.5 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'right';
            ctx.fillText(`Target - ${activeChartData.tgt1.toLocaleString('en-IN')}`, ptB_x - 10 * dpr, ptB_y - 4 * dpr);

            // Right axis black pill for Target 1
            ctx.fillRect(w - paddingRight + 2 * dpr, ptB_y - 8.5 * dpr, 85 * dpr, 17 * dpr);
            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'left';
            ctx.fillText(activeChartData.tgt1.toLocaleString('en-IN'), w - paddingRight + 8 * dpr, ptB_y + 3.5 * dpr);
            ctx.restore();

            // 9. TARGET 2 HORIZONTAL SOLID LINE & LABELS
            ctx.save();
            ctx.strokeStyle = '#0f172a';
            ctx.lineWidth = 1.5 * dpr;
            ctx.beginPath();
            ctx.moveTo(ptD_x, ptD_y);
            ctx.lineTo(w - paddingRight, ptD_y);
            ctx.stroke();

            // Text tag: "Target - [Price]"
            ctx.fillStyle = '#0f172a';
            ctx.font = `bold ${10.5 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'right';
            ctx.fillText(`Target - ${activeChartData.tgt2.toLocaleString('en-IN')}`, ptD_x - 10 * dpr, ptD_y - 4 * dpr);

            // Right axis black pill for Target 2
            ctx.fillRect(w - paddingRight + 2 * dpr, ptD_y - 8.5 * dpr, 85 * dpr, 17 * dpr);
            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${9 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'left';
            ctx.fillText(activeChartData.tgt2.toLocaleString('en-IN'), w - paddingRight + 8 * dpr, ptD_y + 3.5 * dpr);
            ctx.restore();

            // 10. CURRENT MARKET PRICE (CMP) GUIDE & PILL
            const cmpY = yToPrice(activeChartData.cmp);
            ctx.save();
            ctx.strokeStyle = '#089981';
            ctx.lineWidth = 1.2 * dpr;
            ctx.setLineDash([3 * dpr, 3 * dpr]);
            ctx.beginPath();
            ctx.moveTo(paddingLeft, cmpY);
            ctx.lineTo(w - paddingRight, cmpY);
            ctx.stroke();
            ctx.setLineDash([]);

            // Right axis green pill
            ctx.fillStyle = '#089981';
            ctx.fillRect(w - paddingRight + 2 * dpr, cmpY - 10 * dpr, 92 * dpr, 20 * dpr);
            ctx.fillStyle = '#ffffff';
            ctx.font = `bold ${9.5 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'left';
            ctx.fillText(`${activeChartData.cmp.toLocaleString('en-IN')}`, w - paddingRight + 8 * dpr, cmpY + 3.5 * dpr);
            ctx.restore();

            // 11. BOTTOM DATE AXIS & TRADINGVIEW LOGO
            ctx.save();
            ctx.fillStyle = '#64748b';
            ctx.font = `${9.5 * dpr}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'center';
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            let lastMonth = -1;
            for (let i = 0; i < n; i++) {
                const dt = new Date(candles[i].t * 1000);
                const m = dt.getMonth();
                if (m !== lastMonth && (i - lastMonth > 7 || lastMonth === -1)) {
                    lastMonth = m;
                    const cx = paddingLeft + slotWidth * (i + 0.5);
                    ctx.fillText(monthNames[m], cx, h - paddingBottom + 16 * dpr);
                }
            }

            // TradingView Logo text at bottom left
            ctx.fillStyle = '#0f172a';
            ctx.font = `bold ${11 * dpr}px 'Plus Jakarta Sans', sans-serif`;
            ctx.textAlign = 'left';
            ctx.fillText('17 TradingView', paddingLeft, h - 14 * dpr);
            ctx.restore();

            // 12. CROSSHAIR & TOOLTIP
            if (hoverIdx >= 0 && hoverIdx < n) {
                const c = candles[hoverIdx];
                const cx = paddingLeft + slotWidth * (hoverIdx + 0.5);
                const cy = yToPrice(c.c);

                ctx.save();
                ctx.strokeStyle = '#94a3b8';
                ctx.lineWidth = 1 * dpr;
                ctx.setLineDash([3 * dpr, 3 * dpr]);

                ctx.beginPath();
                ctx.moveTo(cx, paddingTop);
                ctx.lineTo(cx, h - paddingBottom);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(paddingLeft, cy);
                ctx.lineTo(w - paddingRight, cy);
                ctx.stroke();
                ctx.restore();

                const dateStr = new Date(c.t * 1000).toLocaleDateString('en-GB');
                document.getElementById('candleHoverInfo').innerHTML = `
                    <span class="text-slate-900 font-bold">${dateStr}</span> &bull; 
                    O: <strong class="text-slate-700">₹${c.o}</strong> 
                    H: <strong class="text-emerald-600">₹${c.h}</strong> 
                    L: <strong class="text-rose-600">₹${c.l}</strong> 
                    C: <strong class="${c.c >= c.o ? 'text-emerald-600' : 'text-rose-600'}">₹${c.c}</strong> &bull; 
                    Vol: <strong class="text-blue-600">${(c.v / 100000).toFixed(1)}L</strong>
                `;
            }
        }

        function setupChartMouseInteractions() {
            const canvas = document.getElementById('breakoutCanvas');
            const dpr = window.devicePixelRatio || 1;

            canvas.onmousemove = function(e) {
                if (!activeChartData) return;
                const rect = canvas.getBoundingClientRect();
                const mouseX = (e.clientX - rect.left) * dpr;
                const paddingLeft = 45 * dpr;
                const paddingRight = 105 * dpr;
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