import json
from pathlib import Path
from app.utils.logger import log_event
from app.utils.validators import validate_order_id

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "orders.json"

def _load_orders() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def get_order_details(order_id: str) -> dict:
    try:
        order_id = validate_order_id(order_id)
    except ValueError as exc:
        return {"success": False, "error_code": "INVALID_ORDER_ID", "message": str(exc)}

    if order_id == "ORD-0000":
        log_event("tool_call", tool="get_order_details", success=False, reason="simulated_failure")
        return {"success": False, "error_code": "SERVICE_UNAVAILABLE", "message": "Order service is temporarily unavailable."}

    order = _load_orders().get(order_id)
    if not order:
        log_event("tool_call", tool="get_order_details", success=False, reason="not_found")
        return {"success": False, "error_code": "ORDER_NOT_FOUND", "message": "Order was not found."}

    log_event("tool_call", tool="get_order_details", success=True, order_id=order_id)
    return {"success": True, "data": order}

def get_order_status(order_id: str) -> dict:
    result = get_order_details(order_id)
    if not result["success"]:
        return result
    data = result["data"]
    return {
        "success": True,
        "data": {
            "order_id": data["order_id"],
            "status": data["status"],
            "estimated_delivery": data.get("estimated_delivery"),
        },
    }
