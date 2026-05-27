#!/usr/bin/env python3
"""
PortDive Workbook Basket Scaffolder
-----------------------------------
Generalized scaffolding utility that recursively climbs the workbook's theses,
resolves identity via `- **Server Thesis:** N`, parses the `## Tradable Proxies` and 
`## Health Basket` sections to map portfolios, dynamically looks up canonical database
`instrument_id`s at runtime, programmatically adds active/health baskets to the server,
and populates all positions with weights, roles, and rationales.

Usage:
  python3 scripts/basket_scaffolder.py --root ./theses --dry-run
"""

import os
import re
import sys
import json
import argparse
import subprocess

def clean(text):
    if not text:
        return ""
    # Strip markdown bold, italics, backticks, spaces
    cleaned = re.sub(r'[*_`]', '', text).strip()
    if cleaned.upper() in ["N/A", "N/A.", "VERIFY", "(VERIFY)", "VERIFY BEFORE TRADE", "NONE", "—", "-"]:
        return ""
    return cleaned

def parse_exchange_symbol(asset_dict):
    symbol = ""
    exchange = ""
    for k in ["Exchange Symbol", "Exchange", "TSE", "Listing"]:
        if k in asset_dict and asset_dict[k]:
            val = clean(asset_dict[k])
            if not val:
                continue
            if ":" in val:
                parts = val.split(":")
                exchange = parts[0].strip()
                symbol = parts[1].strip()
            elif k == "TSE":
                exchange = "TSE"
                symbol = val
            elif k == "Listing":
                if "Xetra" in val or "XETR" in val.upper():
                    exchange = "XETR"
                    symbol = val.replace("Xetra", "").replace("XETR", "").strip()
                else:
                    symbol = val
            elif k == "Exchange":
                if val.startswith("NASDAQ") and len(val) > 6:
                    exchange = "NASDAQ"
                    symbol = val[6:].strip()
                elif val.startswith("NYSE") and len(val) > 4:
                    exchange = "NYSE"
                    symbol = val[4:].strip()
                elif val.startswith("Euronext Paris") and len(val) > 14:
                    exchange = "EPA"
                    symbol = val[14:].strip()
                elif val.startswith("XETR") and len(val) > 4:
                    exchange = "XETR"
                    symbol = val[4:].strip()
                else:
                    exchange = val
            else:
                symbol = val
    asset_name = clean(asset_dict.get("Asset", ""))
    match = re.search(r'\(([^)]+)\)', asset_name)
    if match and not symbol:
        symbol = match.group(1).strip()
    return symbol, exchange

def run_command(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"Exit code {e.returncode}: {e.stderr.strip()}"

def resolve_instrument_id(symbol, exchange, isin):
    # Standardize Exchange Names
    if exchange:
        exchange = exchange.upper()
        if exchange in ["TSE", "TOKYO", "T"]:
            exchange = "TSE"
        elif exchange in ["XETRA", "XETR", "36BZ"]:
            exchange = "XETR"
        elif exchange in ["L&S / SG", "L&S", "SG"]:
            exchange = "XETR"
        elif exchange in ["EURONEXT PARIS", "EURONEXT_PARIS", "SOI.PA"]:
            exchange = "EPA"
            
    # Try resolving by ISIN first
    if isin:
        success, out = run_command(f"pd ticker resolve --isin \"{isin}\" --json")
        if success:
            try:
                return json.loads(out).get("instrument_id")
            except:
                pass
                
    # Try resolving by Symbol + Exchange
    if symbol and exchange:
        success, out = run_command(f"pd ticker resolve --exchange \"{exchange}\" \"{symbol}\" --json")
        if success:
            try:
                return json.loads(out).get("instrument_id")
            except:
                pass
                
    return None

def parse_thesis_id(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'- \*\*Server Thesis:\*\* (\d+)', content)
    if match:
        return int(match.group(1))
    return None

def parse_tables_and_health(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.split("\n")
    sections = {}
    current_section = None
    current_lines = []
    
    for line in lines:
        if line.startswith("## "):
            if current_section:
                sections[current_section] = current_lines
            current_section = clean(line[3:])
            current_lines = []
        elif current_section:
            current_lines.append(line)
    if current_section:
        sections[current_section] = current_lines
        
    proxies = []
    proxies_section = next((sections[k] for k in sections if "Tradable" in k), None)
    if proxies_section:
        table_lines = [line for line in proxies_section if "|" in line]
        if len(table_lines) >= 3:
            header = [col.strip() for col in table_lines[0].split("|")[1:-1]]
            for row in table_lines[2:]:
                cols = [col.strip() for col in row.split("|")[1:-1]]
                if len(cols) < len(header):
                    continue
                proxies.append(dict(zip(header, cols)))
                
    health_items = []
    health_section = next((sections[k] for k in sections if "Health" in k), None)
    if health_section:
        for line in health_section:
            line_clean = line.strip()
            # Match "- **Name (Ticker)** — Rationale" or similar bullet points
            match = re.match(r'[-*]\s+\*\*([^(]+)\(([^)]+)\)\*\*\s+[-—]\s+(.+)', line_clean)
            if match:
                name = match.group(1).strip()
                ident = match.group(2).strip()
                rationale = match.group(3).strip()
                
                symbol = ident
                exchange = ""
                if ":" in ident:
                    parts = ident.split(":")
                    exchange = parts[0].strip()
                    symbol = parts[1].strip()
                elif ident.isdigit():
                    exchange = "TSE" # Default Japanese stocks
                    
                health_items.append({
                    "name": name,
                    "symbol": symbol,
                    "exchange": exchange,
                    "rationale": rationale
                })
                
    return proxies, health_items

def main():
    parser = argparse.ArgumentParser(description="Programmatically build thesis baskets and positions on server.")
    parser.add_argument("--root", default="./theses", help="Path to the theses folder.")
    parser.add_argument("--dry-run", action="store_true", help="Display the planned actions without executing.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.root):
        print(f"Error: Root folder '{args.root}' does not exist.")
        sys.exit(1)
        
    print("Scanning theses and scaffolding server baskets...")
    if args.dry_run:
        print("--- DRY-RUN MODE ACTIVE ---")
        
    for root, dirs, files in os.walk(args.root):
        for file in files:
            if file == "THESIS.md":
                file_path = os.path.join(root, file)
                slug = os.path.basename(root)
                
                thesis_id = parse_thesis_id(file_path)
                if not thesis_id:
                    continue
                    
                print(f"\n==================== PROCESSING THESIS {thesis_id} ({slug}) ====================")
                
                proxies, health = parse_tables_and_health(file_path)
                
                # Setup Baskets to create
                baskets_to_create = []
                
                # Active Proxies Basket
                if proxies:
                    items = []
                    for p in proxies:
                        symbol, exchange = parse_exchange_symbol(p)
                        weight_raw = clean(p.get("Weight", "0"))
                        weight = float(weight_raw.replace("%", "").strip()) if weight_raw else 0.0
                        isin = clean(p.get("ISIN", ""))
                        role = clean(p.get("Strategic Role", "CORE"))
                        
                        items.append({
                            "symbol": symbol,
                            "exchange": exchange,
                            "isin": isin,
                            "weight_pct": weight,
                            "role": "CORE",
                            "rationale": role
                        })
                    
                    baskets_to_create.append({
                        "name": "Core Proxies",
                        "allocation_pct": 100.0,
                        "description": "Active portfolio allocations targeting the primary physical and chemical bottlenecks.",
                        "items": items
                    })
                    
                # Watchlist Health Basket
                if health:
                    items = []
                    for h in health:
                        items.append({
                            "symbol": h["symbol"],
                            "exchange": h["exchange"],
                            "isin": "",
                            "weight_pct": 0.0,
                            "role": "WATCHLIST",
                            "rationale": h["rationale"]
                        })
                    
                    baskets_to_create.append({
                        "name": "Health Basket",
                        "allocation_pct": 0.0,
                        "description": "Non-tradable industry leaders and KPIs used to validate upstream demand signals.",
                        "items": items
                    })
                    
                for basket in baskets_to_create:
                    bname = basket["name"]
                    bpct = basket["allocation_pct"]
                    bdesc = basket["description"]
                    
                    print(f"Creating basket '{bname}' ({bpct}%)...")
                    
                    cmd_basket = f"pd basket add --thesis {thesis_id} --name \"{bname}\" --allocation-pct {bpct} --description \"{bdesc}\" --json"
                    
                    if args.dry_run:
                        print(f"  PLANNED: {cmd_basket}")
                        basket_id = "BASKET_ID_DRYRUN"
                    else:
                        success, out = run_command(cmd_basket)
                        if success:
                            try:
                                basket_id = json.loads(out).get("id")
                                print(f"  SUCCESS! Created basket: {basket_id}")
                            except:
                                print(f"  SUCCESS but failed to parse ID: {out}")
                                continue
                        else:
                            print(f"  FAILED to create basket: {out}")
                            continue
                            
                    for item in basket["items"]:
                        symbol = item["symbol"]
                        exchange = item["exchange"]
                        isin = item["isin"]
                        weight = item["weight_pct"]
                        role = item["role"]
                        rationale = item["rationale"]
                        
                        # Check database ID at runtime
                        instrument_id = resolve_instrument_id(symbol, exchange, isin)
                        
                        print(f"  Adding position {symbol} ({exchange}) [instrument_id={instrument_id}] with weight {weight}%...")
                        
                        cmd_item = f"pd basket items add --symbol \"{symbol}\" --exchange \"{exchange}\" --weight-pct {weight} --role \"{role}\" --rationale \"{rationale}\" {basket_id}"
                        
                        if args.dry_run:
                            print(f"    PLANNED: {cmd_item}")
                        else:
                            success, out = run_command(cmd_item)
                            if success:
                                print(f"    SUCCESS added {symbol}")
                            else:
                                print(f"    FAILED added {symbol}: {out}")

    print("\nBasket scaffolding completed.")

if __name__ == "__main__":
    main()
