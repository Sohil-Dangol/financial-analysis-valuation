import numpy as np
import pandas as pd

def monte_carlo_dcf(base_forecast, wacc_mean=0.09, wacc_sd=0.01,
                    growth_mean=0.025, growth_sd=0.005,
                    revenue_growth_mean=0.06, revenue_growth_sd=0.02,
                    ebitda_margin_mean=0.34, ebitda_margin_sd=0.025,
                    net_debt=0, simulations=10000, seed=42):
    rng = np.random.default_rng(seed)
    values = []

    base_revenue = float(base_forecast.iloc[0]["revenue"]) / (1 + revenue_growth_mean)

    for _ in range(simulations):
        wacc = max(rng.normal(wacc_mean, wacc_sd), 0.04)
        g = max(rng.normal(growth_mean, growth_sd), 0.0)
        rg = rng.normal(revenue_growth_mean, revenue_growth_sd)
        margin = np.clip(rng.normal(ebitda_margin_mean, ebitda_margin_sd), 0.05, 0.70)

        revenue = base_revenue
        fcfs = []
        for year in range(len(base_forecast)):
            revenue *= (1 + rg)
            ebitda = revenue * margin
            da = revenue * 0.04
            ebit = ebitda - da
            tax = max(0, ebit * 0.16)
            fcf = (ebit - tax) + da - revenue * 0.035 - revenue * 0.005
            fcfs.append(fcf)

        if wacc <= g:
            continue

        pv = sum(f / ((1+wacc)**(i+1)) for i, f in enumerate(fcfs))
        tv = fcfs[-1] * (1+g) / (wacc-g)
        pv_tv = tv / ((1+wacc)**len(fcfs))
        values.append(pv + pv_tv - net_debt)

    s = pd.Series(values, name="equity_value")
    return {
        "values": s,
        "summary": s.describe(percentiles=[.05,.10,.25,.5,.75,.90,.95]),
    }
