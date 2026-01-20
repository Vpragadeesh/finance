from typing import List, Dict
import json
import os
from datetime import datetime

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


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
    # Find all available JSON output files
    json_files = [f for f in os.listdir(".") if f.startswith("pegy_output_") and f.endswith(".json")]

    # Sort files and display options
    json_files = sorted(json_files, reverse=True)

    print("PEGY Calculator - Select Data Source:\n")

    for idx, filename in enumerate(json_files, 1):
        print(f"{idx}. {filename}")

    print(f"{len(json_files) + 1}. Enter custom stock data (manual)")
    print(f"{len(json_files) + 2}. Fetch LIVE data from Yahoo Finance")
    print(f"{len(json_files) + 3}. Exit")

    # Ask user to select
    while True:
        try:
            choice = input(f"\nSelect option (1-{len(json_files) + 3}): ").strip()
            choice_num = int(choice)

            if choice_num == len(json_files) + 3:
                print("Exiting...")
                return
            elif choice_num == len(json_files) + 2:
                # Live fetch from Yahoo Finance
                stocks = get_live_stocks()
                if stocks:
                    print(f"\nFetched {len(stocks)} stocks from Yahoo Finance\n")
                    calculate_pegy_for_stocks(stocks)
                return
            elif choice_num == len(json_files) + 1:
                # Custom input
                stocks = get_custom_stocks()
                if stocks:
                    print(f"\nLoaded {len(stocks)} custom stocks\n")
                    calculate_pegy_for_stocks(stocks)
                return
            elif 1 <= choice_num <= len(json_files):
                selected_file = json_files[choice_num - 1]
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(json_files) + 3}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Load selected file
    with open(selected_file, "r") as f:
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

    print(f"\nLoaded {len(stocks)} stocks from {selected_file}\n")
    calculate_pegy_for_stocks(stocks)


def fetch_stock_data_from_yfinance(symbol: str) -> Dict:
    """
    Fetch P/E ratio, dividend yield, and earnings growth from Yahoo Finance.
    For Indian stocks, append .NS for NSE or .BO for BSE.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Get P/E ratio
        pe = info.get("trailingPE") or info.get("forwardPE")

        # Get dividend yield
        # Yahoo Finance may return it as decimal (0.0428) or percentage (4.28)
        dividend_yield_raw = info.get("dividendYield")
        if dividend_yield_raw:
            # If value > 1, it's likely already a percentage
            if dividend_yield_raw > 1:
                dividend_yield = dividend_yield_raw
            else:
                dividend_yield = dividend_yield_raw * 100
        else:
            dividend_yield = 0

        # Get earnings growth (already in decimal, convert to percentage)
        earnings_growth_raw = info.get("earningsGrowth") or info.get("earningsQuarterlyGrowth")
        if earnings_growth_raw:
            earnings_growth = earnings_growth_raw * 100
        else:
            # Try to calculate from financials
            earnings_growth = calculate_earnings_growth(stock)

        return {
            "name": info.get("shortName") or symbol,
            "symbol": symbol,
            "pe": round(pe, 2) if pe else None,
            "growth": round(earnings_growth, 2) if earnings_growth else None,
            "dividend": round(dividend_yield, 2) if dividend_yield else 0,
            "price": info.get("currentPrice") or info.get("regularMarketPrice")
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def calculate_earnings_growth(stock) -> float:
    """Calculate earnings growth from historical financials"""
    try:
        financials = stock.financials
        if financials.empty:
            return None

        # Get Net Income row
        if "Net Income" in financials.index:
            net_income = financials.loc["Net Income"]
        elif "Net Income Common Stockholders" in financials.index:
            net_income = financials.loc["Net Income Common Stockholders"]
        else:
            return None

        # Calculate YoY growth
        if len(net_income) >= 2:
            current = net_income.iloc[0]
            previous = net_income.iloc[1]
            if previous and previous != 0:
                growth = ((current - previous) / abs(previous)) * 100
                return growth
        return None
    except Exception:
        return None


def get_live_stocks() -> List[Dict]:
    """Fetch stock data live from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        print("Error: yfinance library not installed. Run: pip install yfinance")
        return []

    stocks = []

    print("\n--- Fetch Live Stock Data from Yahoo Finance ---")
    print("Enter stock symbols (e.g., RELIANCE.NS, TCS.NS, INFY.NS for Indian stocks)")
    print("(Press Enter with empty symbol to finish)\n")

    while True:
        symbol = input("Stock symbol (or press Enter to finish): ").strip().upper()
        if not symbol:
            break

        # Auto-append .NS if no suffix provided for likely Indian stocks
        if not ("." in symbol):
            print(f"  Hint: For Indian NSE stocks, use {symbol}.NS")
            suffix = input(f"  Add suffix? (.NS/.BO/none): ").strip().upper()
            if suffix in [".NS", ".BO"]:
                symbol = symbol + suffix
            elif suffix in ["NS", "BO"]:
                symbol = symbol + "." + suffix

        print(f"  Fetching data for {symbol}...")
        data = fetch_stock_data_from_yfinance(symbol)

        if data:
            if data["pe"] and data["growth"]:
                stocks.append(data)
                print(f"  ✓ {data['name']}: P/E={data['pe']}, Growth={data['growth']}%, Div={data['dividend']}%\n")
            else:
                print(f"  ✗ Incomplete data for {symbol}. PE={data['pe']}, Growth={data['growth']}")
                manual = input("  Enter manually? (y/n): ").strip().lower()
                if manual == 'y':
                    try:
                        pe = float(input(f"    P/E ratio: ") or 0)
                        growth = float(input(f"    Growth %: ") or 0)
                        dividend = float(input(f"    Dividend %: ") or data['dividend'] or 0)
                        stocks.append({
                            "name": data['name'],
                            "pe": pe,
                            "growth": growth,
                            "dividend": dividend
                        })
                        print()
                    except ValueError:
                        print("  Invalid input, skipping.\n")
                print()
        else:
            print(f"  ✗ Could not fetch data for {symbol}\n")

    return stocks


def get_custom_stocks() -> List[Dict]:
    """Allow user to input custom stock data"""
    stocks = []

    print("\n--- Enter Custom Stock Data ---")
    print("(Press Enter with empty company name to finish)\n")

    while True:
        name = input("Company name (or press Enter to finish): ").strip()
        if not name:
            break

        try:
            pe = float(input(f"  P/E ratio for {name}: "))
            growth = float(input(f"  Profit growth % for {name}: "))
            dividend = float(input(f"  Dividend yield % for {name}: "))

            stocks.append({
                "name": name,
                "pe": pe,
                "growth": growth,
                "dividend": dividend
            })
            print()
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")
            continue

    return stocks


if __name__ == "__main__":
    main()
