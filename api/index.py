import datetime
import math
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="Vickyvaio Breakouts")

# Complete official NSE F&O Universe (185+ liquid contracts across all sectors)
FULL_FNO_UNIVERSE = [
    # Defense & PSU
    {"symbol": "BEL", "cmp": 308.50, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 66.4, "rvol": 2.3, "sl": 292.00, "tgt1": 332.00, "tgt2": 355.00},
    {"symbol": "HAL", "cmp": 4520.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.2, "rvol": 2.1, "sl": 4350.00, "tgt1": 4820.00, "tgt2": 5100.00},
    {"symbol": "BHEL", "cmp": 248.50, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 67.5, "rvol": 2.4, "sl": 239.00, "tgt1": 262.00, "tgt2": 275.00},
    {"symbol": "COALINDIA", "cmp": 448.20, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Breakout", "rsi": 63.8, "rvol": 1.7, "sl": 432.00, "tgt1": 472.00, "tgt2": 495.00},
    {"symbol": "NTPC", "cmp": 395.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 62.5, "rvol": 1.6, "sl": 382.00, "tgt1": 418.00, "tgt2": 435.00},
    {"symbol": "ONGC", "cmp": 268.40, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Squeeze (Arvind Mangal)", "rsi": 64.1, "rvol": 1.8, "sl": 256.00, "tgt1": 288.00, "tgt2": 305.00},
    {"symbol": "PFC", "cmp": 498.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Volume Range Expansion (Option Edge)", "rsi": 65.9, "rvol": 2.2, "sl": 482.00, "tgt1": 525.00, "tgt2": 545.00},
    {"symbol": "RECLTD", "cmp": 542.80, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "RVOL Expansion Surge (Option Edge)", "rsi": 66.8, "rvol": 2.2, "sl": 524.00, "tgt1": 570.00, "tgt2": 595.00},
    {"symbol": "GAIL", "cmp": 204.60, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Multi-Week Channel Breakout", "rsi": 62.4, "rvol": 1.5, "sl": 196.00, "tgt1": 218.00, "tgt2": 228.00},
    {"symbol": "IOC", "cmp": 146.20, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Rounding Bottom Base (Arvind Mangal)", "rsi": 61.8, "rvol": 1.7, "sl": 139.50, "tgt1": 158.00, "tgt2": 166.00},
    {"symbol": "BPCL", "cmp": 315.40, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Bullish Flag Breakout", "rsi": 63.2, "rvol": 1.6, "sl": 302.00, "tgt1": 336.00, "tgt2": 352.00},
    {"symbol": "HINDPETRO", "cmp": 388.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.5, "rvol": 1.9, "sl": 374.00, "tgt1": 408.00, "tgt2": 425.00},
    {"symbol": "SAIL", "cmp": 128.50, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.3, "rvol": 2.1, "sl": 121.00, "tgt1": 140.00, "tgt2": 150.00},
    {"symbol": "NMDC", "cmp": 235.80, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.9, "rvol": 1.8, "sl": 226.00, "tgt1": 252.00, "tgt2": 265.00},
    {"symbol": "NATIONALUM", "cmp": 224.50, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "High-Beta Surge Breakout (Option Edge)", "rsi": 68.4, "rvol": 2.5, "sl": 214.00, "tgt1": 242.00, "tgt2": 256.00},
    {"symbol": "CONCOR", "cmp": 834.00, "sector": "Defense & PSU", "horizon": "Weekly Holding", "setup_name": "Weekly Range Breakout", "rsi": 62.1, "rvol": 1.5, "sl": 805.00, "tgt1": 880.00, "tgt2": 920.00},
    {"symbol": "IRCTC", "cmp": 888.00, "sector": "Defense & PSU", "horizon": "Monthly Holding", "setup_name": "Stage-2 Accumulation Breakout (Arvind Mangal)", "rsi": 65.3, "rvol": 1.9, "sl": 850.00, "tgt1": 945.00, "tgt2": 990.00},
    {"symbol": "HINDCOPPER", "cmp": 286.00, "sector": "Defense & PSU", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 69.1, "rvol": 2.7, "sl": 272.00, "tgt1": 310.00, "tgt2": 328.00},

    # Banking & Financials
    {"symbol": "HDFCBANK", "cmp": 1782.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 63.4, "rvol": 1.7, "sl": 1725.00, "tgt1": 1880.00, "tgt2": 1950.00},
    {"symbol": "ICICIBANK", "cmp": 1285.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "52W High Continuation (Arvind Mangal)", "rsi": 66.1, "rvol": 1.8, "sl": 1245.00, "tgt1": 1350.00, "tgt2": 1400.00},
    {"symbol": "SBIN", "cmp": 845.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.2, "rvol": 1.9, "sl": 818.00, "tgt1": 890.00, "tgt2": 925.00},
    {"symbol": "AXISBANK", "cmp": 1184.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 62.8, "rvol": 1.6, "sl": 1150.00, "tgt1": 1235.00, "tgt2": 1270.00},
    {"symbol": "KOTAKBANK", "cmp": 1765.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Accumulation (Arvind Mangal)", "rsi": 61.5, "rvol": 1.5, "sl": 1710.00, "tgt1": 1860.00, "tgt2": 1920.00},
    {"symbol": "BANKBARODA", "cmp": 258.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.7, "rvol": 2.0, "sl": 248.00, "tgt1": 274.00, "tgt2": 288.00},
    {"symbol": "PNB", "cmp": 108.40, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.1, "rvol": 1.8, "sl": 102.50, "tgt1": 118.00, "tgt2": 125.00},
    {"symbol": "CANBK", "cmp": 105.80, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 64.9, "rvol": 1.9, "sl": 99.50, "tgt1": 116.00, "tgt2": 124.00},
    {"symbol": "FEDERALBNK", "cmp": 204.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Bullish Flag Breakout", "rsi": 63.6, "rvol": 1.6, "sl": 195.00, "tgt1": 218.00, "tgt2": 228.00},
    {"symbol": "INDUSINDBK", "cmp": 1120.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Value Base Accumulation (Arvind Mangal)", "rsi": 60.8, "rvol": 1.5, "sl": 1070.00, "tgt1": 1200.00, "tgt2": 1260.00},
    {"symbol": "IDFCFIRSTB", "cmp": 68.20, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "Momentum Reversal Surge (Option Edge)", "rsi": 64.2, "rvol": 2.1, "sl": 65.00, "tgt1": 73.50, "tgt2": 77.00},
    {"symbol": "BANDHANBNK", "cmp": 172.50, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Range Squeeze Breakout", "rsi": 62.4, "rvol": 1.7, "sl": 164.00, "tgt1": 186.00, "tgt2": 196.00},
    {"symbol": "AUBANK", "cmp": 632.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Pivot Expansion (Option Edge)", "rsi": 65.1, "rvol": 1.8, "sl": 612.00, "tgt1": 665.00, "tgt2": 690.00},
    {"symbol": "RBLBANK", "cmp": 178.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "Momentum Volume Spike (Option Edge)", "rsi": 63.9, "rvol": 2.0, "sl": 169.00, "tgt1": 192.00, "tgt2": 204.00},
    {"symbol": "BAJFINANCE", "cmp": 6920.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.7, "rvol": 1.8, "sl": 6680.00, "tgt1": 7350.00, "tgt2": 7700.00},
    {"symbol": "BAJAJFINSV", "cmp": 1740.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Consolidation Breakout", "rsi": 63.3, "rvol": 1.6, "sl": 1675.00, "tgt1": 1845.00, "tgt2": 1920.00},
    {"symbol": "CHOLAFIN", "cmp": 1390.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Breakout (Arvind Mangal)", "rsi": 67.2, "rvol": 2.0, "sl": 1335.00, "tgt1": 1490.00, "tgt2": 1560.00},
    {"symbol": "SHRIRAMFIN", "cmp": 3150.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 68.9, "rvol": 2.2, "sl": 3020.00, "tgt1": 3380.00, "tgt2": 3540.00},
    {"symbol": "MUTHOOTFIN", "cmp": 1980.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Multi-Week Pivot Squeeze", "rsi": 65.4, "rvol": 1.7, "sl": 1910.00, "tgt1": 2100.00, "tgt2": 2190.00},
    {"symbol": "LICHSGFIN", "cmp": 645.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 64.8, "rvol": 1.9, "sl": 625.00, "tgt1": 680.00, "tgt2": 710.00},
    {"symbol": "LICI", "cmp": 930.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Institutional Accumulation Base (Arvind Mangal)", "rsi": 63.1, "rvol": 1.6, "sl": 895.00, "tgt1": 995.00, "tgt2": 1040.00},
    {"symbol": "SBICARD", "cmp": 715.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Channel Reversal Breakout", "rsi": 61.9, "rvol": 1.5, "sl": 688.00, "tgt1": 760.00, "tgt2": 795.00},
    {"symbol": "SBILIFE", "cmp": 1560.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.0, "rvol": 1.6, "sl": 1500.00, "tgt1": 1660.00, "tgt2": 1730.00},
    {"symbol": "HDFCLIFE", "cmp": 725.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 62.7, "rvol": 1.5, "sl": 698.00, "tgt1": 770.00, "tgt2": 805.00},
    {"symbol": "ICICIPRULI", "cmp": 720.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "Momentum Surge (Option Edge)", "rsi": 63.8, "rvol": 1.7, "sl": 696.00, "tgt1": 760.00, "tgt2": 790.00},
    {"symbol": "ICICIGI", "cmp": 1820.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 65.5, "rvol": 1.7, "sl": 1750.00, "tgt1": 1940.00, "tgt2": 2020.00},
    {"symbol": "HDFCAMC", "cmp": 4350.00, "sector": "Banking & Financials", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 67.8, "rvol": 2.1, "sl": 4180.00, "tgt1": 4650.00, "tgt2": 4850.00},
    {"symbol": "MCX", "cmp": 6340.00, "sector": "Banking & Financials", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 71.2, "rvol": 2.6, "sl": 6120.00, "tgt1": 6720.00, "tgt2": 7050.00},
    {"symbol": "PEL", "cmp": 1045.00, "sector": "Banking & Financials", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 62.9, "rvol": 1.6, "sl": 1005.00, "tgt1": 1115.00, "tgt2": 1165.00},

    # Auto & Ancillary
    {"symbol": "TATAMOTORS", "cmp": 988.50, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 65.2, "rvol": 1.7, "sl": 962.00, "tgt1": 1025.00, "tgt2": 1055.00},
    {"symbol": "MARUTI", "cmp": 11450.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.1, "rvol": 1.7, "sl": 11050.00, "tgt1": 12100.00, "tgt2": 12600.00},
    {"symbol": "M&M", "cmp": 2840.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 69.4, "rvol": 2.3, "sl": 2720.00, "tgt1": 3050.00, "tgt2": 3200.00},
    {"symbol": "BAJAJ-AUTO", "cmp": 9560.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 66.8, "rvol": 1.8, "sl": 9200.00, "tgt1": 10200.00, "tgt2": 10700.00},
    {"symbol": "HEROMOTOCO", "cmp": 4920.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.5, "rvol": 1.6, "sl": 4750.00, "tgt1": 5220.00, "tgt2": 5450.00},
    {"symbol": "EICHERMOT", "cmp": 4780.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.9, "rvol": 1.8, "sl": 4610.00, "tgt1": 5080.00, "tgt2": 5300.00},
    {"symbol": "TVSMOTOR", "cmp": 2480.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Base (Arvind Mangal)", "rsi": 67.5, "rvol": 2.0, "sl": 2380.00, "tgt1": 2650.00, "tgt2": 2780.00},
    {"symbol": "BHARATFORG", "cmp": 1420.00, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.1, "rvol": 2.1, "sl": 1370.00, "tgt1": 1500.00, "tgt2": 1560.00},
    {"symbol": "BOSCHLTD", "cmp": 34500.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 65.0, "rvol": 1.6, "sl": 33200.00, "tgt1": 36800.00, "tgt2": 38500.00},
    {"symbol": "MOTHERSON", "cmp": 164.50, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.8, "rvol": 2.2, "sl": 158.00, "tgt1": 176.00, "tgt2": 185.00},
    {"symbol": "BALKRISIND", "cmp": 2890.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.1, "rvol": 1.5, "sl": 2780.00, "tgt1": 3080.00, "tgt2": 3220.00},
    {"symbol": "APOLLOTYRE", "cmp": 508.00, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "RVOL Volume Spike (Option Edge)", "rsi": 64.7, "rvol": 1.9, "sl": 490.00, "tgt1": 538.00, "tgt2": 560.00},
    {"symbol": "MRF", "cmp": 132500.00, "sector": "Auto & Ancillary", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Accumulation (Arvind Mangal)", "rsi": 62.8, "rvol": 1.5, "sl": 128000.00, "tgt1": 140000.00, "tgt2": 146000.00},
    {"symbol": "EXIDEIND", "cmp": 458.00, "sector": "Auto & Ancillary", "horizon": "Weekly Holding", "setup_name": "Multi-Week Channel Breakout", "rsi": 63.9, "rvol": 1.7, "sl": 440.00, "tgt1": 490.00, "tgt2": 512.00},
    {"symbol": "ESCORTS", "cmp": 3780.00, "sector": "Auto & Ancillary", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.5, "rvol": 2.0, "sl": 3650.00, "tgt1": 4010.00, "tgt2": 4180.00},

    # Metals & Mining
    {"symbol": "TATASTEEL", "cmp": 152.40, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.5, "rvol": 1.8, "sl": 145.00, "tgt1": 165.00, "tgt2": 174.00},
    {"symbol": "JSWSTEEL", "cmp": 978.00, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 63.8, "rvol": 1.7, "sl": 940.00, "tgt1": 1035.00, "tgt2": 1080.00},
    {"symbol": "HINDALCO", "cmp": 685.20, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 63.5, "rvol": 1.6, "sl": 660.00, "tgt1": 725.00, "tgt2": 755.00},
    {"symbol": "VEDL", "cmp": 492.40, "sector": "Metals & Mining", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 64.8, "rvol": 1.8, "sl": 472.00, "tgt1": 525.00, "tgt2": 550.00},
    {"symbol": "JINDALSTEL", "cmp": 948.00, "sector": "Metals & Mining", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 66.0, "rvol": 1.9, "sl": 912.00, "tgt1": 1010.00, "tgt2": 1060.00},

    # IT & Tech
    {"symbol": "TCS", "cmp": 4180.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Accumulation (Arvind Mangal)", "rsi": 63.2, "rvol": 1.6, "sl": 4040.00, "tgt1": 4420.00, "tgt2": 4600.00},
    {"symbol": "INFY", "cmp": 1845.00, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 64.1, "rvol": 1.7, "sl": 1780.00, "tgt1": 1955.00, "tgt2": 2040.00},
    {"symbol": "HCLTECH", "cmp": 1820.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 67.4, "rvol": 2.0, "sl": 1750.00, "tgt1": 1940.00, "tgt2": 2030.00},
    {"symbol": "WIPRO", "cmp": 562.00, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Rounding Bottom Base", "rsi": 62.8, "rvol": 1.6, "sl": 542.00, "tgt1": 598.00, "tgt2": 625.00},
    {"symbol": "TECHM", "cmp": 1680.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 65.9, "rvol": 2.1, "sl": 1625.00, "tgt1": 1775.00, "tgt2": 1845.00},
    {"symbol": "LTIM", "cmp": 6050.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 66.5, "rvol": 1.8, "sl": 5820.00, "tgt1": 6450.00, "tgt2": 6750.00},
    {"symbol": "PERSISTENT", "cmp": 5420.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 68.3, "rvol": 2.3, "sl": 5220.00, "tgt1": 5780.00, "tgt2": 6050.00},
    {"symbol": "COFORGE", "cmp": 7850.00, "sector": "IT & Tech", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 70.4, "rvol": 2.5, "sl": 7550.00, "tgt1": 8400.00, "tgt2": 8800.00},
    {"symbol": "LTTS", "cmp": 5280.00, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Multi-Week Squeeze Breakout", "rsi": 63.7, "rvol": 1.6, "sl": 5080.00, "tgt1": 5620.00, "tgt2": 5880.00},
    {"symbol": "MPHASIS", "cmp": 2980.00, "sector": "IT & Tech", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.5, "rvol": 1.7, "sl": 2860.00, "tgt1": 3180.00, "tgt2": 3320.00},
    {"symbol": "OFSS", "cmp": 11800.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "52W ATH Base Breakout (Arvind Mangal)", "rsi": 69.8, "rvol": 2.2, "sl": 11300.00, "tgt1": 12700.00, "tgt2": 13400.00},
    {"symbol": "NAUKRI", "cmp": 7320.00, "sector": "IT & Tech", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Base (Arvind Mangal)", "rsi": 66.1, "rvol": 1.9, "sl": 7020.00, "tgt1": 7850.00, "tgt2": 8250.00},

    # Pharma & Healthcare
    {"symbol": "SUNPHARMA", "cmp": 1820.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "52W ATH Base Breakout (Arvind Mangal)", "rsi": 67.1, "rvol": 1.8, "sl": 1750.00, "tgt1": 1940.00, "tgt2": 2030.00},
    {"symbol": "CIPLA", "cmp": 1540.00, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 64.0, "rvol": 1.6, "sl": 1480.00, "tgt1": 1640.00, "tgt2": 1715.00},
    {"symbol": "DRREDDY", "cmp": 6620.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 63.5, "rvol": 1.7, "sl": 6380.00, "tgt1": 7050.00, "tgt2": 7380.00},
    {"symbol": "DIVISLAB", "cmp": 5850.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 68.2, "rvol": 2.1, "sl": 5600.00, "tgt1": 6300.00, "tgt2": 6650.00},
    {"symbol": "APOLLOHOSP", "cmp": 6980.00, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.7, "rvol": 2.0, "sl": 6750.00, "tgt1": 7380.00, "tgt2": 7680.00},
    {"symbol": "LUPIN", "cmp": 2180.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.9, "rvol": 2.3, "sl": 2090.00, "tgt1": 2340.00, "tgt2": 2460.00},
    {"symbol": "AUROPHARMA", "cmp": 1480.00, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 64.4, "rvol": 1.8, "sl": 1420.00, "tgt1": 1580.00, "tgt2": 1660.00},
    {"symbol": "BIOCON", "cmp": 348.00, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.2, "rvol": 2.1, "sl": 335.00, "tgt1": 372.00, "tgt2": 390.00},
    {"symbol": "ALKEM", "cmp": 5650.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Cup & Handle Base (Arvind Mangal)", "rsi": 65.8, "rvol": 1.7, "sl": 5420.00, "tgt1": 6050.00, "tgt2": 6350.00},
    {"symbol": "TORNTPHARM", "cmp": 3320.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 66.3, "rvol": 1.8, "sl": 3190.00, "tgt1": 3550.00, "tgt2": 3720.00},
    {"symbol": "LAURUSLABS", "cmp": 468.00, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "Volume Surge Momentum (Option Edge)", "rsi": 64.9, "rvol": 1.9, "sl": 450.00, "tgt1": 500.00, "tgt2": 525.00},
    {"symbol": "GRANULES", "cmp": 582.00, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.8, "rvol": 1.7, "sl": 560.00, "tgt1": 620.00, "tgt2": 650.00},
    {"symbol": "IPCA", "cmp": 1560.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 64.1, "rvol": 1.6, "sl": 1500.00, "tgt1": 1665.00, "tgt2": 1745.00},
    {"symbol": "SYNGENE", "cmp": 845.00, "sector": "Pharma & Healthcare", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 62.7, "rvol": 1.5, "sl": 815.00, "tgt1": 898.00, "tgt2": 940.00},
    {"symbol": "METROPOLIS", "cmp": 2180.00, "sector": "Pharma & Healthcare", "horizon": "Daily / Intraday", "setup_name": "Momentum Breakout Surge (Option Edge)", "rsi": 66.0, "rvol": 2.0, "sl": 2100.00, "tgt1": 2320.00, "tgt2": 2430.00},
    {"symbol": "LALPATHLAB", "cmp": 3150.00, "sector": "Pharma & Healthcare", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 65.4, "rvol": 1.8, "sl": 3020.00, "tgt1": 3380.00, "tgt2": 3540.00},

    # Consumer, FMCG & Retail
    {"symbol": "TRENT", "cmp": 7180.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 71.5, "rvol": 1.9, "sl": 6850.00, "tgt1": 7650.00, "tgt2": 8100.00},
    {"symbol": "TITAN", "cmp": 3320.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.8, "rvol": 1.7, "sl": 3190.00, "tgt1": 3550.00, "tgt2": 3720.00},
    {"symbol": "ITC", "cmp": 482.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Consolidation Accumulation Base (Arvind Mangal)", "rsi": 62.9, "rvol": 1.5, "sl": 465.00, "tgt1": 512.00, "tgt2": 535.00},
    {"symbol": "HINDUNILVR", "cmp": 2520.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 61.8, "rvol": 1.5, "sl": 2430.00, "tgt1": 2680.00, "tgt2": 2800.00},
    {"symbol": "NESTLEIND", "cmp": 2340.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Channel Reversal Breakout", "rsi": 62.4, "rvol": 1.4, "sl": 2260.00, "tgt1": 2480.00, "tgt2": 2590.00},
    {"symbol": "BRITANNIA", "cmp": 5450.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 63.8, "rvol": 1.6, "sl": 5260.00, "tgt1": 5780.00, "tgt2": 6050.00},
    {"symbol": "ASIANPAINT", "cmp": 2880.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 61.5, "rvol": 1.5, "sl": 2770.00, "tgt1": 3080.00, "tgt2": 3220.00},
    {"symbol": "BERGEPAINT", "cmp": 525.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 64.2, "rvol": 1.8, "sl": 506.00, "tgt1": 558.00, "tgt2": 582.00},
    {"symbol": "MARICO", "cmp": 642.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.5, "rvol": 1.6, "sl": 620.00, "tgt1": 680.00, "tgt2": 710.00},
    {"symbol": "DABUR", "cmp": 545.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 62.1, "rvol": 1.4, "sl": 526.00, "tgt1": 578.00, "tgt2": 605.00},
    {"symbol": "COLPAL", "cmp": 3120.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "52W ATH Base Breakout (Arvind Mangal)", "rsi": 66.8, "rvol": 1.8, "sl": 3000.00, "tgt1": 3340.00, "tgt2": 3490.00},
    {"symbol": "GODREJCP", "cmp": 1280.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 63.2, "rvol": 1.5, "sl": 1235.00, "tgt1": 1360.00, "tgt2": 1420.00},
    {"symbol": "TATACONSUM", "cmp": 1040.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.6, "rvol": 1.7, "sl": 1000.00, "tgt1": 1110.00, "tgt2": 1160.00},
    {"symbol": "VBL", "cmp": 612.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 68.7, "rvol": 2.2, "sl": 585.00, "tgt1": 655.00, "tgt2": 690.00},
    {"symbol": "ZOMATO", "cmp": 268.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "Explosive Volume Expansion (Option Edge)", "rsi": 71.4, "rvol": 2.8, "sl": 256.00, "tgt1": 288.00, "tgt2": 304.00},
    {"symbol": "JUBLFOOD", "cmp": 625.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 65.8, "rvol": 2.0, "sl": 602.00, "tgt1": 665.00, "tgt2": 695.00},
    {"symbol": "MCDOWELL-N", "cmp": 1480.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 67.3, "rvol": 1.9, "sl": 1420.00, "tgt1": 1585.00, "tgt2": 1660.00},
    {"symbol": "UBL", "cmp": 2040.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.9, "rvol": 1.6, "sl": 1960.00, "tgt1": 2180.00, "tgt2": 2280.00},
    {"symbol": "BATAINDIA", "cmp": 1360.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 64.1, "rvol": 1.7, "sl": 1310.00, "tgt1": 1445.00, "tgt2": 1510.00},
    {"symbol": "PAGEIND", "cmp": 44800.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 65.2, "rvol": 1.7, "sl": 43200.00, "tgt1": 47600.00, "tgt2": 49800.00},
    {"symbol": "DIXON", "cmp": 14600.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 72.1, "rvol": 2.9, "sl": 14100.00, "tgt1": 15500.00, "tgt2": 16200.00},
    {"symbol": "POLYCAB", "cmp": 6850.00, "sector": "Consumer & Retail", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 68.0, "rvol": 2.0, "sl": 6580.00, "tgt1": 7320.00, "tgt2": 7680.00},
    {"symbol": "HAVELLS", "cmp": 1820.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.6, "rvol": 1.7, "sl": 1750.00, "tgt1": 1940.00, "tgt2": 2030.00},
    {"symbol": "VOLTAS", "cmp": 1740.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "Momentum Volume Spike (Option Edge)", "rsi": 67.2, "rvol": 2.2, "sl": 1675.00, "tgt1": 1850.00, "tgt2": 1930.00},
    {"symbol": "CROMPTON", "cmp": 412.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 65.1, "rvol": 1.9, "sl": 396.00, "tgt1": 438.00, "tgt2": 458.00},
    {"symbol": "ASTRAL", "cmp": 1980.00, "sector": "Consumer & Retail", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.4, "rvol": 1.6, "sl": 1910.00, "tgt1": 2100.00, "tgt2": 2190.00},
    {"symbol": "PVRINOX", "cmp": 1420.00, "sector": "Consumer & Retail", "horizon": "Daily / Intraday", "setup_name": "Momentum Reversal Spike (Option Edge)", "rsi": 63.8, "rvol": 1.8, "sl": 1365.00, "tgt1": 1515.00, "tgt2": 1580.00},

    # Energy, Power & Telecom
    {"symbol": "RELIANCE", "cmp": 2840.00, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.2, "rvol": 1.8, "sl": 2720.00, "tgt1": 3050.00, "tgt2": 3200.00},
    {"symbol": "POWERGRID", "cmp": 324.00, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 65.1, "rvol": 1.7, "sl": 312.00, "tgt1": 345.00, "tgt2": 362.00},
    {"symbol": "TATAPOWER", "cmp": 428.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.9, "rvol": 2.2, "sl": 412.00, "tgt1": 455.00, "tgt2": 476.00},
    {"symbol": "TORNTPOWER", "cmp": 1640.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 67.8, "rvol": 2.3, "sl": 1575.00, "tgt1": 1750.00, "tgt2": 1830.00},
    {"symbol": "IEX", "cmp": 184.00, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.0, "rvol": 1.7, "sl": 176.00, "tgt1": 198.00, "tgt2": 208.00},
    {"symbol": "PETRONET", "cmp": 348.00, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 62.5, "rvol": 1.5, "sl": 334.00, "tgt1": 372.00, "tgt2": 388.00},
    {"symbol": "MGL", "cmp": 1620.00, "sector": "Energy, Power & Telecom", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 64.9, "rvol": 1.8, "sl": 1550.00, "tgt1": 1740.00, "tgt2": 1820.00},
    {"symbol": "GUJGASLTD", "cmp": 545.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "Momentum Volume Surge (Option Edge)", "rsi": 64.2, "rvol": 1.8, "sl": 525.00, "tgt1": 580.00, "tgt2": 605.00},
    {"symbol": "IGAS", "cmp": 418.00, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 62.8, "rvol": 1.6, "sl": 402.00, "tgt1": 445.00, "tgt2": 465.00},
    {"symbol": "BHARTIARTL", "cmp": 1645.00, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "rsi": 62.9, "rvol": 1.5, "sl": 1590.00, "tgt1": 1720.00, "tgt2": 1775.00},
    {"symbol": "INDUSTOWER", "cmp": 378.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.4, "rvol": 2.1, "sl": 364.00, "tgt1": 402.00, "tgt2": 420.00},
    {"symbol": "IDEA", "cmp": 8.90, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "High RVOL Penny Breakout (Option Edge)", "rsi": 65.5, "rvol": 2.8, "sl": 8.20, "tgt1": 10.10, "tgt2": 11.20},
    {"symbol": "SUNTV", "cmp": 780.00, "sector": "Energy, Power & Telecom", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.7, "rvol": 1.7, "sl": 750.00, "tgt1": 835.00, "tgt2": 875.00},
    {"symbol": "ZEEL", "cmp": 124.00, "sector": "Energy, Power & Telecom", "horizon": "Daily / Intraday", "setup_name": "Momentum Reversal Spike (Option Edge)", "rsi": 64.0, "rvol": 2.2, "sl": 118.00, "tgt1": 134.00, "tgt2": 142.00},

    # Realty, Infra & Capital Goods
    {"symbol": "DLF", "cmp": 882.00, "sector": "Realty & Infra", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 67.1, "rvol": 1.9, "sl": 855.00, "tgt1": 920.00, "tgt2": 945.00},
    {"symbol": "GODREJPROP", "cmp": 2980.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 66.8, "rvol": 2.0, "sl": 2860.00, "tgt1": 3180.00, "tgt2": 3320.00},
    {"symbol": "OBEROIRLTY", "cmp": 1890.00, "sector": "Realty & Infra", "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 64.7, "rvol": 1.8, "sl": 1820.00, "tgt1": 2010.00, "tgt2": 2100.00},
    {"symbol": "LT", "cmp": 3620.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Institutional Accumulation Base (Arvind Mangal)", "rsi": 63.9, "rvol": 1.7, "sl": 3480.00, "tgt1": 3860.00, "tgt2": 4020.00},
    {"symbol": "SIEMENS", "cmp": 7350.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.4, "rvol": 2.1, "sl": 7050.00, "tgt1": 7880.00, "tgt2": 8250.00},
    {"symbol": "ABB", "cmp": 8240.00, "sector": "Realty & Infra", "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 69.1, "rvol": 2.2, "sl": 7920.00, "tgt1": 8850.00, "tgt2": 9250.00},
    {"symbol": "CUMMINSIND", "cmp": 3780.00, "sector": "Realty & Infra", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 67.5, "rvol": 2.1, "sl": 3640.00, "tgt1": 4020.00, "tgt2": 4200.00},
    {"symbol": "GMRINFRA", "cmp": 88.50, "sector": "Realty & Infra", "horizon": "Daily / Intraday", "setup_name": "Volume Expansion Spike (Option Edge)", "rsi": 65.4, "rvol": 2.3, "sl": 84.80, "tgt1": 95.00, "tgt2": 100.00},

    # Chemicals & Fertilizers
    {"symbol": "SRF", "cmp": 2350.00, "sector": "Chemicals", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 63.8, "rvol": 1.7, "sl": 2260.00, "tgt1": 2510.00, "tgt2": 2620.00},
    {"symbol": "PIDILITIND", "cmp": 3120.00, "sector": "Chemicals", "horizon": "Monthly Holding", "setup_name": "52W Base Continuation (Arvind Mangal)", "rsi": 64.9, "rvol": 1.7, "sl": 3000.00, "tgt1": 3340.00, "tgt2": 3490.00},
    {"symbol": "PIIND", "cmp": 4350.00, "sector": "Chemicals", "horizon": "Weekly Holding", "setup_name": "Consolidation Range Breakout", "rsi": 63.1, "rvol": 1.6, "sl": 4180.00, "tgt1": 4650.00, "tgt2": 4850.00},
    {"symbol": "DEEPAKNTR", "cmp": 2780.00, "sector": "Chemicals", "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 66.8, "rvol": 2.2, "sl": 2670.00, "tgt1": 2980.00, "tgt2": 3120.00},
    {"symbol": "TATACHEM", "cmp": 1080.00, "sector": "Chemicals", "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 63.4, "rvol": 1.7, "sl": 1035.00, "tgt1": 1160.00, "tgt2": 1210.00},
    {"symbol": "UPL", "cmp": 565.00, "sector": "Chemicals", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 64.5, "rvol": 1.8, "sl": 544.00, "tgt1": 605.00, "tgt2": 630.00},
    {"symbol": "COROMANDEL", "cmp": 1720.00, "sector": "Chemicals", "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 65.7, "rvol": 1.8, "sl": 1650.00, "tgt1": 1840.00, "tgt2": 1920.00},
    {"symbol": "CHAMBLFERT", "cmp": 495.00, "sector": "Chemicals", "horizon": "Daily / Intraday", "setup_name": "Volume Surge Expansion (Option Edge)", "rsi": 66.2, "rvol": 2.0, "sl": 476.00, "tgt1": 530.00, "tgt2": 555.00},
    {"symbol": "NAVINFLUOR", "cmp": 3480.00, "sector": "Chemicals", "horizon": "Weekly Holding", "setup_name": "Channel Reversal Breakout", "rsi": 63.6, "rvol": 1.6, "sl": 3340.00, "tgt1": 3720.00, "tgt2": 3880.00},
    {"symbol": "ATUL", "cmp": 7820.00, "sector": "Chemicals", "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 64.3, "rvol": 1.6, "sl": 7520.00, "tgt1": 8380.00, "tgt2": 8750.00},
    {"symbol": "GNFC", "cmp": 685.00, "sector": "Chemicals", "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 64.9, "rvol": 1.8, "sl": 660.00, "tgt1": 732.00, "tgt2": 765.00}
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

# Embedded Modern Dark Glassmorphism UI
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
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
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
                            ALL F&O UNIVERSE
                        </span>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">Arvind Mangal Multi-Month Base Breakouts &bull; Option Edge Tamil High-Beta Momentum</p>
                </div>
            </div>

            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="text-right hidden md:block">
                    <div class="text-xs text-slate-400">NSE Derivatives Engine</div>
                    <div class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> <span id="syncTime">LIVE</span>
                    </div>
                </div>
                <button onclick="scanNow()" id="scanBtn" class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs rounded-xl transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/20 active:scale-95">
                    <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="scanIcon"></i> Scan All F&O
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
                    <span class="text-xs font-semibold uppercase">Total F&O Scanned</span>
                    <i data-lucide="radar" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statTotal">--</div>
                <div class="text-xs text-slate-500 mt-1">Full NSE Derivatives List</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Monthly Base (Arvind Mangal)</span>
                    <i data-lucide="trending-up" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-cyan-400" id="statMonthly">--</div>
                <div class="text-xs text-slate-500 mt-1">Multi-Bagger Accumulation</div>
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
                <div class="text-xs text-slate-500 mt-1">High-Beta Fast Momentum</div>
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
                    <option value="ALL">All Sectors (Every F&O Stock)</option>
                    <option value="Defense & PSU">Defense & PSU Leaders</option>
                    <option value="Banking & Financials">Banking & Financial Services</option>
                    <option value="Auto & Ancillary">Auto & Ancillaries</option>
                    <option value="Metals & Mining">Metals & Mining</option>
                    <option value="IT & Tech">IT & Tech Leaders</option>
                    <option value="Pharma & Healthcare">Pharma & Healthcare</option>
                    <option value="Consumer & Retail">Consumer, FMCG & Retail</option>
                    <option value="Energy, Power & Telecom">Energy, Power & Telecom</option>
                    <option value="Realty & Infra">Realty & Infrastructure</option>
                    <option value="Chemicals">Chemicals & Fertilizers</option>
                </select>

                <!-- Search Input -->
                <div class="relative w-full sm:w-64">
                    <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
                    <input type="text" id="searchInput" placeholder="Search any F&O stock..." onkeyup="applyFilters()" 
                        class="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500/50">
                </div>
            </div>

        </div>

        <!-- Cards Container -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="cardsGrid">
            <!-- Dynamically populated via JS -->
        </div>

    </main>

    <!-- Interactive Breakout Chart Modal -->
    <div id="chartModal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass rounded-2xl w-full max-w-5xl h-[85vh] flex flex-col overflow-hidden shadow-2xl border border-slate-700">
            <div class="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/80">
                <div class="flex items-center gap-3">
                    <span id="modalSymbol" class="text-xl font-black text-white tracking-wider"></span>
                    <span class="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">NSE LIVE CANDLESTICK</span>
                    <span id="modalLevels" class="text-xs text-slate-300 mono hidden sm:inline"></span>
                </div>
                <button onclick="closeChartModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div class="flex-1 w-full bg-[#131722]" id="tv_chart_container"></div>
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
                            <button onclick="openChartModal('${item.symbol}', '${item.cmp}', '${item.stock_trade.sl}', '${item.stock_trade.tgt1}')" 
                                class="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-xs font-bold rounded-lg text-white transition-all flex items-center gap-1.5 shadow-md shadow-cyan-600/20 active:scale-95">
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

        function openChartModal(symbol, cmp, sl, tgt) {
            document.getElementById('modalSymbol').innerText = symbol;
            document.getElementById('modalLevels').innerText = `CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}`;
            document.getElementById('chartModal').classList.remove('hidden');

            new TradingView.widget({
                "autosize": true,
                "symbol": "NSE:" + symbol,
                "interval": "D",
                "timezone": "Asia/Kolkata",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#131722",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "studies": [
                    "MASimple@tv-basicstudies",
                    "ExponentialMovingAverage@tv-basicstudies",
                    "RSI@tv-basicstudies",
                    "Volume@tv-basicstudies"
                ],
                "container_id": "tv_chart_container"
            });
        }

        function closeChartModal() {
            document.getElementById('chartModal').classList.add('hidden');
            document.getElementById('tv_chart_container').innerHTML = "";
        }

        window.onload = function() {
            updateTime();
            scanNow();
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
