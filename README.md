# Company Valuation & Financial Intelligence

A finance + accounting + data science project for analysing and valuing a public company using Python and Excel.

## What this project does

- Pulls public-company XBRL financial data from the SEC Company Facts API
- Pulls market data using `yfinance`
- Builds a normalised historical financial dataset
- Calculates revenue, EBITDA, EBIT, margins, growth, FCF and balance-sheet ratios
- Produces a driver-based forecast
- Builds a 3-statement-style forecast
- Performs a DCF valuation
- Performs comparable-company analysis
- Runs regression analysis on valuation multiples
- Runs DCF sensitivity analysis
- Runs Monte Carlo valuation
- Flags unusual financial-ratio observations
- Exports clean data for Excel
- Provides an Excel model template and presentation outline

## Default company

The starter configuration uses:

- Company: Apple Inc.
- Ticker: AAPL
- SEC CIK: 0000320193
- Peers: MSFT, GOOGL, AMZN

You can change these in `config/project_config.py`.

## Data sources

### Primary accounting data
The preferred source for US public companies is the SEC EDGAR/XBRL Company Facts API:
https://www.sec.gov/search-filings/edgar-application-programming-interfaces

It provides machine-readable XBRL facts from company filings such as 10-K and 10-Q. The SEC also publishes Financial Statement Data Sets containing numeric information from primary financial statements.

### Market data
`yfinance` is used for:
- historical share prices
- market capitalisation where available
- beta
- peer market data

For a professional-quality version, verify important market-data fields against an exchange/company filing or another licensed data provider.

## Setup

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run the complete pipeline:
```bash
python run_project.py
```

The pipeline writes outputs into `outputs/`.

## Project structure

```text
company-valuation-financial-intelligence/
├── config/
│   └── project_config.py
├── data/
│   ├── raw/
│   └── processed/
├── excel/
│   └── Company_Financial_Model.xlsx
├── notebooks/
│   └── README.md
├── outputs/
├── presentation/
│   └── Investment_Valuation_Deck.md
├── src/
│   ├── sec_data.py
│   ├── market_data.py
│   ├── financial_analysis.py
│   ├── forecasting.py
│   ├── dcf.py
│   ├── comps.py
│   ├── regression.py
│   ├── monte_carlo.py
│   ├── anomaly_detection.py
│   └── reporting.py
├── run_project.py
└── requirements.txt
```

## Important modelling note

SEC XBRL tags vary between companies. This project therefore uses a tag-priority approach and keeps the raw SEC response. Some companies may require adding company-specific tags in `src/sec_data.py`.

Do not treat the model's valuation output as investment advice. The point of the project is to demonstrate financial modelling, accounting understanding and analytical methodology.
