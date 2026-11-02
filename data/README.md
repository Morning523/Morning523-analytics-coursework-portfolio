# Input data (not included)

Course datasets and workbooks are intentionally excluded because redistribution permissions and data provenance have not been verified, and raw data is unnecessary to show the methods.

Expected local inputs, if you have permission to use them:

- `household_expenditure.csv` and `podcast_listens.csv` — R analysis.
- `Q3.xlsx` — course workbook with `Ranking`, `jr`, and (for stadium assignment) `Capacity` sheets; used by two Python optimisation scripts.
- `early_2012_2013_loan_sample_with_outcome.csv` — credit application DNN notebook, and the A/B testing, clustering & deep learning project (LendingClub-derived loan data).
- `datafile_small.csv` — classification model comparison notebooks (all six).
- `london_underground_temperature.csv` — underground temperature statistics script, with `Temp`, `Line`, `Year`, `Month` columns.
- `q2_segments_exact.csv` — a derived cluster-label lookup (`row_id`, `cluster`, `segment`) used by the deep-learning default model to break results down by borrower segment; not included as it is derived from the same real respondent-level data.

The synthetic coffee notebook generates a simulated dataset itself with Faker; its database and generated records are not included. No BT Group client data, internal business information, survey responses, or confidential materials are part of this repository.
