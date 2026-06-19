import json
import mysql.connector
import pandas as pd

from data_validation import validate_record


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

    cursor = conn.cursor()

    invalid_count = 0

    for _, row in df.iterrows():

        record = row.to_dict()

        is_valid, error_message = validate_record(record)

        if not is_valid:

            cursor.execute(
                """
                INSERT INTO error_records
                (
                    source_data,
                    error_message,
                    detected_at
                )
                VALUES
                (
                    %s,
                    %s,
                    NOW()
                )
                """,
                (
                    json.dumps(record, default=str),
                    error_message
                )
            )

            invalid_count += 1

    conn.commit()

    print(f"Invalid records stored: {invalid_count}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()