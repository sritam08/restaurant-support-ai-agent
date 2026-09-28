import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str | None = Field(default=None)
    openai_model: str = "gpt-5.6-luna"
    agent_mode: str = "mock"
    rag_top_k: int = 3
    rag_min_score: float = 0.05
    tool_timeout_seconds: float = 5.0

@lru_cache
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        agent_mode=os.getenv("AGENT_MODE", "mock").lower(),
        rag_top_k=int(os.getenv("RAG_TOP_K", "3")),
        rag_min_score=float(os.getenv("RAG_MIN_SCORE", "0.05")),
        tool_timeout_seconds=float(os.getenv("TOOL_TIMEOUT_SECONDS", "5")),
    )
