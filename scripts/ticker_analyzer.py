#!/usr/bin/env python3
"""
PortDive Workbook Ticker Analyzer
---------------------------------
Recursively scans the workbook's investment theses (`theses/*/THESIS.md`), extracts
all tradable proxies and health basket tickers, cleans and normalizes identifiers
(symbols, exchanges, ISINs, and WKNs), and cross-references them against the
live PortDive database via `pd ticker resolve` to identify existing vs missing tickers.

Usage:
  python3 scripts/ticker_analyzer.py --root ./theses --output ./scripts/outputs/analyzer_report.json --check-db
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
    # Replace invalid values with empty string
    if cleaned.upper() in ["N/A", "N/A.", "VERIFY", "(VERIFY)", "VERIFY BEFORE TRADE", "NONE", "—", "-"]:
        return ""
    return cleaned

def parse_exchange_symbol(asset_dict):
    symbol = ""
    exchange = ""
    
    # Try typical table keys
    for k in ["Exchange Symbol", "Exchange", "TSE", "Listing"]:
        if k in asset_dict and asset_dict[k]:
            val = clean(asset_dict[k])
            if not val:
                continue
            
            # Check for colon like "NYSE: HIMS"
            if ":" in val:
                parts = val.split(":")
                exchange = parts[0].strip()
                symbol = parts[1].strip()
            # Check if TSE code (e.g. 2802 or 3110)
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

def extract_tables_from_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.split("\n")
    table_lines = []
    in_table = False
    tables = []
    
    for line in lines:
        if "|" in line:
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        else:
            if in_table:
                if len(table_lines) >= 3:
                    tables.append(table_lines)
                in_table = False
                table_lines = []
    if in_table and len(table_lines) >= 3:
        tables.append(table_lines)
        
    extracted = []
    for table in tables:
        header = [col.strip() for col in table[0].split("|")[1:-1]]
        lower_header = [h.lower() for h in header]
        if not any(k in lower_header for k in ['isin', 'wkn']):
            continue
            
        for row in table[2:]:
            cols = [col.strip() for col in row.split("|")[1:-1]]
            if len(cols) < len(header):
                continue
            row_dict = dict(zip(header, cols))
            extracted.append(row_dict)
            
    return extracted

def query_ticker_resolve(symbol, exchange, isin):
    # Try resolving by ISIN first
    if isin:
        try:
            cmd = f"pd ticker resolve --isin \"{isin}\" --json"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                parsed = json.loads(res.stdout.strip())
                return True, parsed.get("instrument_id"), f"ISIN {isin}"
        except:
            pass
            
    # Try resolving by symbol + exchange
    if symbol and exchange:
        try:
            cmd = f"pd ticker resolve --exchange \"{exchange}\" \"{symbol}\" --json"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                parsed = json.loads(res.stdout.strip())
                return True, parsed.get("instrument_id"), f"Symbol/Exchange {symbol}/{exchange}"
        except:
            pass
            
    return False, None, ""

def main():
    parser = argparse.ArgumentParser(description="Analyze PortDive workbook theses to identify missing tickers.")
    parser.add_argument("--root", default="./theses", help="Path to the theses folder.")
    parser.add_argument("--output", default="./scripts/outputs/analyzer_report.json", help="Path to export the structured JSON report.")
    parser.add_argument("--check-db", action="store_true", help="Cross-reference extracted tickers against live PortDive database.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.root):
        print(f"Error: Root folder '{args.root}' does not exist.")
        sys.exit(1)
        
    print(f"Scanning '{args.root}' for THESIS.md files...")
    
    all_proxies = []
    for root, dirs, files in os.walk(args.root):
        for file in files:
            if file == "THESIS.md":
                file_path = os.path.join(root, file)
                slug = os.path.basename(root)
                try:
                    proxies = extract_tables_from_markdown(file_path)
                    for p in proxies:
                        p["thesis"] = slug
                        p["file"] = file_path
                    all_proxies.extend(proxies)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    print(f"Extracted {len(all_proxies)} raw ticker definitions.")
    
    results = []
    seen = set()
    
    for item in all_proxies:
        isin = clean(item.get("ISIN", ""))
        wkn = clean(item.get("WKN", ""))
        ticker_wkn = item.get("Ticker / WKN", "")
        
        if ticker_wkn:
            parts = clean(ticker_wkn).split("/")
            if len(parts) == 2:
                wkn = parts[1].strip()
                
        symbol, exchange = parse_exchange_symbol(item)
        if ticker_wkn and not symbol:
            parts = clean(ticker_wkn).split("/")
            if len(parts) >= 1:
                symbol = parts[0].strip()
                
        asset_name = clean(item.get("Asset", ""))
        
        if not symbol and not isin:
            continue
            
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
                
        # Deduplicate
        key = (isin.upper(), wkn.upper(), symbol.upper(), exchange.upper() if exchange else "")
        if key in seen:
            continue
        seen.add(key)
        
        existing = False
        existing_id = None
        match_reason = ""
        
        if args.check_db:
            existing, existing_id, match_reason = query_ticker_resolve(symbol, exchange, isin)
            
        results.append({
            "asset_name": asset_name,
            "symbol": symbol,
            "exchange": exchange,
            "isin": isin,
            "wkn": wkn,
            "thesis": item.get("thesis"),
            "existing": existing,
            "match_reason": match_reason,
            "existing_id": existing_id
        })
        
    # Ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nAnalysis Report exported to '{args.output}'")
    print(f"Total Unique Tickers Checked: {len(results)}")
    if args.check_db:
        print(f"  Existing in Database: {sum(1 for x in results if x['existing'])}")
        print(f"  Missing from Database: {sum(1 for x in results if not x['existing'])}")

if __name__ == "__main__":
    main()
