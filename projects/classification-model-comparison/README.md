# Classification Model Comparison

## Case question

On an anonymised, class-imbalanced tabular dataset: how do class balancing, feature selection, and hyperparameter tuning change a classification workflow, and how do six different model families (SVM, logistic regression, random forest, LightGBM, CatBoost, XGBoost) compare on the same problem?

## Code

| File | Covers |
|---|---|
| [`svm_imbalance_and_tuning.ipynb`](notebooks/svm_imbalance_and_tuning.ipynb) | SVM — baseline, resampling, feature-selection, and tuned approaches |
| [`logistic_regression.ipynb`](notebooks/logistic_regression.ipynb) | Logistic regression — sampling-method comparison (SMOTE, class weighting, EasyEnsemble), feature selection, hyperparameter tuning (GridSearchCV and Optuna) |
| [`random_forest.ipynb`](notebooks/random_forest.ipynb) | Random forest with resampling comparison |
| [`lightgbm.ipynb`](notebooks/lightgbm.ipynb) | LightGBM |
| [`catboost.ipynb`](notebooks/catboost.ipynb) | CatBoost |
| [`xgboost.ipynb`](notebooks/xgboost.ipynb) | XGBoost, evaluated on F2-score, MCC, and PR-AUC for the imbalanced target |

All six notebooks model the same binary, class-imbalanced target (roughly 90/10 split) on the same anonymised dataset, so model families and resampling strategies can be compared directly.

## Data and teamwork

This is team coursework (IB9BW0, Analytics in Practice). The input CSV and execution outputs are not included, and results are not independently reproduced here. Each notebook uses a project-relative path under `data/` when the permitted input is available.
