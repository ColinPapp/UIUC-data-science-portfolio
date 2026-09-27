# Predicting Probability of MLB Batter Swinging Using Machine Learning

**Course:** CS307, UIUC | **Tools:** Python, scikit-learn, pandas, seaborn/matplotlib

## Summary
Calibrated random forest estimating the probability a batter swings at a given pitch, using pitch-tracking and game-situation data from Zac Gallen's 2023 season.

## Approach
- Data: 2,663 pitches, 21 features (pitch characteristics, count, baserunners, batter stance and strike zone)
- Model: random forest wrapped in sigmoid calibration, grid-searched over tree count, depth, split criterion, and calibration method
- Metric: Brier score

## Key Result
0.1803 test Brier score with 73.3% accuracy; expected calibration error of 0.0319.

## Files
- [Notebook](mlb-swing-probability.ipynb) | [HTML report](https://colinpapp.github.io/UIUC-data-science-portfolio/CS%20307%20Reports/mlb-swing-probability/mlb-swing-probability.html)

## Finance Applications
Calibrated probability models are the foundation of credit default probability (PD) estimation and any priced decision driven by a predicted likelihood.
