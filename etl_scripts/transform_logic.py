import pandas as pd


def standardize_product_name(product_name):

    if pd.isna(product_name):
        return None

    return str(product_name).strip().title()


def calculate_total_order_value(item_price, quantity):

    return round(
        float(item_price) * int(quantity),
        2
    )


def transform_dataframe(df):

    transformed = df.copy()

    transformed["product_name"] = (
        transformed["product_name"]
        .apply(standardize_product_name)
    )

    transformed["total_order_value"] = (
        transformed["item_price"].astype(float)
        * transformed["quantity"].astype(int)
    )

    transformed["total_order_value"] = (
        transformed["total_order_value"]
        .round(2)
    )

    return transformed