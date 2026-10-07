# Beta Factor Analysis: CAPM Mispricing in Large-Cap Industrials

## Context and Tools
Personal project. Python (pandas, yfinance, scikit-learn, matplotlib, seaborn).

## Summary
Front-to-back market risk factor analysis of all S&P 500 Industrials constituents with at least 10 years of trading history: 70 companies representing approximately 7.17% of the index by weight. Monthly regressions of each stock's excess returns against the S&P 500 derive implied alpha, beta, and statistical significance, flagging names potentially mispriced under a single-factor CAPM. Results are summarized in 10 visualizations and exported to Excel.

## Approach
Pulled 10 years of monthly returns via yfinance and computed excess returns over the 3-month T-bill rate. Ran an OLS regression per stock (excess stock return on excess market return) to estimate alpha, beta, and p-values, flagging alpha significant at the 10% level as mispriced. Ran the same procedure on Covid-era and pre-Covid windows for comparison. Tested CAPM's predictions with scatter analyses: market cap vs beta, market cap vs excess return, and beta vs excess return (the security market line).

## Key Result
Nine companies generated statistically significant alpha at the 10% level: FIX, AXON, PWR, EME, CAT, ODFL, TT, RSG, and ETN. These are names where realized returns cannot be explained by market exposure alone. Separately, CAPM's core prediction does not hold in this universe: no meaningful relationship between market cap and beta (R²=0.00), and no meaningful relationship between beta and annualized excess returns (R²=0.04).

## Files
- [Notebook](beta-factor-analysis.ipynb)
- [HTML report](https://colinpapp.github.io/UIUC-data-science-portfolio/Finance%20Projects/beta-factor-analysis/beta-factor-analysis.html)

The notebook reads tickers and base market data from `IndData.xlsx` (not included).

## Takeaways
Statistically significant alpha is a useful first screen for deeper fundamental work: it can indicate durable competitive advantages, pricing power, or structural tailwinds not yet reflected in valuations. The flat security market line is consistent with academic literature and a reminder that single-factor models leave considerable return variation unexplained within a sector.
