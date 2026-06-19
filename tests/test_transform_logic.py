from etl_scripts.transform_logic import *
def test_total_order_value():

    result = calculate_total_order_value(
        100,
        2
    )

    assert result == 200
def test_product_name():

    result = standardize_product_name(
        "   laptop   "
    )

    assert result == "Laptop"