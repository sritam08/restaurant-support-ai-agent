from app.agent.agent import Agent

def test_mock_chat_order_status():
    agent = Agent()
    result = agent.chat("chat-session", "Where is my order ORD-1005?")
    assert "Out for Delivery" in result["response"]
    assert "get_order_status" in result["tool_calls"]
