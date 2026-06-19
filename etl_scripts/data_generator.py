from datetime import datetime


def validate_order_id(order_id):
    if order_id is None:
        return False, "order_id is null"

    if str(order_id).strip() == "":
        return False, "order_id is empty"

    return True, None


def validate_price(price):
    try:
        price = float(price)

        if price <= 0:
            return False, "item_price must be positive"

        return True, None

    except Exception:
        return False, "invalid item_price"


def validate_quantity(quantity):
    try:
        quantity = int(quantity)

        if quantity <= 0:
            return False, "quantity must be positive"

        return True, None

    except Exception:
        return False, "invalid quantity"


def validate_order_date(order_date):
    try:

        if isinstance(order_date, datetime):
            return True, None

        datetime.fromisoformat(str(order_date))

        return True, None

    except Exception:
        return False, "invalid order_date"


def validate_record(record):

    validators = [
        validate_order_id(record.get("order_id")),
        validate_price(record.get("item_price")),
        validate_quantity(record.get("quantity")),
        validate_order_date(record.get("order_date"))
    ]

    errors = []

    for valid, message in validators:
        if not valid:
            errors.append(message)

    if errors:
        return False, "; ".join(errors)

    return True, None