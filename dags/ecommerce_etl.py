from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def ingest_raw_data():

    import os
    import pandas as pd
    import mysql.connector
    import logging

    logger = logging.getLogger(__name__)

    conn = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="root123",
        database="ecommerce_data"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT file_name FROM processed_files"
    )

    processed_files = {
        row[0]
        for row in cursor.fetchall()
    }

    data_path = "/opt/airflow/data/raw_orders"

    files = [
        f
        for f in os.listdir(data_path)
        if f.endswith(".csv")
    ]

    total_rows = 0

    for file in files:

        if file in processed_files:
            logger.info(f"Skipping already processed file: {file}")
            continue

        logger.info(f"Processing file: {file}")

        full_path = os.path.join(
            data_path,
            file
        )

        df = pd.read_csv(full_path)

        for _, row in df.iterrows():

            if pd.isna(row["order_id"]):
                continue

            query = """
            INSERT INTO raw_orders
            (
                order_id,
                customer_id,
                product_name,
                item_price,
                quantity,
                order_date,
                load_timestamp
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,NOW()
            )
            ON DUPLICATE KEY UPDATE
                customer_id=VALUES(customer_id),
                product_name=VALUES(product_name),
                item_price=VALUES(item_price),
                quantity=VALUES(quantity),
                order_date=VALUES(order_date),
                load_timestamp=NOW()
            """

            cursor.execute(
                query,
                (
                    str(row["order_id"]),
                    str(row["customer_id"]),
                    str(row["product_name"]),
                    float(row["item_price"]),
                    int(row["quantity"]),
                    str(row["order_date"])
                )
            )

            total_rows += 1

        cursor.execute(
            """
            INSERT INTO processed_files
            (
                file_name,
                processed_at
            )
            VALUES
            (
                %s,
                NOW()
            )
            """,
            (file,)
        )

        conn.commit()

    logger.info(
        f"Rows loaded into raw_orders: {total_rows}"
    )

    cursor.close()
    conn.close()

def transform_and_validate_data():
    print("Transform task running")


def load_fact_data_incrementally():
    print("Load task running")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ecommerce_etl",
    start_date=datetime(2026, 6, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=ingest_raw_data,
    )

    transform_task = PythonOperator(
        task_id="transform_and_validate_data",
        python_callable=transform_and_validate_data,
    )

    load_task = PythonOperator(
        task_id="load_fact_data_incrementally",
        python_callable=load_fact_data_incrementally,
    )

    ingest_task >> transform_task >> load_task