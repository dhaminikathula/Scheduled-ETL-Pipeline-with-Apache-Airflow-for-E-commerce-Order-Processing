import mysql.connector
import pandas as pd

from data_validation import validate_record
from transform_logic import transform_dataframe


def main():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="ecommerce_data"
    )

    query = """
    SELECT
        order_id,
        customer_id,
        product_name,
        item_price,
        quantity,
        order_date
    FROM raw_orders
    """

    df = pd.read_sql(query, conn)

    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():

        record = row.to_dict()

        is_valid, error_message = validate_record(record)

        if is_valid:
            valid_rows.append(record)

        else:
            invalid_rows.append(
                {
                    "record": str(record),
                    "error": error_message
                }
            )

    print(f"Valid records: {len(valid_rows)}")
    print(f"Invalid records: {len(invalid_rows)}")

    if len(valid_rows) == 0:
        print("No valid records found.")
        conn.close()
        return

    valid_df = pd.DataFrame(valid_rows)

    transformed_df = transform_dataframe(valid_df)

    cursor = conn.cursor()

    for _, row in transformed_df.iterrows():

        cursor.execute(
            """
            INSERT INTO fact_orders
            (
                order_id,
                customer_id,
                product_name,
                total_order_value,
                order_date,
                processed_timestamp
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
            ON DUPLICATE KEY UPDATE
                customer_id = VALUES(customer_id),
                product_name = VALUES(product_name),
                total_order_value = VALUES(total_order_value),
                order_date = VALUES(order_date),
                processed_timestamp = NOW()
            """,
            (
                row["order_id"],
                row["customer_id"],
                row["product_name"],
                float(row["total_order_value"]),
                row["order_date"]
            )
        )

    conn.commit()

    print(
        f"Loaded {len(transformed_df)} rows into fact_orders"
    )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()