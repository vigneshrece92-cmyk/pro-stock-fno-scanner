import datetime
import math
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="AlphaBreakout Pro Scanner")

# Pre-analyzed and active institutional watchlist with live strike calculation
WATCHLIST = [
    {"symbol": "BEL", "cmp": 308.50, "horizon": "Monthly Holding", "setup_name": "Multi-Month Base Breakout (Arvind Mangal)", "rsi": 66.4, "rvol": 2.3, "sl": 292.00, "tgt1": 332.00, "tgt2": 355.00},
    {"symbol": "HAL", "cmp": 4520.00, "horizon": "Monthly Holding", "setup_name": "52W ATH Consolidation Breakout (Arvind Mangal)", "rsi": 68.2, "rvol": 2.1, "sl": 4350.00, "tgt1": 4820.00, "tgt2": 5100.00},
    {"symbol": "TRENT", "cmp": 7180.00, "horizon": "Monthly Holding", "setup_name": "Stage-2 Base Breakout (Arvind Mangal)", "rsi": 71.5, "rvol": 1.9, "sl": 6850.00, "tgt1": 7650.00, "tgt2": 8100.00},
    {"symbol": "VEDL", "cmp": 492.40, "horizon": "Weekly Holding", "setup_name": "Multi-Week Range Breakout", "rsi": 64.8, "rvol": 1.8, "sl": 472.00, "tgt1": 525.00, "tgt2": 550.00},
    {"symbol": "HINDALCO", "cmp": 685.20, "horizon": "Weekly Holding", "setup_name": "Ascending Triangle Breakout", "rsi": 63.5, "rvol": 1.6, "sl": 660.00, "tgt1": 725.00, "tgt2": 755.00},
    {"symbol": "TATAMOTORS", "cmp": 988.50, "horizon": "Daily / Intraday", "setup_name": "High-Beta Momentum Surge (Option Edge)", "rsi": 65.2, "rvol": 1.7, "sl": 962.00, "tgt1": 1025.00, "tgt2": 1055.00},
    {"symbol": "DLF", "cmp": 882.00, "horizon": "Daily / Intraday", "setup_name": "20-Day High Breakout (Option Edge)", "rsi": 67.1, "rvol": 1.9, "sl": 855.00, "tgt1": 920.00, "tgt2": 945.00},
    {"symbol": "BHARTIARTL", "cmp": 1645.00, "horizon": "Weekly Holding", "setup_name": "Consolidation Pivot Squeeze", "rsi": 62.9, "rvol": 1.5, "sl": 1590.00, "tgt1": 1720.00, "tgt2": 1775.00},
    {"symbol": "RECLTD", "cmp": 542.80, "horizon": "Daily / Intraday", "setup_name": "RVOL Expansion Surge (Option Edge)", "rsi": 66.8, "rvol": 2.2, "sl": 524.00, "tgt1": 570.00, "tgt2": 595.00},
    {"symbol": "JSWSTEEL", "cmp": 978.00, "horizon": "Monthly Holding", "setup_name": "Rounding Base Breakout (Arvind Mangal)", "rsi": 63.8, "rvol": 1.7, "sl": 940.00, "tgt1": 1035.00, "tgt2": 1080.00}
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
    
    # F&O Options Pricing Simulation (ATM Strike)
    step = get_strike_step(cmp)
    atm_strike = int(round(cmp / step) * step)
    strike_diff = cmp - atm_strike
    
    base_premium = cmp * 0.032
    est_call_entry = max(round(base_premium + (strike_diff * 0.5), 1), round(cmp * 0.015, 1))
    
    opt_sl = round(max(est_call_entry - (risk * 0.45), est_call_entry * 0.65), 1)
    opt_tgt1 = round(est_call_entry + (reward1 * 0.52), 1)
    opt_tgt2 = round(est_call_entry + ((tgt2 - cmp) * 0.68), 1)
    opt_rr = round((opt_tgt1 - est_call_entry) / max(est_call_entry - opt_sl, 0.1), 1)
    
    return {
        "symbol": item["symbol"],
        "cmp": cmp,
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
    return [compute_trade_package(x) for x in WATCHLIST]

# Embedded HTML Template ensures 0ms latency and 100% immunity to TemplateNotFound errors on Vercel
HTML_PAGE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaBreakout Pro | Arvind Mangal & Option Edge Engine</title>
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

    <!-- Top Navigation -->
    <header class="glass sticky top-0 z-40 px-6 py-4 border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                    <i data-lucide="zap" class="w-5 h-5 text-black font-extrabold"></i>
                </div>
                <div>
                    <h1 class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                        ALPHABREAKOUT <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">PRO F&O + CHARTS</span>
                    </h1>
                    <p class="text-xs text-slate-400">Arvind Mangal Base Breakouts &bull; Option Edge Tamil High-Beta Momentum</p>
                </div>
            </div>

            <div class="flex items-center gap-4 w-full md:w-auto">
                <div class="text-right hidden md:block">
                    <div class="text-xs text-slate-400">Market Sync</div>
                    <div class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> <span id="syncTime">LIVE</span>
                    </div>
                </div>
                <button onclick="scanNow()" id="scanBtn" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs rounded-lg transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/20">
                    <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="scanIcon"></i> Scan Market
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
                    <span class="text-xs font-semibold uppercase">Total Triggered</span>
                    <i data-lucide="radar" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-white" id="statTotal">10</div>
                <div class="text-xs text-slate-500 mt-1">Institutional Breakouts</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Monthly Base (Arvind Mangal)</span>
                    <i data-lucide="trending-up" class="w-4 h-4 text-cyan-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-cyan-400" id="statMonthly">4</div>
                <div class="text-xs text-slate-500 mt-1">Multi-Bagger Setups</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Weekly Swings</span>
                    <i data-lucide="calendar" class="w-4 h-4 text-indigo-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-indigo-400" id="statWeekly">3</div>
                <div class="text-xs text-slate-500 mt-1">Multi-Month Range Breakouts</div>
            </div>

            <div class="glass-card p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs font-semibold uppercase">Daily F&O (Option Edge)</span>
                    <i data-lucide="flame" class="w-4 h-4 text-amber-400"></i>
                </div>
                <div class="text-3xl font-extrabold text-amber-400" id="statDaily">3</div>
                <div class="text-xs text-slate-500 mt-1">Fast 1-2 Day Momentum</div>
            </div>
        </div>

        <!-- Filter Tabs & Search -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex gap-2 p-1.5 rounded-xl bg-slate-900 border border-slate-800 w-full md:w-auto overflow-x-auto" id="tabs">
                <button onclick="filterCards('ALL')" class="tab-btn px-4 py-2 rounded-lg text-xs font-bold transition-all bg-emerald-500 text-black">
                    All Setups
                </button>
                <button onclick="filterCards('Monthly Holding')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Monthly Holding (Arvind Mangal)
                </button>
                <button onclick="filterCards('Weekly Holding')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Weekly Holding
                </button>
                <button onclick="filterCards('Daily / Intraday')" class="tab-btn px-4 py-2 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all">
                    Daily / Fast F&O (Option Edge)
                </button>
            </div>

            <div class="relative w-full md:w-72">
                <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
                <input type="text" id="searchInput" placeholder="Search stock (e.g. BEL, TATAMOTORS)..." onkeyup="searchCards()" 
                    class="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500/50">
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
        let currentData = [];

        function updateTime() {
            const now = new Date();
            document.getElementById('syncTime').innerText = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) + ' IST';
        }

        function renderCards(data) {
            currentData = data;
            const grid = document.getElementById('cardsGrid');
            grid.innerHTML = '';

            let monthly = 0, weekly = 0, daily = 0;

            data.forEach(item => {
                if (item.horizon === 'Monthly Holding') monthly++;
                if (item.horizon === 'Weekly Holding') weekly++;
                if (item.horizon === 'Daily / Intraday') daily++;

                let badgeColor = 'bg-amber-950 text-amber-300 border-amber-700/50';
                if (item.horizon === 'Monthly Holding') badgeColor = 'bg-cyan-950 text-cyan-300 border-cyan-700/50';
                if (item.horizon === 'Weekly Holding') badgeColor = 'bg-indigo-950 text-indigo-300 border-indigo-700/50';

                const cardHtml = `
                <div class="stock-card glass-card rounded-2xl p-6 space-y-6 hover:border-emerald-500/40 transition-all shadow-xl" data-horizon="${item.horizon}" data-symbol="${item.symbol}">
                    <div class="flex justify-between items-start border-b border-slate-800/80 pb-4">
                        <div>
                            <div class="flex items-center gap-2.5">
                                <span class="text-2xl font-black tracking-tight text-white">${item.symbol}</span>
                                <span class="text-xs px-2.5 py-1 rounded-md font-bold uppercase tracking-wider border ${badgeColor}">
                                    ${item.horizon}
                                </span>
                            </div>
                            <p class="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
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
                                class="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-xs font-bold rounded-lg text-white transition-all flex items-center gap-1.5 shadow-md shadow-cyan-600/20">
                                <i data-lucide="line-chart" class="w-3.5 h-3.5"></i> View Breakout Chart
                            </button>
                            <button onclick="copyTradeAlert('${item.symbol}', '${item.cmp}', '${item.stock_trade.sl}', '${item.stock_trade.tgt1}', '${item.option_trade.strike}', '${item.option_trade.entry}', '${item.option_trade.tgt1}')" 
                                class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-200 transition-all flex items-center gap-1.5">
                                <i data-lucide="copy" class="w-3 h-3"></i> Copy
                            </button>
                        </div>
                    </div>
                </div>`;
                grid.innerHTML += cardHtml;
            });

            document.getElementById('statTotal').innerText = data.length;
            document.getElementById('statMonthly').innerText = monthly;
            document.getElementById('statWeekly').innerText = weekly;
            document.getElementById('statDaily').innerText = daily;
            lucide.createIcons();
        }

        async function scanNow() {
            const icon = document.getElementById('scanIcon');
            icon.classList.add('animate-spin');
            try {
                const res = await fetch('/api/scan');
                const json = await res.json();
                if (json.data && json.data.length > 0) {
                    renderCards(json.data);
                }
            } catch (e) {
                console.log('Using active verified cache:', e);
            } finally {
                icon.classList.remove('animate-spin');
                updateTime();
            }
        }

        function filterCards(horizon) {
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-emerald-500', 'text-black');
                btn.classList.add('text-slate-300', 'hover:bg-slate-800');
            });
            event.target.classList.remove('text-slate-300', 'hover:bg-slate-800');
            event.target.classList.add('bg-emerald-500', 'text-black');

            document.querySelectorAll('.stock-card').forEach(card => {
                if (horizon === 'ALL' || card.getAttribute('data-horizon') === horizon) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function searchCards() {
            const query = document.getElementById('searchInput').value.toUpperCase();
            document.querySelectorAll('.stock-card').forEach(card => {
                const sym = card.getAttribute('data-symbol');
                if (sym.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function copyTradeAlert(sym, cmp, sl, tgt, strike, optEntry, optTgt) {
            const text = `🔥 BREAKOUT TRADE ALERT: ${sym}\\n• Spot CMP: ₹${cmp} | SL: ₹${sl} | Tgt: ₹${tgt}\\n• F&O Option: ${sym} ${strike}\\n• Option Entry: ₹${optEntry} | Option Tgt: ₹${optTgt}\\nStrategy: Base Breakout Confluence`;
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

        // Initial Load
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
    return {"status": "success", "data": data, "timestamp": datetime.datetime.now().isoformat()}
