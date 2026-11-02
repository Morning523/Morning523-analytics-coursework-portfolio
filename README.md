# Analytics & Coding Portfolio

A curated selection of team coursework, analytical code, and business case write-ups from my MSc in Business Analytics at the University of Warwick. The repository is organised around the questions each project answers; each project page explains the methods, code map, and data limits before the files.

## Project guide

| Project | Question and approach | Main tools |
|---|---|---|
| [Subscription analytics](projects/subscription-analytics/README.md) | How do subscription plan, tenure, review ratings, and customer value relate to churn? SQL analysis over a simulated coffee-subscription case. | SQL, SQLite, Python/Faker, Tableau visuals on portfolio site |
| [World Cup operations](projects/world-cup-operations/README.md) | How can tournament groups, qualifiers, and stadium assignments be explored under stated constraints? Simulation and optimisation scenarios. | Python, pandas, SciPy, PuLP, Monte Carlo |
| [Credit risk modelling](projects/credit-risk-modelling/README.md) | How can application risk be modelled and compared across customer segments? A team DNN coursework case. | Python, PyTorch, scikit-learn |
| [Classification model comparison](projects/classification-model-comparison/README.md) | How do resampling, feature selection, and tuning affect an imbalanced classification workflow, and how do six model families compare? | Python, scikit-learn, imbalanced-learn, LightGBM, CatBoost, XGBoost, Optuna |
| [Statistical analysis](projects/statistical-analysis/README.md) | What relationships appear in household spending and podcast listening data? Regression, interaction analysis, and visualisation. | R, tidyverse, ggplot2 |
| [Underground temperature statistics](projects/underground-temperature-statistics/README.md) | Does platform temperature differ by Underground line, and between Bakerloo and Central specifically? Individual R assessment. | R, tidyverse, ggplot2 |
| [A/B testing, clustering & deep learning](projects/ab-test-cluster-deep-learning/README.md) | Which loan-approval policy wins on net profit, does that change once borrowers are segmented, and can a neural network predict default risk? | R, Python, PyTorch, scikit-learn |

Three instructor-provided PyTorch notebooks are kept separately under [`reference/warwick-pytorch-course/`](reference/warwick-pytorch-course/). They are learning references, not original portfolio projects. Source and licence details are in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Case studies

Business-case write-ups (strategy and commercial analysis, not code), built on public sources only:

| Case | Question and approach |
|---|---|
| [Prioritising four business cases at Citi](case-studies/citi-business-prioritisation/README.md) | Individual case: which of four workstreams (audit remediation, structured notes growth, UI/UX, valuation AI) should a bank focus on first, using only public evidence? |
| [Biofuel market entry strategy](case-studies/biofuel-market-entry-strategy/README.md) | Case competition: should an oil & gas major enter biofuels, and how should it structure the entry (JV, M&A, organic growth)? Financial modelling, risk assessment, financing comparison. |

## How to read this repository

1. Start with a project or case page to understand its question, scope, and constraints.
2. Follow the code map to the SQL scripts, Python files, R script, or notebook — or read the case write-up directly.
3. Use [`data/README.md`](data/README.md) to see which inputs are intentionally absent.

## Teamwork and AI assistance

Most analytics projects are coursework completed with teams and are labelled accordingly; the underground temperature statistics project and the Citi business case are individual work. I contributed substantially to the team work; my earlier estimate of approximately 80–90% applies to coursework I previously described, not automatically to every notebook in this repository. I do not claim sole authorship of every file. The original R assessment declaration states that Gemini and ChatGPT supported code debugging, example approaches, and language polishing; those suggestions were interpreted and adapted for the coursework. For the biofuel case competition, teammates' names are intentionally not published; only my own contribution is attributed.

## Data and reuse

Course datasets, rendered notebook outputs, reports, and confidential client materials are not included. The subscription case is simulated; the World Cup work is scenario modelling, not an official forecast. Other model outputs have not been independently reproduced here. No open-source licence is granted for the team-coursework samples. The MIT licence in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) applies only to the separate course reference notebooks.
