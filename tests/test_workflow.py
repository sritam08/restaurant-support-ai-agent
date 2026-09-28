from app.workflows.complaint_workflow import run_complaint_workflow

def test_payment_complaint_escalates():
    result = run_complaint_workflow("My payment was deducted but my order failed.", "test-session")
    assert result["classification"]["category"] == "Payment"
    assert result["classification"]["priority"] == "High"
    assert result["classification"]["requires_escalation"] is True
    assert result["ticket"]["success"] is True

def test_ticket_creation_is_idempotent():
    message = "My payment was deducted but my order failed."
    first = run_complaint_workflow(message, "idempotent-session")
    second = run_complaint_workflow(message, "idempotent-session")
    assert first["ticket"]["data"]["ticket_id"] == second["ticket"]["data"]["ticket_id"]
    assert second["ticket"]["duplicate"] is True
