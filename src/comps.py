import numpy as np
import pandas as pd

def calculate_multiples(peer_df):
    df = peer_df.copy()
    df["ev_revenue"] = df["enterprise_value"] / df["revenue_ttm"]
    df["ev_ebitda"] = df["enterprise_value"] / df["ebitda_ttm"]
    return df

def peer_statistics(df):
    return pd.DataFrame({
        "EV/Revenue": df["ev_revenue"].describe(percentiles=[.25,.5,.75]),
        "EV/EBITDA": df["ev_ebitda"].describe(percentiles=[.25,.5,.75]),
    })

def implied_value(target_revenue, target_ebitda, peer_df):
    med_ev_rev = peer_df["ev_revenue"].median()
    med_ev_ebitda = peer_df["ev_ebitda"].median()
    return {
        "ev_from_revenue_multiple": target_revenue * med_ev_rev,
        "ev_from_ebitda_multiple": target_ebitda * med_ev_ebitda,
        "median_ev_revenue": med_ev_rev,
        "median_ev_ebitda": med_ev_ebitda,
    }
