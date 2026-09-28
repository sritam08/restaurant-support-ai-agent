from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent.agent import Agent
from app.agent.schemas import ChatRequest, ChatResponse, ComplaintRequest
from app.tools.order_tools import get_order_details, get_order_status
from app.tools.ticket_tools import create_support_ticket
from app.workflows.complaint_workflow import run_complaint_workflow

app = FastAPI(
    title="Restaurant Support & Operations AI Agent",
    version="1.0.0",
    description="Assessment project demonstrating an AI support agent with tools, RAG and automation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()

@app.get("/health")
def health():
    return {"status": "ok", "agent_mode": "llm" if agent.client else "mock"}

@app.post("/api/agent/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = agent.chat(request.session_id, request.message)
    return ChatResponse(session_id=request.session_id, response=result["response"], tool_calls=result["tool_calls"], sources=result["sources"])

@app.get("/api/orders/{order_id}")
def order_details(order_id: str):
    return get_order_details(order_id)

@app.get("/api/orders/{order_id}/status")
def order_status(order_id: str):
    return get_order_status(order_id)

@app.post("/api/support/tickets")
def support_ticket(payload: dict):
    return create_support_ticket(**payload)

@app.post("/api/workflows/complaint")
def complaint_workflow(request: ComplaintRequest):
    return run_complaint_workflow(message=request.message, session_id=request.session_id)
