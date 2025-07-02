import asyncio
import os
from utils.mcp import MCPClient
from utils.policy import OPAPolicyClient
from utils.audit_logging import AuditLogger
from agents.triage import TriageAgent
from agents.tech_support import TechnicalSupportAgent
from agents.network_support import NetworkSupportAgent
from agents.security import SecurityAgent
from agents.escalation_manager import EscalationManagerAgent
from agent_auth.credentials import CredentialStore
from a2a_collaboration.communication import A2ACommunicationBus
from typing import Dict, Any
import logging

# --- Config ---
FRESHDESK_TOOL_NAME = "freshdesk"
POLL_INTERVAL = int(os.getenv("TICKET_POLL_INTERVAL", 10000))  # seconds

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')
logger = logging.getLogger("demo_app")

# --- Setup dependencies ---
credential_store = CredentialStore()
communication_bus = A2ACommunicationBus(registry=None)  # Replace with real registry if needed
mcp_client = MCPClient()
policy_client = OPAPolicyClient()
audit_logger = AuditLogger()

# Dummy LLM config for demo
from agents.llm import LLMConfig, LLMProvider
llm_config = LLMConfig(provider=LLMProvider.GEMINI, model="gemini-pro", temperature=0.2)

# --- Instantiate agents ---
triage_agent = TriageAgent(
    agent_id="triage_agent",
    credential_store=credential_store,
    communication_bus=communication_bus,
    mcp_client=mcp_client,
    policy_client=policy_client,
    llm_config=llm_config,
    secret="triage_secret",
    audit_logger=audit_logger
)
tech_agent = TechnicalSupportAgent(
    agent_id="tech_support_agent",
    credential_store=credential_store,
    communication_bus=communication_bus,
    mcp_client=mcp_client,
    policy_client=policy_client,
    llm_config=llm_config,
    secret="tech_secret",
    audit_logger=audit_logger
)
network_agent = NetworkSupportAgent(
    agent_id="network_support_agent",
    credential_store=credential_store,
    communication_bus=communication_bus,
    mcp_client=mcp_client,
    policy_client=policy_client,
    llm_config=llm_config,
    secret="network_secret",
    audit_logger=audit_logger
)
security_agent = SecurityAgent(
    agent_id="security_agent",
    credential_store=credential_store,
    communication_bus=communication_bus,
    mcp_client=mcp_client,
    policy_client=policy_client,
    llm_config=llm_config,
    secret="security_secret",
    audit_logger=audit_logger
)
escalation_agent = EscalationManagerAgent(
    agent_id="escalation_manager",
    credential_store=credential_store,
    communication_bus=communication_bus,
    mcp_client=mcp_client,
    policy_client=policy_client,
    llm_config=llm_config,
    secret="escalation_secret",
    audit_logger=audit_logger
)

# --- Track processed tickets ---
processed_ticket_ids = set()

async def fetch_new_tickets() -> list:
    """Fetch new/unassigned tickets from Freshdesk via MCP."""
    try:
        logger.info("Fetching new/unassigned tickets from Freshdesk...")
        result = await mcp_client.call_tool(
            tool_name=FRESHDESK_TOOL_NAME,
            operation="list_tickets",
            arguments={"status": "open", "assigned": False}
        )
        tickets = result.get("tickets", []) if result else []
        logger.info(f"Fetched {len(tickets)} tickets from Freshdesk.")
        return tickets
    except Exception as e:
        logger.error(f"Failed to fetch tickets: {e}")
        return []

async def process_ticket(ticket: Dict[str, Any]):
    ticket_id = ticket.get("id")
    logger.info(f"Processing ticket {ticket_id}: {ticket.get('subject')}")
    try:
        triage_result = await triage_agent.receive_message(
            type("Msg", (), {"payload": type("Payload", (), {"data": {"ticket": ticket}})})()
        )
        logger.info(f"[TRIAGE] Ticket {ticket_id} categorized as {triage_result['category']} and assigned to {triage_result['assigned_to']}")
        processed_ticket_ids.add(ticket_id)
    except Exception as e:
        logger.error(f"Error processing ticket {ticket_id}: {e}")

async def main():
    logger.info("[DEMO] Starting IT Helpdesk Agent Orchestration Demo...")
    while True:
        tickets = await fetch_new_tickets()
        new_tickets = [t for t in tickets if t.get("id") not in processed_ticket_ids]
        if new_tickets:
            logger.info(f"Found {len(new_tickets)} new ticket(s) to process.")
        for ticket in new_tickets:
            await process_ticket(ticket)
        if not new_tickets:
            logger.info("No new tickets. Waiting...")
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main()) 