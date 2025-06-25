import pytest
import asyncio

from agents.triage import TriageAgent
from agents.tech_support import TechnicalSupportAgent
from agents.network_support import NetworkSupportAgent
from agents.security import SecurityAgent
from agents.escalation_manager import EscalationManagerAgent

class DummyDep:
    def __init__(self): pass
    def get_agent_credentials(self, agent_id): return ["dummy"]
    def create_credential(self, **kwargs): return "dummy"
    async def send_message(self, *a, **k): return "sent"
    async def call_mcp_tool(self, *a, **k): return {"result": "ok"}

@pytest.mark.asyncio
async def test_triage_agent():
    agent = TriageAgent("triage_agent", DummyDep(), DummyDep(), DummyDep(), secret="s")
    class Msg: pass
    msg = Msg(); msg.payload = Msg(); msg.payload.data = {"ticket": {"id": "1", "description": "software bug"}}
    result = await agent.receive_message(msg)
    assert "category" in result and result["assigned_to"] == "tech_support_agent"

@pytest.mark.asyncio
async def test_tech_support_agent():
    agent = TechnicalSupportAgent("tech_support_agent", DummyDep(), DummyDep(), DummyDep(), secret="s")
    class Msg: pass
    msg = Msg(); msg.payload = Msg(); msg.payload.data = {"ticket": {"id": "2", "description": "network down"}}
    result = await agent.receive_message(msg)
    assert result["consulted_network"] is True

@pytest.mark.asyncio
async def test_network_support_agent():
    agent = NetworkSupportAgent("network_support_agent", DummyDep(), DummyDep(), DummyDep(), secret="s")
    class Msg: pass
    msg = Msg(); msg.payload = Msg(); msg.payload.data = {"ticket": {"id": "3", "description": "router failure"}}
    result = await agent.receive_message(msg)
    assert "analysis" in result

@pytest.mark.asyncio
async def test_security_agent():
    agent = SecurityAgent("security_agent", DummyDep(), DummyDep(), DummyDep(), secret="s")
    class Msg: pass
    msg = Msg(); msg.payload = Msg(); msg.payload.data = {"ticket": {"id": "4", "description": "malware detected"}}
    result = await agent.receive_message(msg)
    assert result["coordinated_with"] == "escalation_manager"

@pytest.mark.asyncio
async def test_escalation_manager_agent():
    agent = EscalationManagerAgent("escalation_manager", DummyDep(), DummyDep(), DummyDep(), secret="s")
    class Msg: pass
    msg = Msg(); msg.payload = Msg(); msg.payload.data = {"ticket": {"id": "5", "description": "critical issue"}}
    result = await agent.receive_message(msg)
    assert "progress" in result 