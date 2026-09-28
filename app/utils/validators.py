import re
ORDER_ID_RE = re.compile(r"^ORD-\d{4}$")

def validate_order_id(order_id: str) -> str:
    order_id = order_id.strip().upper()
    if not ORDER_ID_RE.fullmatch(order_id):
        raise ValueError("Invalid order ID format. Expected ORD-1234.")
    return order_id
