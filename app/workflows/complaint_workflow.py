import hashlib
import re
from app.agent.schemas import ComplaintClassification
from app.tools.ticket_tools import create_support_ticket
from app.utils.logger import log_event

CATEGORY_PATTERNS = {
    "Payment": r"payment|paid|deducted|charged|transaction|card",
    "Delivery": r"delivery|late|delayed|driver|arrive",
    "Refund": r"refund|money back|cancel|cancellation",
    "Order": r"order|missing|wrong item|incorrect",
    "Technical": r"app|website|login|technical|error|bug",
}
HIGH_PRIORITY_PATTERNS = r"deducted.*failed|payment.*failed|fraud|double charged|not received.*paid"

def classify_deterministically(message: str) -> ComplaintClassification:
    lower = message.lower()
    category = "Technical"
    for candidate, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, lower):
            category = candidate
            break

    priority = "High" if re.search(HIGH_PRIORITY_PATTERNS, lower) else "Medium"
    if any(word in lower for word in ["thank", "great", "good"]):
        sentiment = "Positive"
    elif any(word in lower for word in ["bad", "angry", "terrible", "failed", "wrong", "deducted"]):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    requires_escalation = category in {"Payment", "Refund"} or priority == "High"
    return ComplaintClassification(
        category=category,
        priority=priority,
        sentiment=sentiment,
        requires_escalation=requires_escalation,
        summary=message[:500],
    )

def run_complaint_workflow(message: str, session_id: str, classifier=None) -> dict:
    classification = classifier(message) if classifier else classify_deterministically(message)

    if classification.category in {"Payment", "Refund"}:
        classification = classification.model_copy(update={"requires_escalation": True})

    idempotency_key = hashlib.sha256(
        f"{session_id}:{message.strip().lower()}".encode()
    ).hexdigest()

    ticket = None
    if classification.requires_escalation:
        ticket = create_support_ticket(
            category=classification.category,
            priority=classification.priority,
            description=classification.summary,
            session_id=session_id,
            idempotency_key=idempotency_key,
        )

    result = {"classification": classification.model_dump(), "ticket": ticket}
    log_event(
        "complaint_workflow",
        session_id=session_id,
        category=classification.category,
        priority=classification.priority,
        escalated=classification.requires_escalation,
    )
    return result
