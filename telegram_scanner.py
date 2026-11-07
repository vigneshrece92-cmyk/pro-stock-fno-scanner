"""
Vickyvaio Breakouts - Automated Institutional Telegram F&O Signal Scanner
Equipped with Angel One SmartAPI for 0-Latency Real-Time Stock & Strike Prices
Operating Hours: 9:15 AM - 2:30 PM IST (Monday to Friday)
"""

import sys
import os
import time
import datetime
import json
import logging
from typing import Dict, Optional, Tuple
import requests
import pyotp

# Force UTF-8 stdout encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VickyvaioTelegramScanner")

# Configuration & Secrets
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7031852910:AAGkhuuDnuvAYY_llzuBryJQ_uAod9ekFk4")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "927756502")

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY", "hmnP0Ln2")
ANGEL_CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE", "V54384326")
ANGEL_PIN = os.getenv("ANGEL_PIN", "2305")
ANGEL_TOTP_KEY = os.getenv("ANGEL_TOTP_KEY", "47CUKNA5GCAHYNYZVXVXBQBVKE")

CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIP_CACHE_PATH = os.path.join(CACHE_DIR, "scrip_master_cache.json")
NIFTY_BOT_CACHE = r"C:\Users\Vicky\.gemini\antigravity\scratch\nifty_angelone_bot\scrip_master_cache.json"

DISPATCHED_TODAY = set()

# Initialize SmartAPI Client
smart_api = None
scrips_cache = []

def send_telegram_alert(message: str) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID),
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=8)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")
        return False

def init_angel_one():
    """Initializes and authenticates Angel One SmartConnect."""
    global smart_api
    try:
        from SmartApi import SmartConnect
        smart_api = SmartConnect(api_key=ANGEL_API_KEY)
        totp = pyotp.TOTP(ANGEL_TOTP_KEY).now()
        session = smart_api.generateSession(ANGEL_CLIENT_CODE, ANGEL_PIN, totp)
        if session.get("status"):
            logger.info("Angel One SmartAPI connected successfully! (0-Latency Quotes Active)")
            return True
        else:
            logger.warning(f"Angel One session failed: {session.get('message')}. Falling back to default feeds.")
            smart_api = None
            return False
    except Exception as e:
        logger.warning(f"Could not connect to Angel One SmartAPI: {e}. Falling back to default feeds.")
        smart_api = None
        return False

def load_scrip_master():
    """Loads Angel One Scrip Master for accurate symbol and token mapping."""
    global scrips_cache
    try:
        # Check local folder first
        if os.path.exists(SCRIP_CACHE_PATH) and os.path.getsize(SCRIP_CACHE_PATH) > 100000:
            with open(SCRIP_CACHE_PATH, "r", encoding="utf-8") as f:
                scrips_cache = json.load(f)
            logger.info(f"Loaded {len(scrips_cache)} scrip records from local cache.")
            return True
        
        # Check nifty_angelone_bot folder next
        if os.path.exists(NIFTY_BOT_CACHE) and os.path.getsize(NIFTY_BOT_CACHE) > 100000:
            with open(NIFTY_BOT_CACHE, "r", encoding="utf-8") as f:
                scrips_cache = json.load(f)
            logger.info(f"Loaded {len(scrips_cache)} scrip records from nifty_angelone_bot cache.")
            return True

        # Download from Angel One OpenAPI
        logger.info("Downloading latest Scrip Master from Angel One OpenAPI (~4MB)...")
        r = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json", timeout=25)
        if r.status_code == 200:
            scrips_cache = r.json()
            with open(SCRIP_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(scrips_cache, f)
            logger.info(f"Downloaded and cached {len(scrips_cache)} scrip records.")
            return True
    except Exception as e:
        logger.error(f"Error loading scrip master: {e}")
    return False

def get_live_angel_quote(sym: str, option_type: str = "CE", default_strike: str = "") -> Optional[Dict]:
    """
    Fetches real-time Spot CMP, ATM Option Token, and live Option Premium LTP
    directly from Angel One SmartAPI.
    """
    global smart_api, scrips_cache
    if not smart_api or not scrips_cache:
        return None

    try:
        # 1. Resolve Spot Equity Token
        eq_matches = [s for s in scrips_cache if s.get("symbol") == f"{sym}-EQ" and s.get("exch_seg") == "NSE"]
        if not eq_matches:
            return None
        
        eq_token = eq_matches[0]["token"]
        spot_res = smart_api.ltpData("NSE", f"{sym}-EQ", eq_token)
        spot_ltp = spot_res.get("data", {}).get("ltp", 0.0) if spot_res.get("status") else 0.0

        if spot_ltp <= 0:
            return None

        # 2. Resolve Nearest Expiry Options
        pool = [s for s in scrips_cache if s.get("name") == sym and s.get("exch_seg") == "NFO" and s.get("instrumenttype") == "OPTSTK"]
        if not pool:
            return {"spot_ltp": spot_ltp}

        now = datetime.datetime.now()
        expiries = []
        for s in pool:
            try:
                exp_dt = datetime.datetime.strptime(s.get("expiry", ""), "%d%b%Y")
                if exp_dt.date() >= now.date():
                    expiries.append(exp_dt)
            except Exception:
                pass

        if not expiries:
            return {"spot_ltp": spot_ltp}

        nearest_exp_str = min(expiries).strftime("%d%b%Y").upper()
        typed_pool = [s for s in pool if s.get("expiry", "").upper() == nearest_exp_str and s.get("symbol", "").endswith(option_type)]
        if not typed_pool:
            return {"spot_ltp": spot_ltp}

        # 3. ATM Strike Selection (Delta ~ 0.50)
        def parse_strike(s):
            try:
                return float(s.get("strike", 0.0)) / 100.0
            except Exception:
                return 999999.0

        best_contract = min(typed_pool, key=lambda s: abs(parse_strike(s) - spot_ltp))
        strike_val = parse_strike(best_contract)
        opt_token = best_contract["token"]
        opt_symbol = best_contract["symbol"]

        # 4. Fetch Live Option Premium LTP
        opt_res = smart_api.ltpData("NFO", opt_symbol, opt_token)
        opt_ltp = opt_res.get("data", {}).get("ltp", 0.0) if opt_res.get("status") else 0.0

        return {
            "spot_ltp": spot_ltp,
            "strike_str": f"{strike_val:g} {option_type}",
            "contract": opt_symbol,
            "opt_ltp": opt_ltp,
            "opt_token": opt_token,
            "expiry": nearest_exp_str
        }
    except Exception as e:
        logger.warning(f"Angel One live quote exception for {sym}: {e}")
        return None

def is_market_hours(force=False) -> bool:
    if force:
        return True
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # IST is UTC + 5:30
    ist_min = (now_utc.hour * 60 + now_utc.minute + 330) % 1440
    weekday = now_utc.weekday()
    # Monday = 0, Friday = 4; 9:15 AM (555 min) to 2:30 PM (870 min)
    return (weekday < 5) and (555 <= ist_min <= 870)

def run_scanner_cycle(base_url="https://pro-stock-fno-scanner.vercel.app"):
    logger.info("Polling verified breakout & breakdown radar...")
    try:
        r = requests.get(f"{base_url}/api/scan?t={int(time.time())}", timeout=8)
        if r.status_code != 200:
            logger.warning(f"API returned status {r.status_code}")
            return
        
        data = r.json()
        breakouts = data.get("breakouts", [])
        breakdowns = data.get("breakdowns", [])
        
        all_candidates = []
        for b in breakouts:
            b["_mode"] = "BULLISH"
            all_candidates.append(b)
        for bd in breakdowns:
            bd["_mode"] = "BEARISH"
            all_candidates.append(bd)
            
        for item in all_candidates:
            sym = item.get("symbol")
            if not sym or sym in DISPATCHED_TODAY:
                continue
                
            dist = item.get("pct_dist", 99)
            rvol = item.get("rvol", 1.0)
            rsi = item.get("rsi", 50)
            mode = item.get("_mode")
            
            # Check Fresh A+ Conditions
            is_bull = (mode == "BULLISH")
            if is_bull:
                is_fresh = (0.0 <= dist <= 2.0)
                is_good = is_fresh and (rvol >= 1.25) and (58 <= rsi <= 82)
            else:
                is_fresh = (dist <= 0.8)
                is_good = is_fresh and (rvol >= 1.25)
                
            if is_good:
                DISPATCHED_TODAY.add(sym)
                emoji = "🎯" if is_bull else "🩸"
                opt_type = "CE" if is_bull else "PE"
                action = "CALL (CE) OPTION" if is_bull else "PUT (PE) OPTION"
                cname = item.get("company_name", sym)
                st = item.get("stock_trade", {})
                opt = item.get("option_trade", {})
                
                # Fetch Real-Time Angel One 0-Latency Quotes
                angel_data = get_live_angel_quote(sym, option_type=opt_type)
                
                if angel_data and angel_data.get("opt_ltp", 0) > 0:
                    cmp_val = angel_data["spot_ltp"]
                    strike = angel_data["strike_str"]
                    contract = angel_data["contract"]
                    entry = round(angel_data["opt_ltp"], 2)
                    price_badge = "⚡ Angel One Live (0-Latency)"
                else:
                    cmp_val = item.get("cmp")
                    strike = opt.get("strike", "ATM")
                    contract = opt.get("contract", f"{sym} {strike}")
                    entry = opt.get("entry", 0)
                    price_badge = "NSE BhavCopy EOD"

                # Standard Risk-Managed Math: SL -30%, Target 1 +45%, Target 2 +95%
                sl = round(entry * 0.70, 2)
                tgt1 = round(entry * 1.45, 2)
                tgt2 = round(entry * 1.95, 2)
                lot = opt.get("lot_size", 100)
                margin = round(entry * lot)
                
                t1_gain = round((tgt1 - entry) * lot)
                t2_gain = round((tgt2 - entry) * lot)
                
                msg = (
                    f"{emoji} *VICKYVAIO BREAKOUT SIGNAL: {sym}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• *Company:* {cname}\n"
                    f"• *Feed:* {price_badge}\n"
                    f"• *Setup:* {item.get('setup_name', 'Breakout')} (A+ High Conviction)\n"
                    f"• *Spot CMP:* ₹{cmp_val} | SL: ₹{st.get('sl')} | Tgt: ₹{st.get('tgt1')}\n"
                    f"• *{action}:* `{contract}` ({strike})\n"
                    f"• *Live Premium Entry:* ₹{entry}\n"
                    f"• *Stop-Loss (-30%):* ₹{sl}\n"
                    f"• *Target 1 (+45%):* ₹{tgt1} (+₹{t1_gain:,})\n"
                    f"• *Target 2 (+95% Doubler):* ₹{tgt2} (+₹{t2_gain:,})\n"
                    f"• *Lot Size:* {lot} | *Margin Req:* ₹{margin:,}\n"
                    f"• *Volume Surge:* {rvol}x RVOL | *RSI:* {rsi}\n"
                    f"• *Execution Rule:* Buy with LIMIT order at ₹{entry}. Book 50% at T1, trail SL to cost.\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 [Open Live Chart](https://pro-stock-fno-scanner.vercel.app)"
                )
                
                logger.info(f"[TRIGGERED A+] {sym} ({action} {strike} @ Rs.{entry}) -> Dispatching to Telegram...")
                ok = send_telegram_alert(msg)
                if ok:
                    logger.info(f"[SUCCESS] Dispatched {sym} to Telegram Chat {CHAT_ID}!")
                else:
                    logger.error(f"[FAILED] Failed to dispatch {sym}")
                    
    except Exception as e:
        logger.error(f"Scan cycle error: {e}")

def main():
    force = "--force" in sys.argv
    print("=" * 65)
    print(" VICKYVAIO BREAKOUTS - REAL-TIME TELEGRAM F&O SIGNAL SCANNER")
    print(f" Connected Bot Token: {BOT_TOKEN[:12]}...")
    print(f" Connected Chat ID: {CHAT_ID}")
    print(" Real-Time Feed: Angel One SmartAPI (TOTP Active)")
    print(" Schedule: 9:15 AM - 2:30 PM IST (Mon-Fri)")
    print("=" * 65)
    
    # Initialize Angel One and Scrip Master
    init_angel_one()
    load_scrip_master()
    
    if force:
        logger.info("[TEST MODE] --force flag detected. Scanning immediately...")
    else:
        logger.info("Standing by for market hours (9:15 AM - 2:30 PM IST). Use --force to test right now.")
        
    while True:
        if is_market_hours(force):
            run_scanner_cycle()
        else:
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            logger.info(f"[{now_str}] Outside market hours (9:15 AM - 2:30 PM IST). Standing by...")
        time.sleep(60)

if __name__ == "__main__":
    main()
