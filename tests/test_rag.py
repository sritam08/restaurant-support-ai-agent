from pathlib import Path
from app.rag.retriever import LocalRetriever

def test_policy_retrieval():
    retriever = LocalRetriever(Path("data/knowledge_base"), top_k=3, min_score=0.01)
    results = retriever.search("Can I cancel after preparation starts?")
    assert results
    assert any("cancellation" in item["source"] for item in results)

def test_unknown_query_can_return_no_relevant_document():
    retriever = LocalRetriever(Path("data/knowledge_base"), top_k=3, min_score=0.90)
    results = retriever.search("quantum satellite insurance")
    assert results == []
