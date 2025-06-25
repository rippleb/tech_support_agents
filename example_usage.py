import asyncio
from agent_auth.credentials import CredentialStore
from a2a_collaboration.communication import A2ACommunicationBus
from mcp_proxy.proxy import MCPProxy

from agents.triage import TriageAgent
from agents.tech_support import TechnicalSupportAgent
from agents.network_support import NetworkSupportAgent
from agents.security import SecurityAgent
from agents.escalation_manager import EscalationManagerAgent

# Mocked dependencies (replace with real ones in your app)
class DummyDep:
    def __init__(self): pass
    def get_agent_credentials(self, agent_id): return ["dummy"]
    def create_credential(self, **kwargs): return "dummy"
    async def send_message(self, *a, **k): return "sent"
    async def call_mcp_tool(self, *a, **k): return {"result": "ok"}

credential_store = DummyDep()
communication_bus = DummyDep()
mcp_proxy = DummyDep()

# Instantiate agents
triage_agent = TriageAgent("triage_agent", credential_store, communication_bus, mcp_proxy, secret="triage_secret")
tech_agent = TechnicalSupportAgent("tech_support_agent", credential_store, communication_bus, mcp_proxy, secret="tech_secret")
network_agent = NetworkSupportAgent("network_support_agent", credential_store, communication_bus, mcp_proxy, secret="network_secret")
security_agent = SecurityAgent("security_agent", credential_store, communication_bus, mcp_proxy, secret="security_secret")
escalation_agent = EscalationManagerAgent("escalation_manager", credential_store, communication_bus, mcp_proxy, secret="escalation_secret")

async def main():
    # Simulate a new ticket message
    ticket = {"id": "T123", "description": "User cannot connect to WiFi. Suspect network issue."}
    class Msg: pass
    message = Msg(); message.payload = Msg(); message.payload.data = {"ticket": ticket}

    # Triage agent receives the ticket
    triage_result = await triage_agent.receive_message(message)
    print("TriageAgent result:", triage_result)

    # Technical support agent receives the ticket
    tech_result = await tech_agent.receive_message(message)
    print("TechnicalSupportAgent result:", tech_result)

    # Network support agent receives the ticket
    network_result = await network_agent.receive_message(message)
    print("NetworkSupportAgent result:", network_result)

    # Security agent receives a security ticket
    sec_ticket = {"id": "T124", "description": "Suspicious login detected."}
    sec_message = Msg(); sec_message.payload = Msg(); sec_message.payload.data = {"ticket": sec_ticket}
    security_result = await security_agent.receive_message(sec_message)
    print("SecurityAgent result:", security_result)

    # Escalation manager receives a ticket
    escalation_result = await escalation_agent.receive_message(message)
    print("EscalationManagerAgent result:", escalation_result)

if __name__ == "__main__":
    asyncio.run(main()) 