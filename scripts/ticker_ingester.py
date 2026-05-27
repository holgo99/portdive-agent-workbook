#!/usr/bin/env python3
"""
PortDive Workbook Ticker Ingester
---------------------------------
Consumes the JSON report from the Ticker Analyzer, filters for tickers that are
missing in the database, automatically applies known workbook corrections (such as
the Salomon running shoe ISIN and WKN typos), programmatically registers the instruments
via `pd ticker create`, and validates the gRPC resolution immediately.

Usage:
  python3 scripts/ticker_ingester.py --input ./scripts/outputs/analyzer_report.json --dry-run
"""

import sys
import json
import argparse
import subprocess

# Known workbook discrepancies and their canonical corrections
CANONICAL_OVERRIDES = {
    # 1. TOWA Corp ISIN Typo (Originally mapped to Salomon trail running shoe SKU!)
    "JP3596800009": {
        "isin": "JP3555700008",
        "wkn": "904022",
        "name": "Towa Corporation",
        "symbol": "6315",
        "exchange": "TSE"
    },
    # 2. Kokusai Electric ISIN Typo
    "JP3283470000": {
        "isin": "JP3293330001",
        "wkn": "A3D8M3",
        "name": "Kokusai Electric Corporation",
        "symbol": "6525",
        "exchange": "TSE"
    },
    # 3. Vistra WKN Typo
    "US92840M1027": {
        "isin": "US92840M1027",
        "wkn": "A2DJE5",
        "name": "Vistra Corp.",
        "symbol": "VST",
        "exchange": "NYSE"
    },
    # 4. Astera Labs ISIN/WKN Typos
    "US04634X1019": {
        "isin": "US04626A1034",
        "wkn": "A404AF",
        "name": "Astera Labs, Inc.",
        "symbol": "ALAB",
        "exchange": "NASDAQ"
    },
    # 5. Silicon Motion WKN Typo
    "US82706C1080": {
        "isin": "US82706C1080",
        "wkn": "A0ETU4",
        "name": "Silicon Motion Technology Corporation",
        "symbol": "SIMO",
        "exchange": "NASDAQ"
    }
}

# Override by symbol also in case ISIN is missing or different
SYMBOL_OVERRIDES = {
    "ALAB": {"isin": "US04626A1034", "wkn": "A404AF", "name": "Astera Labs, Inc."},
    "6315": {"isin": "JP3555700008", "wkn": "904022", "name": "Towa Corporation"},
    "6525": {"isin": "JP3293330001", "wkn": "A3D8M3", "name": "Kokusai Electric Corporation"},
    "VST": {"wkn": "A2DJE5", "name": "Vistra Corp."},
    "SIMO": {"wkn": "A0ETU4", "name": "Silicon Motion Technology Corporation"},
    "ATS": {"name": "AT&S Austria Technologie & Systemtechnik AG"},
    "BE": {"name": "Bloom Energy Corporation"},
    "DLS": {"name": "Delta Electronics (Thailand) PCL"},
    "SOI": {"name": "Soitec S.A."},
    "36BZ": {"name": "iShares MSCI China A UCITS ETF"},
    "LPK": {"name": "LPKF Laser & Electronics SE"},
    "6981": {"name": "Murata Manufacturing Co., Ltd."},
    "6762": {"name": "TDK Corporation"},
    "SMSN": {"name": "Samsung Electronics Co., Ltd. GDR"},
    "6976": {"name": "Taiyo Yuden Co., Ltd."},
    "MDB": {"name": "MongoDB, Inc."},
    "4182": {"name": "Mitsubishi Gas Chemical Company, Inc."},
    "6752": {"name": "Panasonic Holdings Corporation"},
    "2802": {"name": "Ajinomoto Co., Inc."},
    "3110": {"name": "Nitto Boseki Co., Ltd."}
}

def run_command(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"Exit code {e.returncode}: {e.stderr.strip()}"

def apply_overrides(item):
    isin = item.get("isin", "")
    symbol = item.get("symbol", "")
    
    # 1. Check ISIN overrides
    if isin and isin.upper() in CANONICAL_OVERRIDES:
        o = CANONICAL_OVERRIDES[isin.upper()]
        item["isin"] = o["isin"]
        item["wkn"] = o["wkn"]
        item["name"] = o["name"]
        item["symbol"] = o["symbol"]
        item["exchange"] = o["exchange"]
        item["override_applied"] = "ISIN override"
        return
        
    # 2. Check Symbol overrides
    if symbol and symbol.upper() in SYMBOL_OVERRIDES:
        o = SYMBOL_OVERRIDES[symbol.upper()]
        if "isin" in o:
            item["isin"] = o["isin"]
        if "wkn" in o:
            item["wkn"] = o["wkn"]
        if "name" in o:
            item["name"] = o["name"]
        item["override_applied"] = "Symbol override"

def main():
    parser = argparse.ArgumentParser(description="Programmatically register missing workbook tickers.")
    parser.add_argument("--input", default="./scripts/outputs/analyzer_report.json", help="Path to the Ticker Analyzer report.")
    parser.add_argument("--dry-run", action="store_true", help="Display the planned CLI commands without executing.")
    parser.add_argument("--verify-only", action="store_true", help="Only verify/resolve existing instruments.")
    
    args = parser.parse_args()
    
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading report file: {e}")
        sys.exit(1)
        
    missing = [x for x in data if not x.get("existing")]
    
    if args.verify_only:
        print(f"Starting verification-only check on {len(data)} tickers...")
        for idx, t in enumerate(data, 1):
            apply_overrides(t)
            isin = t.get("isin")
            symbol = t.get("symbol")
            exchange = t.get("exchange")
            
            # Resolve by ISIN
            cmd = f"pd ticker resolve --isin \"{isin}\""
            success, out = run_command(cmd)
            print(f"[{idx}/{len(data)}] Resolving {t.get('asset_name')} (ISIN {isin}): {'RESOLVED (id=' + out + ')' if success else 'FAILED'}")
        sys.exit(0)
        
    if not missing:
        print("No missing tickers to ingest. Everything is synchronized!")
        sys.exit(0)
        
    print(f"Found {len(missing)} missing tickers. Processing ingestion...")
    if args.dry_run:
        print("--- DRY-RUN MODE ACTIVE ---")
        
    success_count = 0
    fail_count = 0
    
    for idx, t in enumerate(missing, 1):
        apply_overrides(t)
        
        symbol = t.get("symbol")
        exchange = t.get("exchange")
        isin = t.get("isin")
        wkn = t.get("wkn", "")
        name = t.get("name", t.get("asset_name"))
        
        # Build cmd
        cmd = f"pd ticker create --exchange \"{exchange}\" --isin \"{isin}\" --wkn \"{wkn}\" --name \"{name}\" \"{symbol}\""
        
        if args.dry_run:
            print(f"[{idx}/{len(missing)}] PLANNED: {cmd}")
            success_count += 1
        else:
            print(f"[{idx}/{len(missing)}] Executing registry for {name} ({symbol} on {exchange})...")
            success, output = run_command(cmd)
            if success:
                try:
                    parsed = json.loads(output)
                    print(f"    SUCCESS! instrument_id: {parsed.get('instrument_id')}")
                    success_count += 1
                except:
                    print(f"    SUCCESS but returned non-JSON: {output}")
                    success_count += 1
            else:
                print(f"    FAILED: {output}")
                fail_count += 1
                
    print(f"\nIngestion Finished.")
    print(f"Total Processed: {len(missing)}")
    print(f"  Successful/Planned: {success_count}")
    print(f"  Failed: {fail_count}")

if __name__ == "__main__":
    main()
