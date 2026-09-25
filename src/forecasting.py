import pandas as pd
import numpy as np

def forecast_financials(history, years=5, revenue_growth=0.06, ebitda_margin=0.34,
                        da_pct_revenue=0.04, capex_pct_revenue=0.035,
                        dnwc_pct_revenue=0.005, tax_rate=0.16):
    hist = history.copy()
    last = hist.iloc[-1]

    base_revenue = float(last["revenue"])
    last_fcf = float(last.get("fcf", np.nan)) if pd.notna(last.get("fcf", np.nan)) else np.nan

    rows = []
    for i in range(1, years + 1):
        revenue = base_revenue * ((1 + revenue_growth) ** i)
        ebitda = revenue * ebitda_margin
        da = revenue * da_pct_revenue
        ebit = ebitda - da
        tax = max(0, ebit * tax_rate)
        nopat = ebit - tax
        capex = revenue * capex_pct_revenue
        dnwc = revenue * dnwc_pct_revenue
        fcf = nopat + da - capex - dnwc

        rows.append({
            "forecast_year": i,
            "revenue": revenue,
            "revenue_growth": revenue_growth,
            "ebitda": ebitda,
            "ebitda_margin": ebitda_margin,
            "depreciation": da,
            "ebit": ebit,
            "tax": tax,
            "nopat": nopat,
            "capex": capex,
            "delta_nwc": dnwc,
            "fcf": fcf,
        })

    return pd.DataFrame(rows)
