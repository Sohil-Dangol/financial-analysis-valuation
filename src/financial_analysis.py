import numpy as np
import pandas as pd

def add_financial_metrics(df):
    df = df.copy()
    for c in df.columns:
        if c not in ("period_end", "fiscal_year"):
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # SEC values are normally absolute currency amounts.
    if "revenue" in df:
        df["revenue_growth"] = df["revenue"].pct_change()
    if "operating_income" in df:
        df["operating_margin"] = df["operating_income"] / df["revenue"]
    if "net_income" in df:
        df["net_margin"] = df["net_income"] / df["revenue"]
    if "cost_of_revenue" in df:
        df["gross_profit"] = df["revenue"] - df["cost_of_revenue"]
        df["gross_margin"] = df["gross_profit"] / df["revenue"]

    if "operating_cash_flow" in df and "capex" in df:
        # Capex is usually reported as a positive cash outflow in XBRL.
        df["fcf"] = df["operating_cash_flow"] - df["capex"]
        df["fcf_margin"] = df["fcf"] / df["revenue"]

    if "total_assets" in df:
        df["roa"] = df["net_income"] / df["total_assets"]

    if "equity" in df:
        df["roe"] = df["net_income"] / df["equity"]

    if "cash" in df and "total_liabilities" in df:
        df["net_debt_proxy"] = df["total_liabilities"] - df["cash"]

    return df

def estimate_ebitda(df):
    df = df.copy()
    if "operating_income" in df and "depreciation" in df:
        df["ebitda"] = df["operating_income"] + df["depreciation"]
    elif "operating_income" in df:
        df["ebitda"] = df["operating_income"]
    return df
