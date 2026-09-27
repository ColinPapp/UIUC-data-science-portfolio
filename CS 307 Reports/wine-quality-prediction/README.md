# Predicting Wine Quality with an AI Sommelier

**Course:** CS307, UIUC | **Tools:** Python, scikit-learn, pandas, seaborn/matplotlib

## Summary
K-nearest neighbors regressor estimating wine quality scores from physicochemical measurements, framed as an automated quality-control tool for wineries and distributors.

## Approach
- Data: 4,157 wines (UCI ML Repository), 12 features (acidity, pH, alcohol, sulfur dioxide, and more)
- Model: K-nearest neighbors regressor, grid-searched over neighbor count, distance metric, and weighting
- Metric: mean absolute error

## Key Result
0.46 test MAE; predictions within half a quality point on average on a 0-10 scale.

## Files
- [Notebook](wine-quality-prediction.ipynb) | [HTML report](wine-quality-prediction.html)

## Finance Applications
Nearest-neighbor logic is the statistical backbone of comparable-company analysis: valuing an asset from the observed prices of its closest peers.
