## Suggested notebook workflow

Create Jupyter notebooks in this order:

1. `01_financial_analysis.ipynb`
   - Load historical_financials.csv
   - Revenue/EBITDA/margin charts
   - Growth and accounting ratios
   - Anomaly observations

2. `02_dcf_valuation.ipynb`
   - Explain WACC
   - Build FCFF
   - DCF valuation
   - Sensitivity heatmap

3. `03_comparable_companies.ipynb`
   - Peer data
   - EV/Revenue and EV/EBITDA
   - Distribution plots
   - Implied valuation

4. `04_valuation_regression.ipynb`
   - Build a larger peer universe
   - Regression of valuation multiples against fundamentals
   - Feature importance / coefficient interpretation

5. `05_monte_carlo_valuation.ipynb`
   - Simulate assumptions
   - Plot intrinsic-value distribution
   - Calculate percentiles
   - Examine assumption/value relationships
