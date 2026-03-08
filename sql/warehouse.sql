DROP VIEW IF EXISTS vw_daily_kpi;
DROP VIEW IF EXISTS vw_kpi_by_type;
DROP VIEW IF EXISTS vw_kpi_by_customer;

DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_accounts;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_customers AS
SELECT customer_id, name, age, country
FROM customers_raw;

CREATE TABLE dim_accounts AS
SELECT account_id, customer_id, type, balance
FROM accounts_raw;

CREATE TABLE dim_date AS
SELECT DISTINCT
    date AS transaction_date,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(DAY FROM date) AS day
FROM transactions_raw;

CREATE TABLE fact_transactions AS
SELECT
    t.transaction_id,
    t.account_id,
    a.customer_id,
    t.amount,
    t.type,
    t.date,
    a.balance
FROM transactions_raw t
JOIN accounts_raw a
    ON t.account_id = a.account_id;

CREATE VIEW vw_daily_kpi AS
SELECT
    date,
    COUNT(*) AS nb_transactions,
    SUM(amount) AS montant_total,
    AVG(amount) AS montant_moyen
FROM fact_transactions
GROUP BY date
ORDER BY date;

CREATE VIEW vw_kpi_by_type AS
SELECT
    type,
    COUNT(*) AS nb_transactions,
    SUM(amount) AS montant_total,
    AVG(amount) AS montant_moyen
FROM fact_transactions
GROUP BY type
ORDER BY montant_total DESC;

CREATE VIEW vw_kpi_by_customer AS
SELECT
    customer_id,
    COUNT(*) AS nb_transactions,
    SUM(amount) AS montant_total,
    AVG(amount) AS montant_moyen
FROM fact_transactions
GROUP BY customer_id
ORDER BY montant_total DESC;
