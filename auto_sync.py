import concurrent.futures
import csv
import datetime
import io
import json
import requests
import zipfile

symbols = [
    'EICHERMOT', 'GODREJPROP', 'ICICIBANK', 'DIVISLAB', 'MARUTI', 'HEROMOTOCO', 'CIPLA', 
    'BAJAJ-AUTO', 'SBIN', 'HDFCBANK', 'DLF', 'BAJFINANCE', 'TITAN', 'LT', 'PNB', 'M&M', 
    'MUTHOOTFIN', 'TATAPOWER', 'NATIONALUM', 'BANKBARODA', 'TATASTEEL', 'BAJAJFINSV', 
    'WIPRO', 'MOTHERSON', 'RELIANCE', 'TVSMOTOR', 'HINDALCO', 'JSWSTEEL', 'AXISBANK', 
    'KOTAKBANK', 'CHOLAFIN', 'DRREDDY', 'BHARTIARTL', 'VEDL', 'SUNPHARMA', 'HAL', 
    'BPCL', 'TECHM', 'GAIL', 'PERSISTENT', 'JINDALSTEL', 'ITC', 'COFORGE', 'IOC', 'BEL', 'BHEL', 'COALINDIA'
]

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

def fetch_nse_bhavcopy():
    # Try the last 5 trading days until we get the latest published BhavCopy
    for i in range(5):
        d = datetime.date.today() - datetime.timedelta(days=i)
        if d.weekday() >= 5: continue
        d_str = d.strftime('%Y%m%d')
        url = f'https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{d_str}_F_0000.csv.zip'
        try:
            r = session.get(url, timeout=10)
            if r.status_code == 200:
                print(f"Found official NSE BhavCopy for {d_str}")
                z = zipfile.ZipFile(io.BytesIO(r.content))
                csv_name = z.namelist()[0]
                content = z.read(csv_name).decode('utf-8')
                reader = csv.DictReader(io.StringIO(content))
                
                # Group options by symbol and expiry
                raw_by_symbol = {}
                for row in reader:
                    sym = row['TckrSymb']
                    opt_type = row['OptnTp']
                    if opt_type == 'CE':
                        exp = row['XpryDt']
                        strike = float(row['StrkPric'])
                        cls_price = float(row['ClsPric'])
                        last_price = float(row['LastPric'])
                        und_price = float(row['UndrlygPric']) if row['UndrlygPric'] else 0.0
                        oi = int(row['OpnIntrst'])
                        vol = int(row['TtlTradgVol'])
                        lot = int(row['NewBrdLotQty'])
                        actual_price = last_price if last_price > 0 else cls_price
                        
                        if sym not in raw_by_symbol:
                            raw_by_symbol[sym] = {}
                        if exp not in raw_by_symbol[sym]:
                            raw_by_symbol[sym][exp] = []
                        raw_by_symbol[sym][exp].append({
                            'expiry': exp,
                            'strike': strike,
                            'price': actual_price,
                            'spot': und_price,
                            'oi': oi,
                            'vol': vol,
                            'lot': lot,
                            'contract': row['FinInstrmNm']
                        })
                
                # Pick nearest expiry for each stock
                options_by_symbol = {}
                for sym, exp_map in raw_by_symbol.items():
                    sorted_exp = sorted(exp_map.keys())
                    nearest_exp = sorted_exp[0]
                    options_by_symbol[sym] = exp_map[nearest_exp]
                return options_by_symbol
        except Exception as e:
            continue
    return {}

def calculate_rsi(series, period=14):
    if len(series) < period + 1: return 60.0
    deltas = [series[i] - series[i-1] for i in range(1, len(series))]
    gains = [max(d, 0) for d in deltas]
    losses = [max(-d, 0) for d in deltas]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0: return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

COMPANY_NAMES = {
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
}

def get_sector(sym):
    sectors = {
        'EICHERMOT': 'Auto & Ancillary', 'MARUTI': 'Auto & Ancillary', 'HEROMOTOCO': 'Auto & Ancillary',
        'BAJAJ-AUTO': 'Auto & Ancillary', 'M&M': 'Auto & Ancillary', 'TVSMOTOR': 'Auto & Ancillary', 'MOTHERSON': 'Auto & Ancillary',
        'GODREJPROP': 'Realty & Infra', 'DLF': 'Realty & Infra', 'LT': 'Realty & Infra',
        'ICICIBANK': 'Banking & Financials', 'SBIN': 'Banking & Financials', 'HDFCBANK': 'Banking & Financials',
        'BAJFINANCE': 'Banking & Financials', 'PNB': 'Banking & Financials', 'MUTHOOTFIN': 'Banking & Financials',
        'BANKBARODA': 'Banking & Financials', 'BAJAJFINSV': 'Banking & Financials', 'AXISBANK': 'Banking & Financials',
        'KOTAKBANK': 'Banking & Financials', 'CHOLAFIN': 'Banking & Financials',
        'DIVISLAB': 'Pharma & Healthcare', 'CIPLA': 'Pharma & Healthcare', 'DRREDDY': 'Pharma & Healthcare',
        'SUNPHARMA': 'Pharma & Healthcare',
        'TITAN': 'Consumer & Retail', 'ITC': 'Consumer & Retail',
        'TATAPOWER': 'Energy, Power & Telecom', 'BHARTIARTL': 'Energy, Power & Telecom', 'RELIANCE': 'Energy, Power & Telecom',
        'BPCL': 'Defense & PSU', 'GAIL': 'Defense & PSU', 'IOC': 'Defense & PSU', 'BEL': 'Defense & PSU', 'HAL': 'Defense & PSU', 'BHEL': 'Defense & PSU', 'COALINDIA': 'Defense & PSU',
        'NATIONALUM': 'Metals & Mining', 'TATASTEEL': 'Metals & Mining', 'HINDALCO': 'Metals & Mining', 'JSWSTEEL': 'Metals & Mining', 'VEDL': 'Metals & Mining', 'JINDALSTEL': 'Metals & Mining',
        'WIPRO': 'IT & Tech', 'TECHM': 'IT & Tech', 'PERSISTENT': 'IT & Tech', 'COFORGE': 'IT & Tech'
    }
    return sectors.get(sym, 'F&O')

def scan_symbol(s, nse_options):
    try:
        r = session.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}.NS?interval=1d&range=3mo', timeout=5)
        if r.status_code != 200: return None
        res = r.json()['chart']['result'][0]
        meta = res['meta']
        q = res['indicators']['quote'][0]
        
        regular_price = meta.get('regularMarketPrice')
        c = []
        h = []
        l = []
        v = []
        for i in range(len(q['high'])):
            cur_h = q['high'][i]
            cur_l = q['low'][i]
            cur_c = q['close'][i]
            cur_v = q['volume'][i] or 0
            if cur_h is None or cur_l is None: continue
            if cur_c is None: cur_c = regular_price or cur_h
            c.append(cur_c)
            h.append(cur_h)
            l.append(cur_l)
            v.append(cur_v)

        if len(c) < 25: return None
        cmp = regular_price if regular_price else c[-1]
        
        h20 = max(h[-21:-1]) if len(h) >= 21 else max(h[:-1])
        l20 = min(l[-21:-1]) if len(l) >= 21 else min(l[:-1])
        h60 = max(h[-61:-1]) if len(h) >= 61 else max(h[:-1])
        pct_from_high = round(((cmp - h20) / h20) * 100, 2)
        
        k = 2 / 21
        ema20 = c[0]
        for x in c[1:]: ema20 = x * k + ema20 * (1 - k)
        
        avg_vol = sum(v[-21:-1]) / 20.0 if len(v) >= 21 else sum(v) / len(v)
        rvol = round(v[-1] / avg_vol, 2) if avg_vol > 0 else 1.0
        rsi = calculate_rsi(c, 14)

        if pct_from_high >= -0.05:
            stage = "LIVE BREAKOUT"
            score = 96
        elif pct_from_high >= -0.5:
            stage = "IMMINENT PIVOT"
            score = 90
        elif pct_from_high >= -1.2:
            stage = "BASE SQUEEZE"
            score = 84
        else:
            stage = "PRE-BREAKOUT"
            score = 78

        # Pattern identification including Cup & Handle Breakout
        is_cup = False
        if len(c) >= 40:
            l_rim = max(h[-45:-15])
            btm = min(l[-35:-8])
            r_rim = max(h[-15:-3])
            h_low = min(l[-6:-1])
            depth = (l_rim - btm) / l_rim
            rim_diff = abs(l_rim - r_rim) / l_rim
            handle_ratio = (r_rim - h_low) / max((r_rim - btm), 1)
            if 0.08 <= depth <= 0.35 and rim_diff <= 0.06 and handle_ratio <= 0.50 and cmp >= r_rim * 0.985:
                is_cup = True

        if is_cup:
            horizon = "Weekly Holding"
            setup_name = "Cup & Handle Breakout"
            pattern = "Cup & Handle Accumulation"
        elif cmp >= h60 * 0.992:
            horizon = "Monthly Holding"
            setup_name = "Multi-Month Base Breakout (Arvind Mangal)"
            pattern = "Multi-Month Base / Stage-2 Transition"
        elif rvol >= 1.6:
            horizon = "Daily / Intraday"
            setup_name = "High-Beta Momentum Surge (Option Edge)"
            pattern = "High-Volume Range Expansion"
        else:
            horizon = "Weekly Holding"
            setup_name = "Consolidation Pivot Squeeze"
            pattern = "Ascending Base Consolidation"

        # Realistic Breakout Stop Loss and Targets by Time Horizon:
        # Swing traders never place 20% stop loss on a breakout.
        # Daily/Intraday: 2.5% to 3.5% SL -> Target 1: +4% to +5%, Target 2: +7% to +9%
        # Weekly: 3.5% to 4.5% SL -> Target 1: +5.5% to +7%, Target 2: +9% to +12%
        # Monthly Base: 4.5% to 5.5% SL -> Target 1: +7.5% to +9.5%, Target 2: +13% to +16%
        l5 = min(l[-6:-1]) if len(l) >= 6 else l20
        if horizon == "Daily / Intraday":
            sl = round(max(l5, cmp * 0.970), 2)  # max ~3% SL
            risk = max(cmp - sl, cmp * 0.02)
            tgt1 = round(cmp + (risk * 1.5), 2)   # +4.5% to +5%
            tgt2 = round(cmp + (risk * 2.6), 2)   # +7.8% to +9%
        elif horizon == "Weekly Holding":
            sl = round(max(l5, ema20, cmp * 0.960), 2)  # max ~4% SL
            risk = max(cmp - sl, cmp * 0.028)
            tgt1 = round(cmp + (risk * 1.5), 2)   # +6%
            tgt2 = round(cmp + (risk * 2.7), 2)   # +10.5%
        else: # Monthly Holding
            sl = round(max(ema20, cmp * 0.950), 2)  # max ~5% SL
            risk = max(cmp - sl, cmp * 0.035)
            tgt1 = round(cmp + (risk * 1.6), 2)   # +8%
            tgt2 = round(cmp + (risk * 2.8), 2)   # +14%

        tgt1_pct = round(((tgt1 - cmp) / cmp) * 100, 1)
        tgt2_pct = round(((tgt2 - cmp) / cmp) * 100, 1)

        # Match with real NSE option from BhavCopy
        lookup = 'M&M' if s in ['M&M', 'MM'] else s
        best_opt = None
        if lookup in nse_options and nse_options[lookup]:
            opts = sorted(nse_options[lookup], key=lambda x: abs(x['strike'] - cmp))
            best_opt = opts[0]

        if best_opt:
            strike_val = int(best_opt['strike']) if best_opt['strike'] == int(best_opt['strike']) else best_opt['strike']
            actual_prem = round(best_opt['price'], 2)
            lot = best_opt['lot']
            opt_sl = round(actual_prem * 0.70, 1)
            opt_tgt1 = round(actual_prem * 1.45, 1)
            opt_tgt2 = round(actual_prem * 1.95, 1)
            rr = round((opt_tgt1 - actual_prem) / max(actual_prem - opt_sl, 0.1), 1)
            capital = int(round(actual_prem * lot))
            t1_profit = int(round((opt_tgt1 - actual_prem) * lot))
            t2_profit = int(round((opt_tgt2 - actual_prem) * lot))
            option_trade = {
                'strike': f"{strike_val} CE",
                'entry': actual_prem,
                'sl': opt_sl,
                'tgt1': opt_tgt1,
                'tgt2': opt_tgt2,
                'rr': rr,
                'lot_size': lot,
                'margin_required': capital,
                'profit_tgt1': t1_profit,
                'profit_tgt2': t2_profit,
                'contract': best_opt['contract'],
                'source': 'Official NSE BhavCopy'
            }
        else:
            option_trade = {}

        return {
            "symbol": s,
            "company_name": COMPANY_NAMES.get(s, f"{s} Ltd"),
            "cmp": round(cmp, 2),
            "resistance": round(h20, 2),
            "base_floor": round(l20, 2),
            "pct_dist": pct_from_high,
            "stage": stage,
            "score": score,
            "sector": get_sector(s),
            "horizon": horizon,
            "setup_name": setup_name,
            "pattern": pattern,
            "rsi": rsi,
            "rvol": rvol,
            "stock_trade": {
                "entry": round(cmp, 2),
                "sl": sl,
                "tgt1": tgt1,
                "tgt2": tgt2,
                "rr": f"1:{round((tgt1 - cmp) / risk, 1)}",
                "potential_pct": f"+{round(((tgt1 - cmp) / cmp) * 100, 1)}% / +{round(((tgt2 - cmp) / cmp) * 100, 1)}%"
            },
            "option_trade": option_trade
        }
    except Exception as e:
        return None

def run_auto_sync():
    print("Starting automated market scan & official NSE option sync...")
    nse_opts = fetch_nse_bhavcopy()
    print(f"Loaded options for {len(nse_opts)} symbols.")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as ex:
        matches = list(filter(None, ex.map(lambda s: scan_symbol(s, nse_opts), symbols)))
    
    matches.sort(key=lambda x: x['pct_dist'], reverse=True)
    print(f"Scanned {len(matches)} authentic breakouts.")
    
    with open('authentic_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=True)
        
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    clean_json_str = json.dumps(matches, ensure_ascii=True)
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith('VERIFIED_BREAKOUT_DATA ='):
            lines[i] = f'VERIFIED_BREAKOUT_DATA = {clean_json_str}'
            break
            
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Auto-sync completed successfully!")

if __name__ == '__main__':
    run_auto_sync()
