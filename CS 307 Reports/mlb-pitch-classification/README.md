# Predicting MLB Pitch Types Using Machine Learning

**Course:** CS307, UIUC | **Tools:** Python, scikit-learn, pandas, seaborn/matplotlib

## Summary
K-nearest neighbors classifier identifying pitch type (four-seam fastball, split-finger, slider, sinker) from Statcast-style tracking measurements, framed as a real-time pitch identification tool for stadiums and broadcasts.

## Approach
- Data: 2,868 pitches from Kevin Gausman, 6 features (release speed, spin rate, movement, stance)
- Model: K-nearest neighbors, grid-searched over neighbor count, distance metric, weighting, and scaling
- Metric: classification accuracy

## Key Result
98.62% test accuracy; 98.12% best cross-validated accuracy.

## Files
- [Notebook](mlb-pitch-classification.ipynb) | [HTML report](mlb-pitch-classification.html)

## Finance Applications
Classifiers that map noisy high-frequency measurements to discrete states transfer directly to market-regime classification and trade-signal detection from order-book and tick data.
