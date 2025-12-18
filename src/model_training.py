import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report

# Create models directory
os.makedirs("models", exist_ok=True)

# Load feature-engineered data
X = pd.read_csv("data/processed/X_features.csv")
y = pd.read_csv("data/processed/y_target.csv").values.ravel()

# Ensure all features are numeric
X = X.select_dtypes(include=["number"])
print(X.dtypes)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# Train Logistic Regression model
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

# Predictions
y_pred = log_model.predict(X_test)
y_pred_proba = log_model.predict_proba(X_test)[:, 1]

# Evaluation
print("Model Evaluation Metrics")
print("-" * 40)
print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall   : {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score : {f1_score(y_test, y_pred):.4f}")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Feature Importance
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "coefficient": log_model.coef_[0]
}).sort_values(by="coefficient", ascending=False)

print("\nFeature Importance:", feature_importance)

# Save trained model
joblib.dump(log_model, "models/logistic_churn_model.pkl")

# Risk Segmentation using churn probability
X_test_copy = X_test.copy()
X_test_copy["churn_probability"] = y_pred_proba

X_test_copy["risk_segment"] = pd.cut(
    X_test_copy["churn_probability"],
    bins=[0, 0.3, 0.6, 1],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)

print("\nRisk Segment Distribution:", X_test_copy["risk_segment"].value_counts())

from sklearn.metrics import precision_recall_fscore_support

precision, recall, f1, _ = precision_recall_fscore_support(
    y_test, y_pred, average=None
)

metrics_df = pd.DataFrame({
    "Class": ["Retained (0)", "Churned (1)"],
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1
})
print("\nClass-wise Metrics:\n", metrics_df)

custom_threshold = 0.35
y_pred_custom = (y_pred_proba >= custom_threshold).astype(int)
print(classification_report(y_test, y_pred_custom))

conf = confusion_matrix(y_test, y_pred_custom)
tn, fp, fn, tp = conf.ravel()
total_cost = (fn * 2000) + (fp * 300)
print(f"\nTotal Cost with custom threshold {custom_threshold}: ${total_cost}")

risk_bins = [0, 0.25, 0.5, 0.75, 1]
risk_labels = ["Very Low", "Low", "Medium", "High"]
X_test_copy["risk_bucket"] = pd.cut(
    X_test_copy["churn_probability"],
    bins=risk_bins,
    labels=risk_labels
)
print("\nRisk Bucket Distribution:", X_test_copy["risk_bucket"].value_counts())