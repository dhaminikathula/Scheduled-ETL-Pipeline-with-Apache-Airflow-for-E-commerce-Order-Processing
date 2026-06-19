# 🚀 Scheduled ETL Pipeline with Apache Airflow for E-Commerce Order Processing

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![Airflow](https://img.shields.io/badge/Apache-Airflow-red?style=for-the-badge\&logo=apacheairflow)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge\&logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge\&logo=docker)
![Pytest](https://img.shields.io/badge/Tested-Pytest-green?style=for-the-badge\&logo=pytest)

</p>

---

## 📖 Overview

A production-style **ETL (Extract, Transform, Load) Pipeline** built using **Apache Airflow**, **MySQL**, **Docker**, and **Python** to automate e-commerce order processing.

The pipeline extracts raw order data from CSV files, validates business rules, quarantines invalid records, transforms clean data, and loads analytics-ready information into a warehouse-style fact table.

---

## 🎯 Key Features

✨ Automated workflow orchestration with Apache Airflow

✨ Incremental file processing

✨ Data validation & quality checks

✨ Invalid record quarantine

✨ Business data transformation

✨ Fact table loading

✨ Dockerized deployment

✨ Unit tested ETL components

✨ Production-ready architecture

---

# 🏗️ Architecture

```text
                  ┌────────────────────┐
                  │  Raw CSV Files     │
                  └──────────┬─────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │  Airflow DAG       │
                  │ ingest_raw_data()  │
                  └──────────┬─────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │   raw_orders       │
                  └──────────┬─────────┘
                             │
                             ▼
           ┌───────────────────────────────────┐
           │ transform_and_validate_data()     │
           └───────┬─────────────────────┬─────┘
                   │                     │
                   ▼                     ▼
         ┌────────────────┐    ┌────────────────┐
         │ Valid Records  │    │ Invalid Records│
         └───────┬────────┘    └───────┬────────┘
                 │                     │
                 ▼                     ▼
      ┌────────────────────┐   ┌──────────────────┐
      │   fact_orders      │   │  error_records   │
      └────────────────────┘   └──────────────────┘
```

---

# ⚙️ Tech Stack

| Category               | Technology     |
| ---------------------- | -------------- |
| Workflow Orchestration | Apache Airflow |
| Database               | MySQL 8        |
| Language               | Python 3.12    |
| Data Processing        | Pandas         |
| Data Generation        | Faker          |
| Containerization       | Docker         |
| Testing                | Pytest         |
| Version Control        | Git & GitHub   |

---

# 📂 Project Structure

```bash
.
├── dags/
│   └── ecommerce_etl.py
│
├── data/
│   └── raw_orders/
│
├── etl_scripts/
│   ├── data_generator.py
│   ├── data_validation.py
│   ├── transform_logic.py
│   ├── load_fact.py
│   └── error_loader.py
│
├── sql/
│   ├── create_tables.sql
│   └── initial_airflow_setup.sql
│
├── tests/
│   ├── test_data_validation.py
│   └── test_transform_logic.py
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🔄 ETL Workflow

## 1️⃣ Extract

Generate synthetic e-commerce orders using Faker.

```python
order_id, customer_id, product_name,
item_price, quantity, order_date
```

---

## 2️⃣ Load Raw Data

Loads CSV records into:

```sql
raw_orders
```

Features:

* Incremental loading
* Duplicate prevention
* File tracking

---

## 3️⃣ Validate Data

Validation Rules:

✅ Order ID cannot be null

✅ Item Price must be positive

✅ Quantity must be positive

✅ Order Date must be valid

Invalid records are redirected to:

```sql
error_records
```

---

## 4️⃣ Transform Data

Business transformations:

```python
total_order_value = item_price * quantity
```

Product names are standardized for consistency.

---

## 5️⃣ Load Fact Table

Validated records are loaded into:

```sql
fact_orders
```

Features:

* Incremental warehouse loading
* Idempotent processing
* Duplicate protection

---

# 🗄️ Database Tables

## raw_orders

Stores incoming source data.

| Column         |
| -------------- |
| order_id       |
| customer_id    |
| product_name   |
| item_price     |
| quantity       |
| order_date     |
| load_timestamp |

---

## fact_orders

Stores transformed analytical data.

| Column              |
| ------------------- |
| order_sk            |
| order_id            |
| customer_id         |
| product_name        |
| total_order_value   |
| order_date          |
| processed_timestamp |

---

## error_records

Stores invalid records and validation errors.

| Column        |
| ------------- |
| error_id      |
| source_data   |
| error_message |
| detected_at   |

---

# 📊 Pipeline Results

| Metric               | Count |
| -------------------- | ----- |
| Raw Orders Processed | 510   |
| Valid Records        | 500   |
| Invalid Records      | 10    |
| Processed Files      | 5     |

### Validation Summary

```text
Valid Records   : 500
Invalid Records : 10
Success Rate    : 98.04%
```

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Result:

```text
8 PASSED
```

---

# 🐳 Run with Docker

Start services:

```bash
docker compose up -d
```

Verify containers:

```bash
docker compose ps
```

Access Airflow:

```text
http://localhost:8080
```

---

# 📈 Airflow DAG

```text
ingest_raw_data
        ↓
transform_and_validate_data
        ↓
load_fact_data_incrementally
```

### DAG Features

* Daily scheduling
* Retry mechanism
* Logging
* Dependency management
* Fault tolerance

---

# 🏆 Highlights

✔ End-to-End ETL Pipeline

✔ Apache Airflow Workflow Automation

✔ Data Validation Framework

✔ Error Quarantine Mechanism

✔ Incremental Data Loading

✔ Dockerized Deployment

✔ Unit Tested Components

✔ Production-Ready Architecture

---

# 🚀 Future Enhancements

* Airflow Email Alerts
* Data Quality Dashboard
* CI/CD with GitHub Actions
* AWS Deployment
* Monitoring & Observability
* Data Lineage Tracking

---

# 👨‍💻 Author

**Dhamini Kathula**

Data Engineering Project built using Apache Airflow, MySQL, Docker, and Python.

⭐ Star this repository if you found it useful!
