from etl_scripts.data_validation import *


def test_valid_price():
    assert validate_price(100)[0] is True


def test_negative_price():
    assert validate_price(-100)[0] is False


def test_valid_quantity():
    assert validate_quantity(5)[0] is True


def test_invalid_quantity():
    assert validate_quantity(0)[0] is False


def test_valid_order_id():
    assert validate_order_id("123")[0] is True


def test_invalid_order_id():
    assert validate_order_id(None)[0] is False