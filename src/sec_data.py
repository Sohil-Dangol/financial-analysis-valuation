import json
from pathlib import Path
import requests
import pandas as pd

STANDARD_TAGS = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
        "Revenues",
    ],
    "cost_of_revenue": [
        "CostOfRevenue",
        "CostOfGoodsAndServicesSold",
    ],
    "operating_income": [
        "OperatingIncomeLoss",
    ],
    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
    ],
    "cash": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    "receivables": [
        "AccountsReceivableNetCurrent",
        "AccountsReceivableNet",
    ],
    "inventory": [
        "InventoryNet",
        "InventoryGross",
    ],
    "current_assets": [
        "AssetsCurrent",
    ],
    "total_assets": [
        "Assets",
    ],
    "current_liabilities": [
        "LiabilitiesCurrent",
    ],
    "total_liabilities": [
        "Liabilities",
    ],
    "equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "depreciation": [
        "DepreciationDepletionAndAmortization",
        "DepreciationDepletionAndAmortizationPropertyPlantAndEquipment",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
    ],
    "operating_cash_flow": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],
    "interest_expense": [
        "InterestExpenseNonOperating",
        "InterestExpenseDebt",
    ],
    "income_tax": [
        "IncomeTaxExpenseBenefit",
    ],
    "shares": [
        "EntityCommonStockSharesOutstanding",
    ],
}

def fetch_companyfacts(cik: str, raw_dir: Path):
    raw_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    headers = {
        "User-Agent": "CompanyValuationFinancialIntelligence/1.0 contact@example.com"
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    payload = r.json()
    path = raw_dir / f"companyfacts_{cik}.json"
    path.write_text(json.dumps(payload, indent=2))
    return payload

def _pick_fact(facts, tags):
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        if tag in us_gaap:
            return us_gaap[tag]
    return None

def _annual_records(fact):
    if not fact:
        return []
    units = fact.get("units", {})
    unit = "USD" if "USD" in units else next(iter(units), None)
    if not unit:
        return []
    records = []
    for x in units[unit]:
        # Prefer annual 10-K data and duration around a year.
        form = x.get("form", "")
        fp = x.get("fp", "")
        start, end = x.get("start"), x.get("end")
        if not start or not end or form not in ("10-K", "10-K/A"):
            continue
        try:
            days = (pd.Timestamp(end) - pd.Timestamp(start)).days
        except Exception:
            continue
        if 300 <= days <= 400:
            records.append({
                "fy": x.get("fy"),
                "end": end,
                "start": start,
                "val": x.get("val"),
                "filed": x.get("filed"),
                "accn": x.get("accn"),
            })
    return records

def build_historical_dataset(payload, years=10):
    rows = {}
    for metric, tags in STANDARD_TAGS.items():
        fact = _pick_fact(payload, tags)
        for r in _annual_records(fact):
            key = r["end"]
            if key not in rows:
                rows[key] = {"period_end": key, "fiscal_year": r["fy"]}
            # Later-filed duplicates can exist. Keep the latest filing.
            current = rows[key].get(metric)
            if current is None or str(r["filed"]) >= str(rows[key].get(f"{metric}_filed", "")):
                rows[key][metric] = r["val"]
                rows[key][f"{metric}_filed"] = r["filed"]

    df = pd.DataFrame(rows.values())
    if df.empty:
        raise ValueError("No annual SEC facts could be extracted.")
    df["period_end"] = pd.to_datetime(df["period_end"])
    df = df.sort_values("period_end").tail(years).reset_index(drop=True)

    drop_cols = [c for c in df.columns if c.endswith("_filed")]
    df = df.drop(columns=drop_cols, errors="ignore")
    return df

def save_historical(df, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
