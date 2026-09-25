from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def save_summary_chart(df, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    if "revenue" in df and "ebitda" in df:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df["period_end"], df["revenue"] / 1e9, marker="o", label="Revenue")
        ax.plot(df["period_end"], df["ebitda"] / 1e9, marker="o", label="EBITDA")
        ax.set_title("Historical Revenue and EBITDA")
        ax.set_ylabel("USD billions")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / "revenue_ebitda_trend.png", dpi=180)
        plt.close(fig)

    if "fcf_margin" in df:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df["period_end"], df["fcf_margin"] * 100, marker="o")
        ax.set_title("Free Cash Flow Margin")
        ax.set_ylabel("FCF margin (%)")
        fig.tight_layout()
        fig.savefig(out_dir / "fcf_margin.png", dpi=180)
        plt.close(fig)
