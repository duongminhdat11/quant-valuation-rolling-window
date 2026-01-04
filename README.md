#Valuation Cluster-IC Framework

This project implements a cluster-based valuation framework that combines
multiple valuation models using rolling-window signals and Rank Information
Coefficient (IC) weighting.

## Methodology
For each test year, valuation signals are constructed using rolling three-year
averages of model-implied expected returns. Stocks are clustered ex-ante based
on multi-model valuation signals.

Within each cluster, valuation models are evaluated using Rank IC, and
cluster-specific model weights are derived accordingly. Final expected returns
are computed as IC-weighted combinations of valuation signals and evaluated
using cross-sectional Rank IC and top–bottom portfolio spreads.

Regime labels are assigned post hoc using rule-based criteria for
interpretability and are not used in signal construction.

## Results
Key evaluation results are summarized in:
- `reports/yearly_ic_summary.csv`

## Notes
Data acquisition and heavy preprocessing were performed in Kaggle and are
omitted here for clarity and runtime considerations.
