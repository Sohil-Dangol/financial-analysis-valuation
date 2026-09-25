from pathlib import Path
import json
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.project_config import COMPANY, PEERS, MODEL, PATHS
from src.sec_data import fetch_companyfacts, build_historical_dataset, save_historical
from src.market_data import download_market_data, get_peer_snapshot
from src.financial_analysis import add_financial_metrics, estimate_ebitda
from src.forecasting import forecast_financials
from src.dcf import cost_of_equity, wacc, dcf_valuation, sensitivity_table
from src.comps import calculate_multiples, implied_value
from src.monte_carlo import monte_carlo_dcf
from src.anomaly_detection import detect_anomalies
from src.reporting import save_summary_chart

def main():
    for p in PATHS.values():
        p.mkdir(parents=True, exist_ok=True)

    print(f"Downloading SEC XBRL data for {COMPANY['name']}...")
    payload = fetch_companyfacts(COMPANY["cik"], PATHS["raw"])

    historical = build_historical_dataset(payload, years=10)
    historical = add_financial_metrics(historical)
    historical = estimate_ebitda(historical)
    save_historical(historical, PATHS["processed"] / "historical_financials.csv")

    print("Downloading market data...")
    prices, info = download_market_data(COMPANY["ticker"])
    peers = get_peer_snapshot(PEERS)
    peers = calculate_multiples(peers)
    peers.to_csv(PATHS["processed"] / "peer_snapshot.csv", index=False)

    # Forecast
    forecast = forecast_financials(
        historical,
        years=COMPANY["forecast_years"],
        revenue_growth=MODEL["revenue_growth"],
        ebitda_margin=MODEL["ebitda_margin"],
        da_pct_revenue=MODEL["da_pct_revenue"],
        capex_pct_revenue=MODEL["capex_pct_revenue"],
        dnwc_pct_revenue=MODEL["dnwc_pct_revenue"],
        tax_rate=MODEL["tax_rate"],
    )
    forecast.to_csv(PATHS["processed"] / "forecast.csv", index=False)

    # Market inputs
    beta = info.get("beta") or 1.0
    market_cap = info.get("marketCap") or 0
    debt_value = 0
    try:
        latest = historical.iloc[-1]
        debt_value = max(float(latest.get("total_liabilities", 0) or 0) - float(latest.get("cash", 0) or 0), 0)
    except Exception:
        pass

    ke = cost_of_equity(MODEL["risk_free_rate"], beta, MODEL["equity_risk_premium"])
    discount = wacc(ke, MODEL["debt_cost"], MODEL["tax_rate"], market_cap, debt_value)

    net_debt = debt_value
    dcf = dcf_valuation(forecast, discount, MODEL["terminal_growth"], net_debt)
    pd.DataFrame([dcf]).to_csv(PATHS["outputs"] / "dcf_summary.csv", index=False)

    sens = sensitivity_table(
        forecast,
        [0.07, 0.08, 0.09, 0.10, 0.11],
        [0.015, 0.020, 0.025, 0.030, 0.035],
        net_debt
    )
    sens.to_csv(PATHS["outputs"] / "dcf_sensitivity.csv")

    # Comps
    target_revenue = float(historical.iloc[-1]["revenue"])
    target_ebitda = float(historical.iloc[-1].get("ebitda", historical.iloc[-1]["operating_income"]))
    comps_value = implied_value(target_revenue, target_ebitda, peers.dropna(subset=["ev_revenue","ev_ebitda"]))
    pd.DataFrame([comps_value]).to_csv(PATHS["outputs"] / "comps_valuation.csv", index=False)

    # Monte Carlo
    mc = monte_carlo_dcf(
        forecast,
        wacc_mean=discount,
        growth_mean=MODEL["terminal_growth"],
        simulations=10000,
        net_debt=net_debt,
    )
    mc["values"].to_csv(PATHS["outputs"] / "monte_carlo_values.csv", index=False)
    mc["summary"].to_csv(PATHS["outputs"] / "monte_carlo_summary.csv")

    # Anomalies
    anomalies = detect_anomalies(historical)
    anomalies.to_csv(PATHS["outputs"] / "financial_anomalies.csv", index=False)

    # Charts
    save_summary_chart(historical, PATHS["outputs"] / "charts")

    # Compact model summary
    summary = {
        "company": COMPANY,
        "beta": beta,
        "cost_of_equity": ke,
        "wacc": discount,
        "dcf": dcf,
        "monte_carlo_median": float(mc["summary"]["50%"]) if "50%" in mc["summary"] else None,
    }
    (PATHS["outputs"] / "model_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    print("\nDone.")
    print(f"Historical data: {PATHS['processed'] / 'historical_financials.csv'}")
    print(f"DCF equity value: {dcf['equity_value']:,.0f}")
    print(f"WACC: {discount:.2%}")
    print(f"Monte Carlo median: {summary['monte_carlo_median']:,.0f}")

if __name__ == "__main__":
    main()
