# Submission Checklist

## Required

- [x] FastAPI backend
- [x] Conversational agent endpoint
- [x] Conversation/session context
- [x] `get_order_status(order_id)`
- [x] `get_order_details(order_id)`
- [x] `create_support_ticket(...)`
- [x] Tool argument validation
- [x] Invalid order handling
- [x] Tool failure handling
- [x] Local knowledge base
- [x] Retrieval / RAG
- [x] RAG no-answer behavior
- [x] Complaint automation workflow
- [x] Payment/Order/Delivery/Refund/Technical categories
- [x] Low/Medium/High priority
- [x] Structured output validation
- [x] Security guardrails
- [x] Application-side authorization boundary
- [x] Logging
- [x] Tool success/failure logging
- [x] Idempotency for tickets
- [x] Failure-case documentation
- [x] `.env.example`
- [x] README
- [x] Architecture notes
- [x] Test prompts
- [x] Technical review answers

## Before GitHub submission

- [ ] Add a real API key only to local `.env`; never commit it
- [ ] Run `pytest -q`
- [ ] Run the API locally
- [ ] Test `/docs`
- [ ] Record a short demo
- [ ] Push repository
- [ ] Verify `.env` is not tracked
