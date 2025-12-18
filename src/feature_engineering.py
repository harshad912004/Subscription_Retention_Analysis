import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import sys
sys.path.append(os.path.abspath(".."))

df = pd.read_csv("data/processed/subscription_churn_clean.csv")
df.head()

df2 = df.drop(columns=["customer_id"])

df2["start_date"] = pd.to_datetime(df2["start_date"], errors="coerce")
df2["start_year"] = df2["start_date"].dt.year # pyright: ignore[reportAttributeAccessIssue]
df2["start_month"] = df2["start_date"].dt.month # pyright: ignore[reportAttributeAccessIssue]
df2["start_date"].dtype

df2["tenure_bucket"] = pd.cut(
    df2["tenure_months"],
    bins=[0, 6, 12, 18, 24],
    labels=["0-6", "6-12", "12-18", "18-24"]
)

df2.drop(columns=["start_date"], inplace=True)

categorical_cols = ["payment_method", "contract_type", "tenure_bucket"]

df2 = pd.get_dummies(
    df2,
    columns=categorical_cols,
    drop_first=True
)

X = df2.drop(columns=["churn"])
y = df2["churn"]

num_cols = [
    "tenure_months",
    "monthly_charges",
    "usage_frequency",
    "support_tickets",
    "start_year",
    "start_month"
]

scaler = StandardScaler()
X[num_cols] = scaler.fit_transform(X[num_cols])

X.shape
X.head()
X.columns

X.to_csv("data/processed/X_features.csv", index=False)
y.to_csv("data/processed/y_target.csv", index=False)
X = X.drop(columns=["cohort_month"])