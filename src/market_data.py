from pathlib import Path
import pandas as pd
import yfinance as yf

def download_market_data(ticker, start="2015-01-01", end=None):
    t = yf.Ticker(ticker)
    hist = t.history(start=start, end=end, auto_adjust=False)
    hist = hist.reset_index()
    hist.to_csv(Path("data/raw") / f"{ticker}_prices.csv", index=False)

    info = {}
    try:
        info = t.info
    except Exception:
        pass

    return hist, info

def get_peer_snapshot(tickers):
    rows = []
    for ticker in tickers:
        t = yf.Ticker(ticker)
        try:
            info = t.info
        except Exception:
            info = {}

        rows.append({
            "ticker": ticker,
            "company": info.get("longName", ticker),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "revenue_ttm": info.get("totalRevenue"),
            "ebitda_ttm": info.get("ebitda"),
            "ebit": info.get("ebitda") if info.get("ebitda") else None,
            "share_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "beta": info.get("beta"),
        })

    return pd.DataFrame(rows)
