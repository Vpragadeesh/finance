from typing import List, Dict
import json
import os
from datetime import datetime


def calculate_pegy(pe: float, profit_growth: float, dividend_yield: float, buffer: float = 0.1):

    denominator = profit_growth + dividend_yield + buffer

    if pe <= 0 or denominator <= 0:
        return None

    return round(pe / denominator, 4)


def calculate_pegy_for_stocks(stocks: List[Dict]):
    """
    Calculate PEGY for a list of stocks.
    """
    print(f"{'Company':<25} {'P/E':>8} {'Growth%':>10} {'Div%':>8} {'PEGY':>10}")
    print("-" * 65)

    for stock in stocks:
        pegy = calculate_pegy(
            stock["pe"],
            stock["growth"],
            stock["dividend"]
        )

        pegy_display = pegy if pegy is not None else "N/A"

        print(
            f"{stock['name']:<25} "
            f"{stock['pe']:>8.2f} "
            f"{stock['growth']:>10.2f} "
            f"{stock['dividend']:>8.2f} "
            f"{str(pegy_display):>10}"
        )


def main():
    # Find the latest JSON output file
    json_files = [f for f in os.listdir(".") if f.startswith("pegy_output_") and f.endswith(".json")]
    
    if not json_files:
        print("No JSON file found. Please run ex.py first to generate pegy_output_YYYY-MM-DD.json")
        return
    
    latest_json = sorted(json_files)[-1]
    
    with open(latest_json, "r") as f:
        data = json.load(f)
    
    # Transform JSON data to stock format
    stocks = []
    for item in data:
        if item["pe_ratio"] is not None and item["net_profit_growth_yoy"] is not None and item["dividend_yield"] is not None:
            stocks.append({
                "name": item["symbol"],
                "pe": item["pe_ratio"],
                "growth": item["net_profit_growth_yoy"],
                "dividend": item["dividend_yield"]
            })
    
    print(f"Loaded {len(stocks)} stocks from {latest_json}\n")
    calculate_pegy_for_stocks(stocks)


if __name__ == "__main__":
    main()
