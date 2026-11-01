# Analytics & Coding Portfolio

A curated selection of team coursework and analytical code from my MSc in Business Analytics at the University of Warwick. The repository is organised around the questions each project answers; each project page explains the methods, code map, and data limits before the files.

## Project guide

| Project | Question and approach | Main tools |
|---|---|---|
| [Subscription analytics](projects/subscription-analytics/README.md) | How do subscription plan, tenure, review ratings, and customer value relate to churn? SQL analysis over a simulated coffee-subscription case. | SQL, SQLite, Python/Faker, Tableau visuals on portfolio site |
| [World Cup operations](projects/world-cup-operations/README.md) | How can tournament groups, qualifiers, and stadium assignments be explored under stated constraints? Simulation and optimisation scenarios. | Python, pandas, SciPy, PuLP, Monte Carlo |
| [Credit risk modelling](projects/credit-risk-modelling/README.md) | How can application risk be modelled and compared across customer segments? A team DNN coursework case. | Python, PyTorch, scikit-learn |
| [SVM classification](projects/svm-classification/README.md) | How do resampling, feature selection, and tuning affect an imbalanced classification workflow? | Python, scikit-learn, imbalanced-learn, Optuna |
| [Statistical analysis](projects/statistical-analysis/README.md) | What relationships appear in household spending and podcast listening data? Regression, interaction analysis, and visualisation. | R, tidyverse, ggplot2 |

Three instructor-provided PyTorch notebooks are kept separately under [`reference/warwick-pytorch-course/`](reference/warwick-pytorch-course/). They are learning references, not original portfolio projects. Source and licence details are in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## How to read this repository

1. Start with a project page to understand its question, scope, and constraints.
2. Follow the code map to the SQL scripts, Python files, R script, or notebook.
3. Use [`data/README.md`](data/README.md) to see which inputs are intentionally absent.

## Teamwork and AI assistance

The analytics projects are coursework completed with teams and are labelled accordingly. I contributed substantially to the work; my earlier estimate of approximately 80–90% applies to coursework I previously described, not automatically to every notebook in this repository. I do not claim sole authorship of every file. The original R assessment declaration states that Gemini and ChatGPT supported code debugging, example approaches, and language polishing; those suggestions were interpreted and adapted for the coursework.

## Data and reuse

Course datasets, rendered notebook outputs, reports, and confidential client materials are not included. The subscription case is simulated; the World Cup work is scenario modelling, not an official forecast. Other model outputs have not been independently reproduced here. No open-source licence is granted for the team-coursework samples. The MIT licence in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) applies only to the separate course reference notebooks.
