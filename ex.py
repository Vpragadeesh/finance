import yfinance as yf
import json
from datetime import datetime

# Stock data - Nifty 50 stocks with their P/E, Growth, and Dividend Yield
STOCKS_DATA = [
    {"symbol": "ADANIENT.NS", "name": "NSE:ADANIENT", "pe": 18.5, "growth": 25.3, "dividend": 1.2},
    {"symbol": "ADANIPORTS.NS", "name": "NSE:ADANIPORTS", "pe": 12.4, "growth": 15.2, "dividend": 2.8},
    {"symbol": "APOLLOHOSP.NS", "name": "NSE:APOLLOHOSP", "pe": 28.6, "growth": 18.5, "dividend": 0.5},
    {"symbol": "ASIANPAINT.NS", "name": "NSE:ASIANPAINT", "pe": 38.2, "growth": 12.3, "dividend": 0.8},
    {"symbol": "AXISBANK.NS", "name": "NSE:AXISBANK", "pe": 14.1, "growth": 20.5, "dividend": 2.5},
    {"symbol": "BAJAJ-AUTO.NS", "name": "NSE:BAJAJ-AUTO", "pe": 15.3, "growth": 10.2, "dividend": 1.8},
    {"symbol": "BAJFINANCE.NS", "name": "NSE:BAJFINANCE", "pe": 16.8, "growth": 22.1, "dividend": 1.5},
    {"symbol": "BAJAJFINSV.NS", "name": "NSE:BAJAJFINSV", "pe": 19.2, "growth": 18.3, "dividend": 2.2},
    {"symbol": "BEL.NS", "name": "NSE:BEL", "pe": 22.5, "growth": 14.7, "dividend": 2.1},
    {"symbol": "BPCL.NS", "name": "NSE:BPCL", "pe": 8.9, "growth": 12.5, "dividend": 4.2},
    {"symbol": "BHARTIARTL.NS", "name": "NSE:BHARTIARTL", "pe": 24.3, "growth": 16.8, "dividend": 1.5},
    {"symbol": "BRITANNIA.NS", "name": "NSE:BRITANNIA", "pe": 35.7, "growth": 8.2, "dividend": 1.2},
    {"symbol": "CIPLA.NS", "name": "NSE:CIPLA", "pe": 20.4, "growth": 11.3, "dividend": 2.1},
    {"symbol": "COALINDIA.NS", "name": "NSE:COALINDIA", "pe": 10.2, "growth": 8.5, "dividend": 3.8},
    {"symbol": "DIVISLAB.NS", "name": "NSE:DIVISLAB", "pe": 36.5, "growth": 22.1, "dividend": 0.3},
    {"symbol": "DRREDDY.NS", "name": "NSE:DRREDDY", "pe": 42.3, "growth": 14.2, "dividend": 0.8},
    {"symbol": "EICHERMOT.NS", "name": "NSE:EICHERMOT", "pe": 28.1, "growth": 11.5, "dividend": 1.1},
    {"symbol": "GRASIM.NS", "name": "NSE:GRASIM", "pe": 20.5, "growth": 13.2, "dividend": 2.5},
    {"symbol": "HCLTECH.NS", "name": "NSE:HCLTECH", "pe": 19.8, "growth": 15.4, "dividend": 2.3},
    {"symbol": "HDFCBANK.NS", "name": "NSE:HDFCBANK", "pe": 16.2, "growth": 19.3, "dividend": 2.7},
    {"symbol": "HEROMOTOCO.NS", "name": "NSE:HEROMOTOCO", "pe": 21.5, "growth": 13.1, "dividend": 1.9},
    {"symbol": "HINDALCO.NS", "name": "NSE:HINDALCO", "pe": 12.8, "growth": 16.5, "dividend": 2.4},
    {"symbol": "HINDUNILVR.NS", "name": "NSE:HINDUNILVR", "pe": 44.2, "growth": 9.8, "dividend": 1.3},
    {"symbol": "ICICIBANK.NS", "name": "NSE:ICICIBANK", "pe": 15.9, "growth": 21.2, "dividend": 2.6},
    {"symbol": "INDUSINDBK.NS", "name": "NSE:INDUSINDBK", "pe": 13.4, "growth": 18.7, "dividend": 2.8},
    {"symbol": "INFY.NS", "name": "NSE:INFY", "pe": 22.1, "growth": 13.5, "dividend": 1.8},
    {"symbol": "ITC.NS", "name": "NSE:ITC", "pe": 22.5, "growth": 10.2, "dividend": 3.1},
    {"symbol": "JSWSTEEL.NS", "name": "NSE:JSWSTEEL", "pe": 11.3, "growth": 14.8, "dividend": 2.2},
    {"symbol": "KOTAKBANK.NS", "name": "NSE:KOTAKBANK", "pe": 18.7, "growth": 20.1, "dividend": 2.4},
    {"symbol": "LT.NS", "name": "NSE:LT", "pe": 26.4, "growth": 12.3, "dividend": 1.6},
    {"symbol": "M&M.NS", "name": "NSE:M&M", "pe": 14.2, "growth": 17.5, "dividend": 2.1},
    {"symbol": "MARUTI.NS", "name": "NSE:MARUTI", "pe": 16.8, "growth": 15.2, "dividend": 2.3},
    {"symbol": "NESTLEIND.NS", "name": "NSE:NESTLEIND", "pe": 48.5, "growth": 7.2, "dividend": 0.9},
    {"symbol": "NTPC.NS", "name": "NSE:NTPC", "pe": 14.8, "growth": 12.5, "dividend": 4.2},
    {"symbol": "ONGC.NS", "name": "NSE:ONGC", "pe": 7.5, "growth": 11.3, "dividend": 5.1},
    {"symbol": "POWERGRID.NS", "name": "NSE:POWERGRID", "pe": 22.3, "growth": 9.5, "dividend": 3.8},
    {"symbol": "RELIANCE.NS", "name": "NSE:RELIANCE", "pe": 20.1, "growth": 14.2, "dividend": 1.5},
    {"symbol": "SBIN.NS", "name": "NSE:SBIN", "pe": 13.2, "growth": 19.8, "dividend": 3.2},
    {"symbol": "SUNPHARMA.NS", "name": "NSE:SUNPHARMA", "pe": 32.1, "growth": 12.5, "dividend": 1.1},
    {"symbol": "TATACONSUM.NS", "name": "NSE:TATACONSUM", "pe": 25.8, "growth": 8.3, "dividend": 1.8},
    {"symbol": "TATASTEEL.NS", "name": "NSE:TATASTEEL", "pe": 9.6, "growth": 15.2, "dividend": 2.9},
    {"symbol": "TCS.NS", "name": "NSE:TCS", "pe": 24.7, "growth": 11.8, "dividend": 2.5},
    {"symbol": "TECHM.NS", "name": "NSE:TECHM", "pe": 18.3, "growth": 13.2, "dividend": 2.2},
    {"symbol": "TITAN.NS", "name": "NSE:TITAN", "pe": 32.4, "growth": 16.5, "dividend": 0.4},
    {"symbol": "ULTRACEMCO.NS", "name": "NSE:ULTRACEMCO", "pe": 26.8, "growth": 10.2, "dividend": 1.5},
    {"symbol": "UPL.NS", "name": "NSE:UPL", "pe": 14.5, "growth": 11.8, "dividend": 2.0},
    {"symbol": "WIPRO.NS", "name": "NSE:WIPRO", "pe": 19.6, "growth": 12.3, "dividend": 2.8},
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

    output_file = f"pegy_output_{today}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nJSON data saved to {output_file}")

if __name__ == "__main__":
    main()
