import numpy as np
import pandas as pd

def cost_of_equity(risk_free, beta, erp):
    return risk_free + beta * erp

def wacc(cost_equity, cost_debt, tax_rate, equity_value, debt_value):
    total = equity_value + debt_value
    if total <= 0:
        return cost_equity
    return (equity_value / total) * cost_equity + (debt_value / total) * cost_debt * (1-tax_rate)

def dcf_valuation(forecast, discount_rate, terminal_growth, net_debt=0):
    fcf = forecast["fcf"].to_numpy(dtype=float)
    periods = np.arange(1, len(fcf) + 1)
    pv_fcf = fcf / ((1 + discount_rate) ** periods)

    terminal_value = fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / ((1 + discount_rate) ** periods[-1])

    enterprise_value = pv_fcf.sum() + pv_terminal
    equity_value = enterprise_value - net_debt

    return {
        "pv_explicit_fcf": pv_fcf.sum(),
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "net_debt": net_debt,
        "equity_value": equity_value,
    }

def sensitivity_table(forecast, wacc_values, growth_values, net_debt=0):
    out = pd.DataFrame(index=[f"{x:.1%}" for x in wacc_values],
                       columns=[f"{x:.1%}" for x in growth_values])
    for w in wacc_values:
        for g in growth_values:
            if w <= g:
                value = np.nan
            else:
                value = dcf_valuation(forecast, w, g, net_debt)["equity_value"]
            out.loc[f"{w:.1%}", f"{g:.1%}"] = value
    return out
