import hashlib
import json
from pathlib import Path
from threading import Lock
from app.agent.schemas import Category, Priority, Ticket
from app.utils.logger import log_event

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "tickets.json"
LOCK = Lock()

def _load() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def _save(items: list[dict]) -> None:
    DATA_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")

def create_support_ticket(
    category: Category,
    priority: Priority,
    description: str,
    session_id: str,
    idempotency_key: str,
) -> dict:
    if not description.strip():
        return {"success": False, "error_code": "INVALID_DESCRIPTION", "message": "Description is required."}
    if not idempotency_key.strip():
        return {"success": False, "error_code": "MISSING_IDEMPOTENCY_KEY", "message": "Idempotency key is required."}

    with LOCK:
        items = _load()
        for item in items:
            if item["idempotency_key"] == idempotency_key:
                log_event("ticket_duplicate_prevented", ticket_id=item["ticket_id"])
                return {"success": True, "data": item, "duplicate": True}

        digest = hashlib.sha256(idempotency_key.encode()).hexdigest()[:8].upper()
        ticket_id = f"TKT-{digest}"

        ticket = Ticket(
            ticket_id=ticket_id,
            category=category,
            priority=priority,
            description=description.strip(),
            session_id=session_id,
            idempotency_key=idempotency_key,
        ).model_dump()

        items.append(ticket)
        _save(items)

    log_event("ticket_created", ticket_id=ticket_id, category=category, priority=priority)
    return {"success": True, "data": ticket, "duplicate": False}
