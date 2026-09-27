# Predicting House Prices Using Machine Learning

**Course:** CS307, UIUC | **Tools:** Python, scikit-learn, pandas, seaborn/matplotlib

## Summary
Histogram Gradient Boosting regressor estimating home sale prices in Ames, Iowa from ~80 structural and quality features, framed as a Zillow-style valuation tool.

## Approach
- Data: 1,875 home sales (2006-2010), 81 features
- Model: Histogram gradient boosting, grid-searched over learning rate, depth, feature sampling
- Metric: MAPE, % of predictions within 20% of true value

## Key Result
7.99% test MAPE; 93.4% of predictions within 20% of actual sale price.

## Files
- [Notebook](house-price-prediction.ipynb) | [HTML report](https://colinpapp.github.io/UIUC-data-science-portfolio/CS%20307%20Reports/house-price-prediction/house-price-prediction.html)

## Finance Applications
Gradient boosting regressors are standard for collateral/real-asset valuation (AVMs, ABS/MBS collateral pricing) and factor-based return prediction - combining many noisy signals into one estimate.
