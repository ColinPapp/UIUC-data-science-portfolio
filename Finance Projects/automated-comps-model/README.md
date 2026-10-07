# Automated Comparable Companies Model

## Context and Tools
Personal project. Python (pandas, yfinance, matplotlib, seaborn).

## Summary
Give it a ticker, get a comps workup. The model selects the six closest comparable companies by revenue within the same industry category, computes EV/EBITDA, EV/Revenue, EV/EBIT, and P/E multiples from live market data, derives an implied valuation range at the 25th percentile, median, and 75th percentile of peer multiples, and renders a six-panel benchmarking chart (revenue, EV/EBITDA, revenue growth, leverage, market cap, operating margin) with the target highlighted.

## Approach
Peer selection runs on revenue proximity within the target's industry category from a ticker universe spreadsheet, with no extra API calls for the screen itself. Multiples are built from yfinance financials, balance sheet, price, and shares outstanding, using a standard EV bridge (equity value plus debt, minority interest, and preferred stock, less cash), with an operating-income fallback for EBITDA. Each multiple's 25th, median, and 75th percentile values are applied to the target's own metrics to produce implied enterprise value, equity value, implied share price, and premium or discount to the current price.

## Key Result
A working engine end to end. On Procter & Gamble, it selected CL, CLX, CHD, ENR, SPB, and ODC as comps and produced a full multiples table: median EV/EBITDA of 12.87x implying $125.14 per share, median EV/EBIT of 19.17x implying $166.28, each with the corresponding premium or discount to the trading price.

## Files
- [Model](automated-comps-model.py)

Run it with `python automated-comps-model.py` after pointing `TICKERS_XLSX` at a spreadsheet with `Ticker`, `Revenue`, and `Category Name` columns. Calling `comparable("TICKER")` from another script returns the multiples table as a DataFrame.

## Takeaways
Automates the most repetitive part of a comps build: peer screening, multiple calculation, and benchmarking visuals in one call. The percentile-based valuation range keeps the output honest about dispersion instead of anchoring on a single multiple. The structure extends naturally to more multiples or a larger peer set.
