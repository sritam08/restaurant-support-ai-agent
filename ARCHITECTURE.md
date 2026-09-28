# Architecture Notes

## 1. Goal

The system is a Restaurant Support & Operations Agent. It handles customer support conversations, retrieves documented restaurant policy, retrieves authoritative order data through tools, and escalates complaints through a structured workflow.

## 2. Request routing

```text
User message
   |
   +-- policy / FAQ --> RAG
   |
   +-- order status --> get_order_status
   |
   +-- order details --> get_order_details
   |
   +-- complaint --> complaint workflow
   |
   +-- unauthorized data request --> deny
```

The LLM can decide which tool to call in LLM mode. The application remains responsible for validating tool arguments, enforcing authorization and executing the tool.

## 3. Separation of concerns

### Agent layer
Natural-language interpretation, tool selection and final response.

### Tool layer
Order retrieval and ticket creation. It owns input validation and operational results.

### RAG layer
Retrieves documented policy/FAQ content and applies a relevance threshold.

### Workflow layer
Classifies complaints, validates structured output, applies business rules, escalates and uses idempotency.

### API layer
HTTP validation, endpoint routing, session handling and exception boundaries.

## 4. Why deterministic rules exist outside the LLM

Sensitive decisions must not depend solely on natural-language model instructions. Examples:

- Order IDs must match the expected format.
- Only an authorized order can be accessed.
- Ticket priority must be one of Low/Medium/High.
- Duplicate ticket creation must be prevented using an idempotency key.
- A failed order API must not become an invented status.

## 5. RAG

The assessment allows a vector database, local vector store, or another justified retrieval approach. This project uses local TF-IDF retrieval because the knowledge base is intentionally small.

Production upgrade path:

```text
TF-IDF
  ↓
Embedding model
  ↓
Vector database
  ↓
Metadata filtering
  ↓
Reranking
```

## 6. Tool failure behavior

Tools return structured results with `success`, `error_code`, and data fields. A failed tool result is reported instead of being converted into an unsupported operational claim.

## 7. Observability

Each request logs request/session ID, event type, tool name where applicable, success/failure and non-sensitive metadata. Secrets and API keys are not logged.

## 8. Idempotency

Ticket creation accepts an idempotency key. The ticket store checks whether that key was already processed and returns the existing ticket on a retry.

## 9. Scalability path

For thousands of conversations:

- move session state to Redis/PostgreSQL
- replace JSON operational storage with a database/service
- use a production vector database
- run FastAPI behind multiple workers
- add distributed tracing
- add rate limiting/authentication
- use a queue for asynchronous notifications
- add automated evaluation and regression tests
