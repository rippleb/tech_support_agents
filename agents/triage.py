from typing import Any, Dict
from .base import BaseAgent
from .system_prompts import SYSTEM_PROMPTS

class TriageAgent(BaseAgent):
    """
    Agent responsible for initial ticket triage: analyzes, categorizes, and assigns tickets.
    """
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.system_prompt = SYSTEM_PROMPTS["triage_agent"]

    async def receive_message(self, message: Any):
        """Handle incoming ticket: analyze, categorize, and assign."""
        ticket = message.payload.data.get("ticket")
        if not ticket:
            return {"error": "No ticket found in message."}
        # Create ticket in Freshdesk
        created = await self.call_mcp_tool("freshdesk", "create_ticket", ticket)
        # Analyze ticket with LLM
        analysis = await self.run_llm(f"Analyze and categorize this ticket: {ticket}")
        # For demo, pretend to extract category and assignee
        category = "software" if "software" in ticket.get("description", "").lower() else "hardware"
        assignee = "tech_support_agent" if category == "software" else "network_support_agent"
        # Add initial note
        await self.call_mcp_tool("freshdesk", "add_note", {"ticket_id": created.get("id", ticket.get("id")), "note": analysis})
        # Assign ticket (stub)
        assign_result = await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="assign_ticket",
            arguments={"ticket_id": created.get("id", ticket.get("id")), "assignee": assignee}
        )
        # Send update message (stub)
        await self.send_message(
            recipient_id=assignee,
            intent="ticket_assigned",
            data={"ticket": ticket, "category": category}
        )
        return {
            "analysis": analysis,
            "category": category,
            "assigned_to": assignee,
            "assign_result": assign_result
        } 