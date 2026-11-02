# -*- coding: utf-8 -*-
"""
Coursework code adapted for a public portfolio.
The original dataset and the derived cluster-label file are not included.
See ../../../data/README.md for expected inputs and data notes.
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import random

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False



# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the assignment dataset
df = pd.read_csv("data/early_2012_2013_loan_sample_with_outcome.csv")

# Quick checks
print(df.shape)
print(df.head())
print(df.columns.tolist())

# Target variable
target = "loan_is_bad"

# Check target
print(df[target].value_counts(dropna=False))
print(df[target].isna().sum())

# Convert target from True/False to 1/0
df["loan_is_bad"] = df["loan_is_bad"].astype(int)

selected_features = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "annual_inc",
    "dti",
    "home_ownership",
    "verification_status",
    "delinq_2yrs",
    "inq_last_6mths",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "total_acc"
]

# Define X and y
X = df[selected_features]
y = df["loan_is_bad"]

# Quick checks
print(X.shape)
print(y.shape)
print(y.value_counts())
print(X.columns.tolist())

# Check missing values in selected features and target

print(df[selected_features + ["loan_is_bad"]].isnull().sum())

# Identify column types
numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

print("Number of numeric columns:", len(numeric_cols))
print("Number of categorical columns:", len(categorical_cols))

print("\nCategorical columns:")
print(categorical_cols)

# Split data into train (70%), validation (15%), and test (15%)
from sklearn.model_selection import train_test_split

# First split (Train vs Temp)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# Second split (Validation vs Test)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.5,
    random_state=42,
    stratify=y_temp
)

# Check dataset sizes
print("Train:", X_train.shape)
print("Validation:", X_val.shape)
print("Test:", X_test.shape)

# One-Hot Encoding after splitting
categorical_cols_split = X_train.select_dtypes(include=["object"]).columns.tolist()

X_train = pd.get_dummies(X_train, columns=categorical_cols_split, drop_first=True)
X_val = pd.get_dummies(X_val, columns=categorical_cols_split, drop_first=True)
X_test = pd.get_dummies(X_test, columns=categorical_cols_split, drop_first=True)

# Align validation and test columns to training columns
X_val = X_val.reindex(columns=X_train.columns, fill_value=0)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

# Standardize features for neural network training
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit scaler on training data and transform all sets
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors

import torch

X_train = torch.tensor(np.array(X_train, dtype=np.float32), dtype=torch.float32)
X_val = torch.tensor(np.array(X_val, dtype=np.float32), dtype=torch.float32)
X_test = torch.tensor(np.array(X_test, dtype=np.float32), dtype=torch.float32)

y_train = torch.tensor(np.array(y_train, dtype=np.float32), dtype=torch.float32).view(-1, 1)
y_val = torch.tensor(np.array(y_val, dtype=np.float32), dtype=torch.float32).view(-1, 1)
y_test = torch.tensor(np.array(y_test, dtype=np.float32), dtype=torch.float32).view(-1, 1)

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)
print(y_train.shape)

# Create TensorDatasets and DataLoaders

from torch.utils.data import TensorDataset, DataLoader

train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=500, shuffle=True)

val_dataset = TensorDataset(X_val, y_val)
val_loader = DataLoader(val_dataset, batch_size=500, shuffle=False)

test_dataset = TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=500, shuffle=False)
print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}, Test samples: {len(X_test)}")

# Define the model

class LoanDefaultModel(nn.Module):
    def __init__(self, input_dim):
        super(LoanDefaultModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.network(x)

# Initialize model

input_dim = X_train.shape[1]
model = LoanDefaultModel(input_dim).to(device)
print(model)

# Define loss function and optimizer

pos_weight = torch.tensor([(y_train.shape[0] - y_train.sum().item()) / y_train.sum().item()], dtype=torch.float32).to(device)
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# AdamW adds weight decay directly to the weight update rule for better regularization
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)

# Learning Rate Decay: Reduces LR when validation loss plateaus
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)

# Training loop

epochs = 100
patience = 10
best_val_loss = float('inf')
epochs_no_improve = 0
early_stop = False

train_losses = []
val_losses = []

for epoch in range(epochs):
    if early_stop:
        print(f"Early stopping triggered at epoch {epoch}")
        break

    # --- Training Phase ---
    model.train()
    running_loss = 0.0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)

    epoch_train_loss = running_loss / len(train_loader.dataset)
    train_losses.append(epoch_train_loss)

    # --- Validation Phase ---
    model.eval()
    val_loss = 0.0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            val_loss += loss.item() * inputs.size(0)

    epoch_val_loss = val_loss / len(val_loader.dataset)
    val_losses.append(epoch_val_loss)

    scheduler.step(epoch_val_loss)

    # --- Early Stopping ---
    if epoch_val_loss < best_val_loss:
        best_val_loss = epoch_val_loss
        epochs_no_improve = 0
        torch.save(model.state_dict(), "best_loan_default_model.pth")
    else:
        epochs_no_improve += 1
        if epochs_no_improve >= patience:
            early_stop = True

    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1:03d}/{epochs} | Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f}")

# Validation performance

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

model.load_state_dict(torch.load("best_loan_default_model.pth"))
model.eval()

val_probs = []
val_preds = []
val_actuals = []
val_loss = 0.0

with torch.no_grad():
    for inputs, labels in val_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        probs = torch.sigmoid(outputs)
        preds = (probs >= 0.5).float()

        val_loss += loss.item() * inputs.size(0)

        val_probs.extend(probs.cpu().numpy().flatten())
        val_preds.extend(preds.cpu().numpy().flatten())
        val_actuals.extend(labels.cpu().numpy().flatten())

val_loss = val_loss / len(val_loader.dataset)

print(f"Validation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {accuracy_score(val_actuals, val_preds):.4f}")
print(f"Validation Precision: {precision_score(val_actuals, val_preds):.4f}")
print(f"Validation Recall: {recall_score(val_actuals, val_preds):.4f}")
print(f"Validation F1: {f1_score(val_actuals, val_preds):.4f}")
print(f"Validation ROC-AUC: {roc_auc_score(val_actuals, val_probs):.4f}")
print(f"Validation PR-AUC: {average_precision_score(val_actuals, val_probs):.4f}")

# Test performance

model.load_state_dict(torch.load("best_loan_default_model.pth"))
model.eval()

test_probs = []
test_preds = []
test_actuals = []
test_loss = 0.0

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        probs = torch.sigmoid(outputs)
        preds = (probs >= 0.5).float()

        test_loss += loss.item() * inputs.size(0)

        test_probs.extend(probs.cpu().numpy().flatten())
        test_preds.extend(preds.cpu().numpy().flatten())
        test_actuals.extend(labels.cpu().numpy().flatten())

test_loss = test_loss / len(test_loader.dataset)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {accuracy_score(test_actuals, test_preds):.4f}")
print(f"Test Precision: {precision_score(test_actuals, test_preds):.4f}")
print(f"Test Recall: {recall_score(test_actuals, test_preds):.4f}")
print(f"Test F1: {f1_score(test_actuals, test_preds):.4f}")
print(f"Test ROC-AUC: {roc_auc_score(test_actuals, test_probs):.4f}")
print(f"Test PR-AUC: {average_precision_score(test_actuals, test_probs):.4f}")

# Plot learning curves

plt.figure(figsize=(10, 5))
plt.plot(train_losses, label="Training Loss")
plt.plot(val_losses, label="Validation Loss")
plt.axvline(x=len(train_losses) - epochs_no_improve - 1,
            color='r', linestyle='--', label='Best Model')
plt.title('Loss Curves over Epochs')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()

# ROC curve

from sklearn.metrics import roc_curve, auc

fpr, tpr, _ = roc_curve(test_actuals, test_probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.4f})")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.show()

# Precision-Recall curve

from sklearn.metrics import precision_recall_curve, average_precision_score

precision, recall, _ = precision_recall_curve(test_actuals, test_probs)
pr_auc = average_precision_score(test_actuals, test_probs)

plt.figure(figsize=(6, 6))
plt.plot(recall, precision, label=f"PR Curve (AUC = {pr_auc:.4f})")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
plt.legend(loc="lower left")
plt.show()

# Classification report

from sklearn.metrics import classification_report

print(classification_report(test_actuals, test_preds, digits=4))

# Helper function for model experiments

from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

class LoanDefaultModel(nn.Module):
    def __init__(self, input_dim, hidden1=64, hidden2=32, dropout_rate=0.2):
        super(LoanDefaultModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.BatchNorm1d(hidden1),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(hidden1, hidden2),
            nn.BatchNorm1d(hidden2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(hidden2, 1)
        )

    def forward(self, x):
        return self.network(x)


def train_and_evaluate_model(hidden1=64, hidden2=32, dropout_rate=0.2, lr=0.001, batch_size=500, patience=10, epochs=100):
    train_loader_exp = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader_exp = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = LoanDefaultModel(input_dim=X_train.shape[1], hidden1=hidden1, hidden2=hidden2, dropout_rate=dropout_rate).to(device)

    pos_weight = torch.tensor([(y_train.shape[0] - y_train.sum().item()) / y_train.sum().item()], dtype=torch.float32).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)

    best_val_loss = float('inf')
    best_state = None
    epochs_no_improve = 0

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for inputs, labels in train_loader_exp:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        model.eval()
        val_loss = 0.0
        val_probs = []
        val_actuals = []

        with torch.no_grad():
            for inputs, labels in val_loader_exp:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                probs = torch.sigmoid(outputs)

                val_loss += loss.item() * inputs.size(0)
                val_probs.extend(probs.cpu().numpy().flatten())
                val_actuals.extend(labels.cpu().numpy().flatten())

        epoch_val_loss = val_loss / len(val_loader_exp.dataset)
        scheduler.step(epoch_val_loss)

        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            best_state = model.state_dict()
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                break

    model.load_state_dict(best_state)

    model.eval()
    val_probs = []
    val_actuals = []

    with torch.no_grad():
        for inputs, labels in val_loader_exp:
            inputs = inputs.to(device)
            outputs = model(inputs)
            probs = torch.sigmoid(outputs)

            val_probs.extend(probs.cpu().numpy().flatten())
            val_actuals.extend(labels.numpy().flatten())

    val_preds = (np.array(val_probs) >= 0.5).astype(int)

    return {
        "hidden1": hidden1,
        "hidden2": hidden2,
        "dropout_rate": dropout_rate,
        "lr": lr,
        "batch_size": batch_size,
        "best_val_loss": best_val_loss,
        "val_precision": precision_score(val_actuals, val_preds),
        "val_recall": recall_score(val_actuals, val_preds),
        "val_f1": f1_score(val_actuals, val_preds),
        "val_roc_auc": roc_auc_score(val_actuals, val_probs),
        "val_pr_auc": average_precision_score(val_actuals, val_probs)
    }

# Model comparison

experiments = [
    {"hidden1": 64, "hidden2": 32, "dropout_rate": 0.2, "lr": 0.001, "batch_size": 500},
    {"hidden1": 128, "hidden2": 64, "dropout_rate": 0.2, "lr": 0.001, "batch_size": 500},
    {"hidden1": 64, "hidden2": 32, "dropout_rate": 0.3, "lr": 0.001, "batch_size": 500},
    {"hidden1": 64, "hidden2": 32, "dropout_rate": 0.2, "lr": 0.0005, "batch_size": 256}
]

experiment_results = []

for config in experiments:
    result = train_and_evaluate_model(**config)
    experiment_results.append(result)

experiment_results_df = pd.DataFrame(experiment_results)
experiment_results_df.sort_values(by="val_pr_auc", ascending=False)

# Threshold tuning on test probabilities

threshold_results = []

for threshold in [0.30, 0.40, 0.50, 0.60]:
    preds = (np.array(test_probs) >= threshold).astype(int)

    threshold_results.append({
        "threshold": threshold,
        "precision": precision_score(test_actuals, preds),
        "recall": recall_score(test_actuals, preds),
        "f1": f1_score(test_actuals, preds)
    })

threshold_results_df = pd.DataFrame(threshold_results)
threshold_results_df

# Plot precision, recall and F1 across thresholds

plt.figure(figsize=(8, 5))
plt.plot(threshold_results_df["threshold"], threshold_results_df["precision"], marker="o", label="Precision")
plt.plot(threshold_results_df["threshold"], threshold_results_df["recall"], marker="o", label="Recall")
plt.plot(threshold_results_df["threshold"], threshold_results_df["f1"], marker="o", label="F1")
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Threshold Tuning")
plt.legend()
plt.show()

# Recreate Q3 split with 1-based row IDs to match R export

df_split_source = pd.read_csv("data/early_2012_2013_loan_sample_with_outcome.csv").copy()
df_split_source["row_id"] = np.arange(1, len(df_split_source) + 1)
df_split_source["loan_is_bad"] = df_split_source["loan_is_bad"].astype(int)

selected_features = [
    "loan_amnt", "term", "int_rate", "installment", "grade", "annual_inc",
    "dti", "home_ownership", "verification_status", "delinq_2yrs",
    "inq_last_6mths", "open_acc", "pub_rec", "revol_bal", "total_acc"
]

X_split = df_split_source[["row_id"] + selected_features]
y_split = df_split_source["loan_is_bad"]

X_train_split, X_temp_split, y_train_split, y_temp_split = train_test_split(
    X_split, y_split, test_size=0.3, random_state=42, stratify=y_split
)

X_val_split, X_test_split, y_val_split, y_test_split = train_test_split(
    X_temp_split, y_temp_split, test_size=0.5, random_state=42, stratify=y_temp_split
)

test_row_ids = X_test_split["row_id"].values
print("Test rows:", len(test_row_ids))

# Merge exact Q2 segments onto Q3 predictions

cluster_labels_exact = pd.read_csv("data/q2_segments_exact.csv")

test_results_cluster = pd.DataFrame({
    "row_id": test_row_ids,
    "actual": test_actuals,
    "predicted": test_preds,
    "predicted_probability": test_probs
})

test_results_cluster = test_results_cluster.merge(
    cluster_labels_exact,
    on="row_id",
    how="left"
)

print(test_results_cluster["segment"].value_counts(dropna=False))
test_results_cluster.head()

# Cluster-level metrics

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    ConfusionMatrixDisplay, roc_curve, precision_recall_curve
)

cluster_eval = []

for label, group in test_results_cluster.dropna(subset=["segment"]).groupby("segment"):
    y_true = group["actual"]
    y_pred = group["predicted"]
    y_prob = group["predicted_probability"]

    cluster_eval.append({
        "segment": label,
        "n": len(group),
        "bad_rate": y_true.mean(),
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "pr_auc": average_precision_score(y_true, y_prob)
    })

cluster_eval_df = pd.DataFrame(cluster_eval)

segment_order = [
    "Low Risk (Prime)",
    "Medium Risk (Near-Prime)",
    "High Risk (Subprime)"
]
cluster_eval_df["segment"] = pd.Categorical(cluster_eval_df["segment"], categories=segment_order, ordered=True)
cluster_eval_df = cluster_eval_df.sort_values("segment")

cluster_eval_df

# Cluster main comparison performance bar chart

import matplotlib.pyplot as plt
import numpy as np

plot_df = cluster_eval_df.set_index("segment")[["precision", "recall", "f1"]]

colors = ["#4C78A8", "#F58518", "#54A24B"]

ax = plot_df.plot(
    kind="bar",
    figsize=(11, 6),
    color=colors,
    width=0.72,
    edgecolor="black",
    linewidth=0.6
)

plt.title("Q3 Model Performance by Borrower Segment", fontsize=16, weight="bold", pad=14)
plt.ylabel("Score", fontsize=12)
plt.xlabel("")
plt.xticks(rotation=0, ha="right", fontsize=11)
plt.yticks(fontsize=11)
plt.ylim(0, 1.0)
plt.legend(title="Metric", fontsize=11, title_fontsize=11, frameon=True)
plt.grid(axis="y", linestyle="--", alpha=0.4)

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, fmt="%.3f", padding=3, fontsize=9)

plt.tight_layout()
plt.show()

# Confusion matrices by borrower segment

for seg in segment_order:
    group = test_results_cluster[test_results_cluster["segment"] == seg]
    if len(group) == 0:
        continue

    cm = confusion_matrix(group["actual"], group["predicted"])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues")
    plt.title(f"Confusion Matrix: {seg}")
    plt.show()