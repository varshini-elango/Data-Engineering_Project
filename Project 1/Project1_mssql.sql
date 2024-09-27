create database Project1

CREATE TABLE user_dim (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    location VARCHAR(255),
    account_creation_date DATE
);

CREATE TABLE transaction_fact (
    transaction_id INT PRIMARY KEY,
    user_id INT,
    transaction_amount DECIMAL(10, 2),
    transaction_time TIMESTAMP,
    payment_method VARCHAR(50),
    location VARCHAR(255),
    fraud_label BIT,
    FOREIGN KEY (user_id) REFERENCES user_dim(user_id)
);

CREATE TABLE fraud_indicators (
    rule_id INT PRIMARY KEY,
    description VARCHAR(255),
    risk_score INT CHECK (risk_score BETWEEN 1 AND 10) -- 1 = Low Risk, 10 = High Risk
);

--calculates the average transaction amount and total transactions.
SELECT u.user_id,u.user_name,
COUNT(t.transaction_id) AS total_transactions,
AVG(t.transaction_amount) AS avg_transaction_amount
FROM transaction_fact t
JOIN user_dim u ON t.user_id = u.user_id
GROUP BY u.user_id, u.user_name;

--transactions higher than user's average transaction amount.
WITH UserAverage AS (SELECT user_id, AVG(transaction_amount) AS avg_amount 
FROM transaction_fact 
GROUP BY user_id)
SELECT t.user_id,t.transaction_id,t.transaction_amount,t.transaction_time
FROM transaction_fact t
JOIN UserAverage ua ON t.user_id = ua.user_id
WHERE t.transaction_amount > ua.avg_amount * 3
ORDER BY t.transaction_amount DESC;

--assigns a fraud risk score to transactions.
SELECT t.transaction_id,t.user_id,t.transaction_amount,t.transaction_time,
CASE
WHEN t.transaction_amount > 1000 THEN 8
WHEN t.payment_method = 'Credit Card' AND t.transaction_amount > 500 THEN 7
WHEN t.location != u.location THEN 6
ELSE 3
END AS fraud_risk_score
FROM transaction_fact t
JOIN user_dim u ON t.user_id = u.user_id
ORDER BY fraud_risk_score DESC;


SELECT * FROM user_dim;
SELECT * FROM transaction_fact;
SELECT * FROM fraud_indicators;
