"""
Vickyvaio Breakouts - Cloud Institutional Telegram Signal Scanner
Runs 100% in GitHub Actions / Cloud (Zero computer dependency)
"""

import sys
import os
import time
import datetime
import json
import logging
from typing import Dict, Optional
import requests
import pyotp

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CloudTelegramScanner")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7031852910:AAGkhuuDnuvAYY_llzuBryJQ_uAod9ekFk4")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "927756502")

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY", "hmnP0Ln2")
ANGEL_CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE", "V54384326")
ANGEL_PIN = os.getenv("ANGEL_PIN", "2305")
ANGEL_TOTP_KEY = os.getenv("ANGEL_TOTP_KEY", "47CUKNA5GCAHYNYZVXVXBQBVKE")

SCRIP_MASTER_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

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
    global smart_api
    try:
        from SmartApi import SmartConnect
        smart_api = SmartConnect(api_key=ANGEL_API_KEY)
        totp = pyotp.TOTP(ANGEL_TOTP_KEY).now()
        session = smart_api.generateSession(ANGEL_CLIENT_CODE, ANGEL_PIN, totp)
        if session.get("status"):
            logger.info("Angel One SmartAPI authenticated successfully in cloud!")
            return True
        else:
            logger.warning(f"Angel One session failed: {session.get('message')}")
            smart_api = None
            return False
    except Exception as e:
        logger.warning(f"Angel One init exception: {e}")
        smart_api = None
        return False

def get_data_dir() -> str:
    d_dir = r"D:\stock_fno_data"
    if os.path.exists(d_dir):
        return d_dir
    return "."

def load_scrip_master():
    global scrips_cache
    data_dir = get_data_dir()
    candidates = [
        os.path.join(data_dir, "scrip_master_cache.json"),
        r"C:\Users\Vicky\.gemini\antigravity\scratch\nifty_angelone_bot\scrip_master_cache.json",
        "scrip_master_cache.json"
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 100000:
            try:
                with open(c, "r", encoding="utf-8") as f:
                    scrips_cache = json.load(f)
                logger.info(f"Loaded {len(scrips_cache)} scrip records from cache ({c}).")
                return True
            except Exception:
                pass

    cache_file = os.path.join(data_dir, "scrip_master_cache.json")
    try:
        logger.info("Downloading latest Scrip Master from Angel One OpenAPI...")
        r = requests.get(SCRIP_MASTER_URL, timeout=30)
        if r.status_code == 200:
            scrips_cache = r.json()
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(scrips_cache, f)
            logger.info(f"Downloaded and cached {len(scrips_cache)} scrip records to {cache_file}.")
            return True
    except Exception as e:
        logger.error(f"Error downloading scrip master: {e}")
    return False

def get_live_angel_quote(sym: str, option_type: str = "CE") -> Optional[Dict]:
    global smart_api, scrips_cache
    if not smart_api or not scrips_cache:
        return None

    try:
        # Enforce rate-limit safe spacing (max ~2.5 req/s)
        time.sleep(0.40)

        # 1. Spot Token Resolution (handles Indices & Equities)
        if sym == "NIFTY":
            eq_token = "99926000"
            eq_symbol = "Nifty 50"
            target_inst = "OPTIDX"
        elif sym == "BANKNIFTY":
            eq_token = "99926009"
            eq_symbol = "Nifty Bank"
            target_inst = "OPTIDX"
        else:
            eq_matches = [s for s in scrips_cache if s.get("symbol") == f"{sym}-EQ" and s.get("exch_seg") == "NSE"]
            if not eq_matches:
                return None
            eq_token = eq_matches[0]["token"]
            eq_symbol = f"{sym}-EQ"
            target_inst = "OPTSTK"

        spot_res = smart_api.ltpData("NSE", eq_symbol, eq_token)
        if spot_res and not spot_res.get("status"):
            msg = str(spot_res.get("message") or "")
            if "exceeding access rate" in msg or spot_res.get("errorcode") in ("AB8050", "AB8051"):
                logger.warning(f"Rate limit detected for {sym}: {msg}. Backing off 2.5s...")
                time.sleep(2.5)

        spot_ltp = spot_res.get("data", {}).get("ltp", 0.0) if spot_res and spot_res.get("status") else 0.0

        if spot_ltp <= 0:
            return None

        # 2. Options Resolution
        pool = [s for s in scrips_cache if s.get("name") == sym and s.get("exch_seg") == "NFO" and s.get("instrumenttype") == target_inst]
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

        def parse_strike(s):
            try:
                return float(s.get("strike", 0.0)) / 100.0
            except Exception:
                return 999999.0

        best_contract = min(typed_pool, key=lambda s: abs(parse_strike(s) - spot_ltp))
        strike_val = parse_strike(best_contract)
        opt_token = best_contract["token"]
        opt_symbol = best_contract["symbol"]

        # Enforce rate-limit safe spacing for option quote call
        time.sleep(0.40)
        opt_res = smart_api.ltpData("NFO", opt_symbol, opt_token)
        if opt_res and not opt_res.get("status"):
            msg = str(opt_res.get("message") or "")
            if "exceeding access rate" in msg or opt_res.get("errorcode") in ("AB8050", "AB8051"):
                logger.warning(f"Rate limit detected for option {opt_symbol}: {msg}. Backing off 2.5s...")
                time.sleep(2.5)

        opt_ltp = opt_res.get("data", {}).get("ltp", 0.0) if opt_res and opt_res.get("status") else 0.0

        return {
            "spot_ltp": spot_ltp,
            "strike_str": f"{strike_val:g} {option_type}",
            "contract": opt_symbol,
            "opt_ltp": opt_ltp,
            "opt_token": opt_token,
            "expiry": nearest_exp_str
        }
    except Exception as e:
        logger.warning(f"Angel One quote exception for {sym}: {e}")
        return None

def run_cloud_scan():
    logger.info("Executing Cloud Scan Cycle from live Vercel endpoint...")
    base_url = "https://pro-stock-fno-scanner.vercel.app"
    try:
        r = requests.get(f"{base_url}/api/scan?t={int(time.time())}", timeout=25)
        if r.status_code != 200:
            logger.error(f"Failed to fetch scanner API: {r.status_code}")
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

        # Track alerted symbols to prevent duplicate spam in cloud
        alert_history_file = os.path.join(get_data_dir(), "dispatched_today.json")
        dispatched = set()
        today_str = datetime.date.today().isoformat()
        if os.path.exists(alert_history_file):
            try:
                with open(alert_history_file, "r") as f:
                    history = json.load(f)
                    if history.get("date") == today_str:
                        dispatched = set(history.get("symbols", []))
            except Exception:
                pass

        nifty_info = data.get("nifty", {})
        nifty_change = nifty_info.get("change_pct", 0.0)
        nifty_cmp = nifty_info.get("cmp", 24500)
        # Check NIFTY Index Sniper Setup
        if "NIFTY" not in dispatched:
            n_price = nifty_info.get("cmp", nifty_info.get("price", 25030.35))
            n_change = nifty_info.get("change_pct", nifty_info.get("pct_change", 0.0))
            n_ema = nifty_info.get("ema20", 23393.14)
            is_nifty_bull = (n_price >= n_ema) and (n_change >= 0.15)
            is_nifty_bear = (n_price < n_ema) and (n_change <= -0.15)

            if is_nifty_bull or is_nifty_bear:
                n_atm = round(n_price / 50) * 50
                n_type = "CE" if is_nifty_bull else "PE"
                n_emoji = "🎯" if is_nifty_bull else "🩸"
                n_contract = f"NIFTY {n_atm} {n_type}"

                n_angel = get_live_angel_quote("NIFTY", option_type=n_type)
                if n_angel and n_angel.get("opt_ltp", 0) > 0:
                    n_entry = round(n_angel["opt_ltp"], 1)
                else:
                    n_entry = round(n_price * 0.0050, 1)

                n_sl = round(n_entry * 0.70, 1)
                n_t1 = round(n_entry * 1.45, 1)
                n_t2 = round(n_entry * 1.95, 1)
                n_lot = 65
                n_capital = round(n_entry * n_lot)

                n_msg = (
                    f"{n_emoji} *{n_contract}* (NIFTY SNIPER)\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"• *Buy Limit:* ₹{n_entry}\n"
                    f"• *Stop-Loss:* ₹{n_sl} (-30%)\n"
                    f"• *Target 1:* ₹{n_t1} (+45%)\n"
                    f"• *Target 2:* ₹{n_t2} (+95% Doubler)\n"
                    f"• *Lot:* {n_lot} | *Capital:* ₹{n_capital:,}\n"
                    f"• *Setup:* 20 EMA + Camarilla Confluence\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 [Terminal](https://pro-stock-fno-scanner.vercel.app)"
                )
                logger.info(f"Dispatching NIFTY Sniper Alert to Telegram: {n_contract}")
                send_telegram_alert(n_msg)
                dispatched.add("NIFTY")

        dispatched_count = 0
        for item in all_candidates:
            sym = item.get("symbol")
            if not sym or sym in dispatched:
                continue

            dist = item.get("pct_dist", 99)
            rvol = item.get("rvol", 1.0)
            rsi = item.get("rsi", 50)
            mode = item.get("_mode")

            is_bull = (mode == "BULLISH")
            if is_bull:
                # -0.5% to +3.5%: Pre-breakout coils up to fast 5-min explosive movers (captures TITAN, HDFCBANK, etc.)
                is_fresh = (-0.5 <= dist <= 3.5)
                is_good = is_fresh and (rvol >= 1.25) and (58 <= rsi <= 82)
            else:
                # <= 2.5%: Decoupled & momentum breakdown drops (captures ASTRAL, SUPREMEIND, etc.)
                is_fresh = (dist <= 2.5)
                is_good = is_fresh and (rvol >= 1.25)

            if is_good:
                dispatched.add(sym)
                dispatched_count += 1
                emoji = "🎯" if is_bull else "🩸"
                opt_type = "CE" if is_bull else "PE"
                action = "CALL (CE) OPTION" if is_bull else "PUT (PE) OPTION"
                cname = item.get("company_name", sym)
                st = item.get("stock_trade", {})
                opt = item.get("option_trade", {})

                # Check Live Angel One quote
                angel_data = get_live_angel_quote(sym, option_type=opt_type)
                if angel_data and angel_data.get("opt_ltp", 0) > 0:
                    cmp_val = angel_data["spot_ltp"]
                    strike = angel_data["strike_str"]
                    contract = angel_data["contract"]
                    entry = round(angel_data["opt_ltp"], 2)
                    price_badge = "⚡ Angel One Live (Cloud)"
                else:
                    cmp_val = item.get("cmp")
                    strike = opt.get("strike", "ATM")
                    contract = opt.get("contract", f"{sym} {strike}")
                    entry = opt.get("entry", 0)
                    price_badge = "NSE BhavCopy Verified"

                sl = round(entry * 0.70, 2)
                tgt1 = round(entry * 1.45, 2)
                tgt2 = round(entry * 1.95, 2)
                lot = opt.get("lot_size", 100)
                margin = round(entry * lot)

                t1_gain = round((tgt1 - entry) * lot)
                t2_gain = round((tgt2 - entry) * lot)

                # Analyze Market Trend Alignment vs Independent Decoupled Breakout (like ASTRAL negative news)
                is_aligned = (is_bull and nifty_change >= -0.10) or (not is_bull and nifty_change <= 0.10)
                # Clean, Compact, High-Speed Institutional Signal
                trend_pill = "Aligned 🟢" if is_aligned else "Decoupled ⚡"
                tv_link = f"https://in.tradingview.com/chart/?symbol=NSE:{sym}"
                msg = (
                    f"{emoji} *{sym} {strike}* ({opt_type})\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"• *Buy Limit:* ₹{entry}\n"
                    f"• *Stop-Loss:* ₹{sl} (-30%)\n"
                    f"• *Target 1:* ₹{tgt1} (+45%)\n"
                    f"• *Target 2:* ₹{tgt2} (+95%)\n"
                    f"• *Lot:* {lot} | *Capital:* ₹{margin:,}\n"
                    f"• *Nifty:* {trend_pill} | *Vol:* {rvol}x\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 [Chart]({tv_link}) • [Terminal](https://pro-stock-fno-scanner.vercel.app)"
                )

                logger.info(f"Dispatching Cloud Alert for {sym} to Telegram...")
                send_telegram_alert(msg)

        # Save dispatched history
        with open(alert_history_file, "w") as f:
            json.dump({"date": today_str, "symbols": list(dispatched)}, f)
    except Exception as e:
        logger.error(f"Error during cloud scan cycle: {e}")

def is_market_hours() -> bool:
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # IST is UTC + 5:30
    ist_min = (now_utc.hour * 60 + now_utc.minute + 330) % 1440
    weekday = now_utc.weekday()
    # Monday to Friday: 9:15 AM (555) to 3:30 PM (930)
    return (weekday < 5) and (555 <= ist_min <= 930)

def main():
    force_scan = "--force" in sys.argv or os.getenv("FORCE_SCAN", "0") == "1"
    if not force_scan and not is_market_hours():
        logger.info("Market is currently CLOSED (IST). Scanner standing down until next market session (Mon-Fri 9:15 AM - 3:30 PM IST). Zero alerts sent. Pass --force to run off-market cycle.")
        return

    logger.info("Initializing Angel One SmartAPI and Scrip Master...")
    init_angel_one()
    load_scrip_master()

    start_time = time.time()
    max_duration_seconds = 50 * 60 if not force_scan else 60  # 1 cycle if forced

    logger.info("Starting High-Frequency 60-Second Cloud Radar Loop...")
    while time.time() - start_time < max_duration_seconds:
        if force_scan or is_market_hours():
            run_cloud_scan()
            if force_scan:
                break
        else:
            logger.info("Market closed during active session. Standing down.")
            break

        # Wait 60 seconds before next scan
        time.sleep(60)

    logger.info("Cloud session cycle completed cleanly.")

if __name__ == "__main__":
    main()

