# A/B Testing, Clustering & Deep Learning on Loan Review Policies

## Case question

Using the public LendingClub loan-outcome dataset: which of two loan-approval policies (conservative vs. aggressive) maximises net profit, does that answer change once borrowers are segmented into risk clusters, and can a neural network predict default risk directly from application-time features?

## Code map

| File | Covers |
|---|---|
| `r/ADA1_Q1.Rmd` | A/B test: defines two rule-based approval policies, a profit-based evaluation metric, and a one-sided Welch t-test comparing mean net profit per approved loan |
| `r/ADA_Q2.Rmd` | Segmentation: PCA (KMO/Bartlett diagnostics, scree plot, loadings) followed by k-means clustering into Prime/Near-Prime/Subprime borrower segments, then re-evaluates both policies *within* each segment |
| `python/deep_learning_default_model.py` | Deep learning: a PyTorch feed-forward network (batch norm, dropout, early stopping, class-weighted loss for imbalance) predicting default risk, evaluated by ROC/PR-AUC and broken down by the borrower segments from Q2 |

## Key finding

The aggregate A/B test favours the aggressive policy on total net profit — but segment-level analysis shows that verdict is uneven: the aggressive policy is a clear win for low-risk borrowers (profit gain, negligible extra default risk) but a real trade-off for high-risk borrowers (strict screening still protects against default there). A uniform policy choice would miss this; a segment-differentiated policy outperforms both blanket policies on risk-adjusted return.

## Data and teamwork

Team coursework (IB98D0, Advanced Data Analysis). The original LendingClub-derived dataset, the derived cluster-label file, and rendered outputs are not included; see [`../../data/README.md`](../../data/README.md).
