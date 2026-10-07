# PE Regression: Finding Undervalued S&P 500 Stocks

## Context and Tools
Course project (STAT 107, January 2024). Python (pandas, scikit-learn, matplotlib, seaborn).

## Summary
Uses S&P Capital IQ data on nearly the full S&P 500 to test how well earnings, revenue, and headcount explain market capitalization, then turns the best-fitting relationship into a screen for undervalued stocks. After cleaning to 437 profitable companies, the analysis compares correlations, runs linear regressions of market cap on each factor, and flags the stock with the largest negative residual relative to its size.

## Approach
Exported an S&P Capital IQ screen of S&P 500 constituents to CSV (data as of 11/26/23) and dropped unprofitable names, leaving 437 companies. Built P/E, P/EBITDA, and P/Sales multiples and compared median multiples by sector. Ran OLS regressions of market capitalization on net income, revenue, and full-time employees; earnings was the only strong correlation (r=0.89). Predicted each company's market cap from its earnings, computed residuals, scaled them by market cap, and selected the minimum residual percentage as the most undervalued name.

## Key Result
Home Depot (HD) screened as the most undervalued stock in the S&P 500: the model predicted a market capitalization 24% above the actual, implying $385 per share against $310 at the time. The stock rose 38% over the following year.

## Files
- [Notebook](pe-regression.ipynb)
- [HTML report](pe-regression.html)

The notebook was reconstructed from the original project PDF; it reads from `DS Project.csv` (not included).

## Takeaways
A simple earnings regression can be a productive first pass at relative value: the residual approach surfaces mispricing the market has not yet corrected without any forward assumptions. The sector median P/E comparison adds context on where the market is paying for growth versus pricing in stagnation.
