-- 1️⃣ Overall Churn Rate (Baseline KPI)
-- Business question: How serious is the churn problem?
-- 📌 Why:
-- churn = 1 → churned
-- Average gives churn %
SELECT 
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions;



-- 2️⃣ Churn by Contract Type
-- Business question: Which plans are risky?
-- 📌 Insight: Monthly plans usually churn more
SELECT 
    contract_type,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions
GROUP BY contract_type;



-- 3️⃣ Churn by Auto-Renew Status
-- Business question: Does auto-renew actually reduce churn?
-- 📌 Business action: Push auto-renew adoption
SELECT 
    auto_renew,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions
GROUP BY auto_renew;



-- 4️⃣ Churn by Payment Method
-- Business question: Do payment failures affect churn?
-- 📌 Insight: UPI vs Card behavior differences
SELECT 
    payment_method,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions
GROUP BY payment_method;



-- 5️⃣ Usage Frequency: Churned vs Retained
-- Business question: Are inactive users leaving?
-- 📌 Classic retention insight: Low usage = high churn risk
SELECT 
    churn,
    ROUND(AVG(usage_frequency), 2) AS avg_usage
FROM subscriptions
GROUP BY churn;



-- 6️⃣ Support Tickets vs Churn
-- Business question: Are unhappy users leaving?
-- 📌 Insight: Complaints → churn
SELECT 
    churn,
    ROUND(AVG(support_tickets), 2) AS avg_tickets
FROM subscriptions
GROUP BY churn;



-- 7️⃣ Tenure Buckets vs Churn
-- Business question: When do customers leave?
-- 📌 Insight: Early churn detection window
SELECT 
    CASE
        WHEN tenure_months <= 3 THEN '0–3 months'
        WHEN tenure_months <= 6 THEN '4–6 months'
        WHEN tenure_months <= 12 THEN '7–12 months'
        ELSE '12+ months'
    END AS tenure_group,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions
GROUP BY tenure_group;



-- 8️⃣ High-Risk Customers (Operational Query)
-- Business question: Whom should we contact right now?
-- 📌 Actionable output: Feed this list to CRM / retention team
SELECT count(*) as high_risk
FROM subscriptions
WHERE 
    usage_frequency < 5
    AND support_tickets >= 3
    AND auto_renew = 0;



-- 9️⃣ Monthly Churn Trend (Cohort Prep)
-- Business question: Is churn improving over time?
-- 📌 Used later for: Cohort retention tables, Dashboards
SELECT 
    DATE_FORMAT(start_date, '%Y-%m') AS cohort_month,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_percent
FROM subscriptions
GROUP BY cohort_month
ORDER BY cohort_month;



-- 1️⃣0️⃣ Retention Rate (Inverse of Churn)
-- Business question: How many customers stay?
-- 📌 Management-friendly KPI
SELECT 
    ROUND((1 - AVG(churn)) * 100, 2) AS retention_rate_percent
FROM subscriptions;