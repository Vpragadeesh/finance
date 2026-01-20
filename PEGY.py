from typing import List, Dict


def calculate_pegy(pe: float, profit_growth: float, dividend_yield: float, buffer: float = 0.1):
    """
    Calculate PEGY ratio safely.

    pe               : Price to Earnings ratio
    profit_growth    : Profit growth percentage (e.g. 15 for 15%)
    dividend_yield   : Dividend yield percentage (e.g. 2.5 for 2.5%)
    buffer           : Small value to avoid division by zero

    returns          : PEGY value (float) or None if invalid
    """
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
    # Example stock data (replace / extend this)
    stocks = [
        {
            "name": "Bank of Baroda",
            "pe": 8.26,
            "growth": 89.06,
            "dividend": 2.72
        },
        {
            "name": "ITC",
            "pe": 22.50,
            "growth": 10.20,
            "dividend": 3.10
        }
        {
            "name": 
        }
    ]

    calculate_pegy_for_stocks(stocks)


if __name__ == "__main__":
    main()
