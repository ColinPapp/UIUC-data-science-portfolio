# Estimating Corporate Credit Spreads

## Context and Tools
FIN 453 / FIN 553 Project 1, Fall 2026, UIUC. Python (JAX, Optax, NumPy, pandas, Matplotlib).

## Summary
A prediction tool for a credit analyst: estimate a corporate bond's credit spread, its yield difference relative to a comparable benchmark bond, from company financial characteristics. Spreads are measured in basis points. The development set holds 12,000 labeled observations; a separate 5,000-observation test set (instructor-held) was predicted for submission. This is a stylized prediction exercise, not a calibrated pricing model or a causal analysis.

## Approach
Eight features: leverage, interest coverage, liquidity, profitability, asset volatility, log size, and two analyst signals. Two 80/20 train/validation splits were built: one by slicing the leverage-sorted file, one from a single seeded permutation, to show what ordered splitting does to a model trained on the low-leverage majority. The linear model was fit with a hand-written JAX training loop: half-MSE loss, gradients from `jax.grad`, a jitted Adam update (learning rate 0.01, 2,000 steps, batch size 256), with feature means and scales learned on training rows only and an intercept added after standardization. Three candidates went through three-fold cross-validation with fresh preprocessing, parameters, and optimizer state per fold: Linear, Expanded (adding leverage squared, interest-coverage squared, and leverage x asset volatility), and Expanded + ridge (lambda 0.01, intercept unpenalized). The winner was refit on all 12,000 development rows and applied to the test set.

## Key Result
The Expanded model won cross-validation with a mean MSE of 503.85 bps², against 752.79 for Linear and 517.26 for Expanded + ridge: the three curvature terms earned their keep, while ridge added nothing on top of them. The split comparison is the sharper lesson. On the random split, the linear baseline reached 28.07 bps validation RMSE (train 27.33, constant benchmark 83.68). On the ordered split, the same model scored 61.11 bps: a model trained only on low-leverage companies extrapolates poorly to high-leverage ones. The final Expanded model, refit on all development rows, produced predictions for all 5,000 test observations.

## Files
- [Notebook](credit-spread-estimation.ipynb)
- `development.csv` (12,000 labeled observations; included so the notebook runs as-is through Part 3)

The notebook's Part 4 reads `test_features.csv`, which is not included: the test set and its labels were held by the instructor.

## Takeaways
Learn scaling statistics on training rows only, or validation scores overstate generalization. A model can stay linear in its parameters while describing a curved relationship, as long as the curvature lives in the features. And the split is part of the experiment: when the data file is sorted, an ordered split tests extrapolation, not ordinary prediction.
