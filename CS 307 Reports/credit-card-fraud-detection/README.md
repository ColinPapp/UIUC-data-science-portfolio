# Detecting Credit Card Fraud with Machine Learning

**Course:** CS307, UIUC | **Tools:** Python, scikit-learn, pandas, seaborn/matplotlib

## Summary
Decision tree classifier flagging fraudulent credit card transactions under severe class imbalance, tuned to balance catching fraud against false alarms.

## Approach
- Data: 54,276 transactions over two days, 29 features (transaction amount plus 28 privacy-preserving principal components)
- Model: decision tree classifier, grid-searched over depth, minimum split size, and class weights, refit on F1
- Metric: precision, recall, F1

## Key Result
91.4% precision, 81.0% recall, 0.85 F1 on unseen test data.

## Files
- [Notebook](credit-card-fraud-detection.ipynb) | [HTML report](https://colinpapp.github.io/UIUC-data-science-portfolio/CS%20307%20Reports/credit-card-fraud-detection/credit-card-fraud-detection.html)

## Finance Applications
The same precision-recall tradeoff drives fraud and AML transaction monitoring and credit-risk flagging, where false positives cost customer trust and false negatives cost real losses.
