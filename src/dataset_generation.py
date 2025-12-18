import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(DATA_DIR, exist_ok=True)

file_path = os.path.join(DATA_DIR, "subscription_churn_raw.csv")

np.random.seed(42)

# Number of customers
n_customers = 1200

# Generate customer IDs
customer_id = np.arange(10001, 10001 + n_customers)

# Subscription start dates
start_date = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    np.random.randint(0, 365, size=n_customers), unit="D"
)

# Subscription tenure in months
tenure_months = np.random.randint(1, 24, size=n_customers)

# Monthly charges (introduce some noise)
monthly_charges = np.round(np.random.normal(499, 120, n_customers), 2)
monthly_charges = np.clip(monthly_charges, 199, 999)

# Usage frequency (sessions per month)
usage_frequency = np.random.poisson(lam=8, size=n_customers).astype(float)

# Support tickets (complaints) raised
support_tickets = np.random.poisson(lam=1.5, size=n_customers).astype(float)

# Auto-renew status
auto_renew = np.random.choice([0, 1], size=n_customers, p=[0.35, 0.65])

# Payment method
payment_method = np.random.choice(
    ["UPI", "Credit Card", "Debit Card", "Net Banking"],
    size=n_customers,
    p=[0.4, 0.25, 0.2, 0.15]
)

# Contract type
contract_type = np.random.choice(
    ["Monthly", "Quarterly", "Yearly"],
    size=n_customers,
    p=[0.5, 0.3, 0.2]
)

# Base churn probability
churn_prob = (
    0.45
    - (usage_frequency * 0.03)
    + (support_tickets * 0.07)
    - (auto_renew * 0.25)
)

# Adjust churn based on contract
churn_prob += np.where(contract_type == "Monthly", 0.15, 0)
churn_prob += np.where(contract_type == "Yearly", -0.2, 0)

# Clip probabilities
churn_prob = np.clip(churn_prob, 0.05, 0.85)

# Final churn variable
churn = np.random.binomial(1, churn_prob)

# Introduce missing values intentionally
monthly_charges[np.random.choice(n_customers, 30, replace=False)] = np.nan
usage_frequency[np.random.choice(n_customers, 25, replace=False)] = np.nan
support_tickets[np.random.choice(n_customers, 20, replace=False)] = np.nan

# Create DataFrame
subscription_df = pd.DataFrame({
    "customer_id": customer_id,
    "start_date": start_date,
    "tenure_months": tenure_months,
    "monthly_charges": monthly_charges,
    "usage_frequency": usage_frequency,
    "support_tickets": support_tickets,
    "auto_renew": auto_renew,
    "payment_method": payment_method,
    "contract_type": contract_type,
    "churn": churn
})

subscription_df["start_date"] = pd.to_datetime(
    subscription_df["start_date"]
).dt.date

# Save dataset
subscription_df.to_csv(file_path, index=False)