import yfinance as yf
import json
from datetime import datetime

# Stock data - BSE Sensex 30 stocks with their P/E, Growth, and Dividend Yield
STOCKS_DATA = [
    {"symbol": "ADANIENT.NS", "name": "BSE:ADANIENT", "pe": 18.5, "growth": 25.3, "dividend": 1.2},
    {"symbol": "ADANIPORTS.NS", "name": "BSE:ADANIPORTS", "pe": 12.4, "growth": 15.2, "dividend": 2.8},
    {"symbol": "APOLLOHOSP.NS", "name": "BSE:APOLLOHOSP", "pe": 28.6, "growth": 18.5, "dividend": 0.5},
    {"symbol": "ASIANPAINT.NS", "name": "BSE:ASIANPAINT", "pe": 38.2, "growth": 12.3, "dividend": 0.8},
    {"symbol": "AXISBANK.NS", "name": "BSE:AXISBANK", "pe": 14.1, "growth": 20.5, "dividend": 2.5},
    {"symbol": "BAJAJ-AUTO.NS", "name": "BSE:BAJAJ-AUTO", "pe": 15.3, "growth": 10.2, "dividend": 1.8},
    {"symbol": "BAJFINANCE.NS", "name": "BSE:BAJFINANCE", "pe": 16.8, "growth": 22.1, "dividend": 1.5},
    {"symbol": "BAJAJFINSV.NS", "name": "BSE:BAJAJFINSV", "pe": 19.2, "growth": 18.3, "dividend": 2.2},
    {"symbol": "BHARTIARTL.NS", "name": "BSE:BHARTIARTL", "pe": 24.3, "growth": 16.8, "dividend": 1.5},
    {"symbol": "BPCL.NS", "name": "BSE:BPCL", "pe": 8.9, "growth": 12.5, "dividend": 4.2},
    {"symbol": "BRITANNIA.NS", "name": "BSE:BRITANNIA", "pe": 35.7, "growth": 8.2, "dividend": 1.2},
    {"symbol": "CIPLA.NS", "name": "BSE:CIPLA", "pe": 20.4, "growth": 11.3, "dividend": 2.1},
    {"symbol": "COALINDIA.NS", "name": "BSE:COALINDIA", "pe": 10.2, "growth": 8.5, "dividend": 3.8},
    {"symbol": "DIVISLAB.NS", "name": "BSE:DIVISLAB", "pe": 36.5, "growth": 22.1, "dividend": 0.3},
    {"symbol": "DRREDDY.NS", "name": "BSE:DRREDDY", "pe": 42.3, "growth": 14.2, "dividend": 0.8},
    {"symbol": "GRASIM.NS", "name": "BSE:GRASIM", "pe": 20.5, "growth": 13.2, "dividend": 2.5},
    {"symbol": "HDFCBANK.NS", "name": "BSE:HDFCBANK", "pe": 16.2, "growth": 19.3, "dividend": 2.7},
    {"symbol": "HEROMOTOCO.NS", "name": "BSE:HEROMOTOCO", "pe": 21.5, "growth": 13.1, "dividend": 1.9},
    {"symbol": "HINDALCO.NS", "name": "BSE:HINDALCO", "pe": 12.8, "growth": 16.5, "dividend": 2.4},
    {"symbol": "HINDUNILVR.NS", "name": "BSE:HINDUNILVR", "pe": 44.2, "growth": 9.8, "dividend": 1.3},
    {"symbol": "ICICIBANK.NS", "name": "BSE:ICICIBANK", "pe": 15.9, "growth": 21.2, "dividend": 2.6},
    {"symbol": "INDUSINDBK.NS", "name": "BSE:INDUSINDBK", "pe": 13.4, "growth": 18.7, "dividend": 2.8},
    {"symbol": "INFY.NS", "name": "BSE:INFY", "pe": 22.1, "growth": 13.5, "dividend": 1.8},
    {"symbol": "ITC.NS", "name": "BSE:ITC", "pe": 22.5, "growth": 10.2, "dividend": 3.1},
    {"symbol": "JSWSTEEL.NS", "name": "BSE:JSWSTEEL", "pe": 11.3, "growth": 14.8, "dividend": 2.2},
    {"symbol": "KOTAKBANK.NS", "name": "BSE:KOTAKBANK", "pe": 18.7, "growth": 20.1, "dividend": 2.4},
    {"symbol": "LT.NS", "name": "BSE:LT", "pe": 26.4, "growth": 12.3, "dividend": 1.6},
    {"symbol": "M&M.NS", "name": "BSE:M&M", "pe": 14.2, "growth": 17.5, "dividend": 2.1},
    {"symbol": "MARUTI.NS", "name": "BSE:MARUTI", "pe": 16.8, "growth": 15.2, "dividend": 2.3},
    {"symbol": "NESTLEIND.NS", "name": "BSE:NESTLEIND", "pe": 48.5, "growth": 7.2, "dividend": 0.9},
]

def get_today_price(symbol):
    """Fetch current stock price from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        
        if hist.empty:
            return None
        
        return round(float(hist["Close"].iloc[-1]), 2)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def calculate_pegy(pe, growth, dividend, buffer=0.1):
    """Calculate PEGY ratio"""
    if pe is None or growth is None or dividend is None:
        return None
    if pe <= 0:
        return None
    return round(pe / (growth + dividend + buffer), 4)

def main():
    output = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Fetching stock data for {len(STOCKS_DATA)} stocks...\n")

    for stock_info in STOCKS_DATA:
        symbol = stock_info["symbol"]
        
        current_price = get_today_price(symbol)
        
        data = {
            "symbol": stock_info["name"],
            "date": today,
            "current_price": current_price,
            "pe_ratio": stock_info["pe"],
            "net_profit_growth_yoy": stock_info["growth"],
            "dividend_yield": stock_info["dividend"],
            "pegy": calculate_pegy(stock_info["pe"], stock_info["growth"], stock_info["dividend"])
        }
        
        output.append(data)

    output_file = f"pegy_output_Sensex_{today}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nJSON data saved to {output_file}")

if __name__ == "__main__":
    main()
