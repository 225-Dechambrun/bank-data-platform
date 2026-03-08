# Bank Data Platform

Bank Data Platform est un projet de Data Engineering qui simule une plateforme de données bancaire de bout en bout.

## Objectif

Construire un pipeline de données capable de :

- ingérer des données bancaires depuis des fichiers CSV
- charger les données brutes dans PostgreSQL
- transformer les données en modèle analytique
- calculer des KPI métier
- orchestrer le pipeline avec Airflow
- exposer les KPI via une API FastAPI

## Architecture

CSV files
   ¦
   ?
Airflow DAG
(load_raw_data.py)
   ¦
   ?
PostgreSQL raw tables
(customers_raw, accounts_raw, transactions_raw)
   ¦
   ?
SQL warehouse
(dim_customers, dim_accounts, dim_date, fact_transactions)
   ¦
   ?
KPI views
(vw_daily_kpi, vw_kpi_by_type, vw_kpi_by_customer)
   ¦
   ?
FastAPI
(/kpi/by-type, /kpi/daily, /kpi/top-customers)

## Technologies utilisées

- Python
- PostgreSQL
- Docker
- Apache Airflow
- FastAPI
- SQL
- Git / GitHub

## Volumétrie des données

- 200 clients
- 300 comptes
- 10000 transactions

## API

Documentation :

http://localhost:8000/docs

Endpoints disponibles :

GET /kpi/by-type  
GET /kpi/daily  
GET /kpi/top-customers  

## Lancer le projet

Démarrer les services :

docker compose up -d

Générer les données :

python generate_data.py

Déclencher le pipeline :

docker exec -it airflow_scheduler airflow dags trigger bank_pipeline

## Auteur

Stephane Dechambrun
