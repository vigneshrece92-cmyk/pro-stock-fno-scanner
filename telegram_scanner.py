"""
Vickyvaio Breakouts - Automated Telegram F&O Signal Scanner
Continuous Institutional Scanner (9:15 AM - 2:30 PM IST)
"""

import time
import datetime
import requests
import sys

BOT_TOKEN = "7031852910:AAGkhuuDnuvAYY_llzuBryJQ_uAod9ekFk4"
CHAT_ID = "927756502"

DISPATCHED_TODAY = set()

def send_telegram_alert(message: str) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID),
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=8)
        return r.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")
        return False

def is_market_hours(force=False) -> bool:
    if force:
        return True
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    # IST is UTC + 5:30
    ist_min = (now_utc.hour * 60 + now_utc.minute + 330) % 1440
    # Monday = 0, Friday = 4
    weekday = (now_utc.weekday())
    # 9:15 AM (555 min) to 2:30 PM (870 min)
    return (weekday < 5) and (555 <= ist_min <= 870)

def run_scanner_cycle(base_url="https://pro-stock-fno-scanner.vercel.app"):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Polling verified breakout & breakdown feeds...")
    try:
        r = requests.get(f"{base_url}/api/scan?t={int(time.time())}", timeout=8)
        if r.status_code != 200:
            print(f"  API returned status {r.status_code}")
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
                action = "CALL (CE) OPTION" if is_bull else "PUT (PE) OPTION"
                cname = item.get("company_name", sym)
                st = item.get("stock_trade", {})
                opt = item.get("option_trade", {})
                
                strike = opt.get("strike", "ATM")
                entry = opt.get("entry", 0)
                sl = opt.get("sl", 0)
                tgt1 = opt.get("tgt1", 0)
                tgt2 = opt.get("tgt2", 0)
                lot = opt.get("lot_size", 100)
                margin = opt.get("margin_required", 15000)
                
                t1_gain = round((tgt1 - entry) * lot)
                t2_gain = round((tgt2 - entry) * lot)
                
                msg = (
                    f"{emoji} *VICKYVAIO BREAKOUT SIGNAL: {sym}*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• *Company:* {cname}\n"
                    f"• *Setup:* {item.get('setup_name', 'Breakout')} (A+ High Conviction)\n"
                    f"• *Spot CMP:* ₹{item.get('cmp')} | SL: ₹{st.get('sl')} | Tgt: ₹{st.get('tgt1')}\n"
                    f"• *{action}:* {sym} {strike}\n"
                    f"• *Premium Entry:* ₹{entry}\n"
                    f"• *Stop-Loss (-30%):* ₹{sl}\n"
                    f"• *Target 1 (+45%):* ₹{tgt1} (+₹{t1_gain:,})\n"
                    f"• *Target 2 (+95% Doubler):* ₹{tgt2} (+₹{t2_gain:,})\n"
                    f"• *Lot Size:* {lot} | *Margin Req:* ₹{margin:,}\n"
                    f"• *Volume Surge:* {rvol}x RVOL | *RSI:* {rsi}\n"
                    f"• *Execution Rule:* Buy with LIMIT order at ₹{entry}. Book 50% at T1, trail SL to cost.\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 [Open Live Chart](https://pro-stock-fno-scanner.vercel.app)"
                )
                
                print(f"  ⚡ TRIGGERED A+ SIGNAL: {sym} ({action} {strike}) -> Dispatching to Telegram...")
                ok = send_telegram_alert(msg)
                if ok:
                    print(f"  ✓ Dispatched {sym} to Telegram Chat {CHAT_ID} successfully!")
                else:
                    print(f"  ✗ Failed to dispatch {sym}")
                    
    except Exception as e:
        print(f"  Scan cycle error: {e}")

def main():
    force = "--force" in sys.argv
    print("=" * 60)
    print(" VICKYVAIO BREAKOUTS - TELEGRAM F&O SIGNAL SCANNER")
    print(f" Connected Bot Token: {BOT_TOKEN[:12]}...")
    print(f" Connected Chat ID: {CHAT_ID}")
    print(" Schedule: 9:15 AM - 2:30 PM IST (Mon-Fri)")
    print("=" * 60)
    
    if force:
        print("⚡ [TEST MODE] --force flag detected. Scanning immediately...")
    else:
        print("⏳ Waiting for market hours (9:15 AM - 2:30 PM IST). Use --force to test right now.")
        
    while True:
        if is_market_hours(force):
            run_scanner_cycle()
        else:
            now_str = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now_str}] Outside market hours (9:15 AM - 2:30 PM IST). Standing by...")
        time.sleep(60)

if __name__ == "__main__":
    main()
