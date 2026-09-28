from app.tools.order_tools import get_order_details, get_order_status

def test_known_order_status():
    result = get_order_status("ORD-1005")
    assert result["success"] is True
    assert result["data"]["status"] == "Out for Delivery"

def test_unknown_order():
    result = get_order_status("ORD-9999")
    assert result["success"] is False
    assert result["error_code"] == "ORDER_NOT_FOUND"

def test_invalid_order_id():
    result = get_order_details("hello")
    assert result["success"] is False
    assert result["error_code"] == "INVALID_ORDER_ID"
