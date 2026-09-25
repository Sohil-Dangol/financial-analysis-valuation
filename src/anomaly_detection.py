import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    ratio_cols = [c for c in [
        "revenue_growth", "gross_margin", "operating_margin",
        "net_margin", "fcf_margin", "roa", "roe"
    ] if c in df.columns]

    if len(ratio_cols) < 2 or len(df.dropna(subset=ratio_cols)) < 5:
        return pd.DataFrame()

    work = df[["period_end"] + ratio_cols].dropna().copy()
    model = IsolationForest(contamination="auto", random_state=42)
    work["anomaly"] = model.fit_predict(work[ratio_cols])
    work["anomaly_score"] = model.decision_function(work[ratio_cols])
    return work.sort_values("anomaly_score")
