create database subcriptions_analysis;

use subcriptions_analysis;

CREATE TABLE subscriptions (
    customer_id INT PRIMARY KEY,
    start_date DATE,
    tenure_months INT,
    monthly_charges DECIMAL(8,2),
    usage_frequency FLOAT,
    support_tickets FLOAT,
    auto_renew TINYINT(1),
    payment_method VARCHAR(50),
    contract_type VARCHAR(20),
    churn TINYINT(1)
);

select * from subscriptions;