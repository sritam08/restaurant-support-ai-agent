# Technical Review Questions — Prepared Answers

## 1. When should the agent answer directly and when should it call a tool?

The agent can answer directly when the answer is static and supported by the knowledge base. It should call a tool when the request needs authoritative or current operational information, such as an order status or order details. Ticket creation should always go through the application tool.

## 2. How do you prevent the LLM from hallucinating an order status?

Order status is never generated from the model's memory. The application exposes `get_order_status(order_id)`. The response is based on the tool result. If the tool fails or the order is not found, the agent reports that state instead of inventing a status.

## 3. How does your RAG pipeline select relevant knowledge?

The local retriever converts knowledge-base documents and the query into TF-IDF vectors and ranks them using cosine similarity. Only documents above the configured relevance threshold are returned to the agent.

## 4. What happens when retrieved documents contain conflicting information?

The current demo uses a small controlled knowledge base, so conflicting policy documents are treated as a data-quality problem rather than something the model should silently resolve. A production implementation should attach document version/effective-date metadata and apply deterministic precedence rules. If a conflict cannot be resolved safely, the agent should escalate or state that the documented sources conflict.

## 5. How would you protect the agent against prompt injection from users or retrieved documents?

The system prompt treats retrieved documents as data, not instructions. Application-side authorization controls sensitive operations. Tool arguments are validated, and arbitrary code, SQL, shell commands and unrelated customer-data retrieval are not exposed as tools.

## 6. Which decisions should never be left solely to an LLM?

Authorization, access to another customer's data, financial actions, irreversible operations, secret handling, and critical business-rule enforcement should be deterministic application decisions.

## 7. How do you prevent duplicate support tickets if an agent retries a failed workflow?

The workflow generates an idempotency key and the ticket store checks whether that key was already processed. If it exists, the existing ticket is returned rather than creating another ticket.

## 8. How would you evaluate whether the agent is improving or regressing after prompt/model changes?

Create a fixed evaluation set containing user prompts, expected tool calls, expected refusal behavior, expected grounding behavior and expected structured outputs. Run it on every important prompt/model change and compare results.

## 9. How would you scale this architecture for thousands of restaurant conversations?

Move session state to Redis or a database, replace JSON operational storage with a database/service, use a production vector database, run multiple FastAPI workers, add authentication/rate limiting, use asynchronous queues for notifications, and add distributed tracing and evaluation monitoring.
