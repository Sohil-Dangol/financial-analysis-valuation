import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def valuation_driver_regression(df):
    cols = ["ev_ebitda", "ev_revenue"]
    if not all(c in df.columns for c in cols):
        raise ValueError("Required valuation multiple columns are missing.")

    # Small peer samples are illustrative. A larger universe should be used
    # for a serious statistical study.
    features = [c for c in ["revenue_growth", "ebitda_margin", "roe", "beta"] if c in df.columns]
    data = df.dropna(subset=cols + features).copy()

    if len(data) < 5:
        return {"model": None, "features": features, "message": "Need at least 5 usable observations."}

    X = data[features]
    y = data["ev_ebitda"]

    model = Pipeline([
        ("scale", StandardScaler()),
        ("ridge", Ridge(alpha=1.0))
    ])
    model.fit(X, y)

    return {
        "model": model,
        "features": features,
        "r2_in_sample": model.score(X, y),
        "n": len(data),
        "coefficients": dict(zip(features, model.named_steps["ridge"].coef_)),
    }
