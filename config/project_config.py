from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

COMPANY = {
    "name": "Apple Inc.",
    "ticker": "AAPL",
    "cik": "0000320193",
    "currency": "USD",
    "forecast_years": 5,
}

PEERS = ["MSFT", "GOOGL", "AMZN"]

MODEL = {
    "risk_free_rate": 0.043,
    "equity_risk_premium": 0.055,
    "tax_rate": 0.16,
    "terminal_growth": 0.025,
    "debt_cost": 0.045,
    "revenue_growth": 0.06,
    "ebitda_margin": 0.34,
    "capex_pct_revenue": 0.035,
    "dnwc_pct_revenue": 0.005,
    "da_pct_revenue": 0.04,
}

PATHS = {
    "raw": PROJECT_ROOT / "data" / "raw",
    "processed": PROJECT_ROOT / "data" / "processed",
    "outputs": PROJECT_ROOT / "outputs",
    "excel": PROJECT_ROOT / "excel",
}
