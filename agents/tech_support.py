from typing import Any, Dict
from .base import BaseAgent
from .system_prompts import SYSTEM_PROMPTS

class TechnicalSupportAgent(BaseAgent):
    """
    Agent for hardware/software troubleshooting. Can consult NetworkSupportAgent.
    """
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.system_prompt = SYSTEM_PROMPTS["tech_support_agent"]

    async def receive_message(self, message: Any):
        ticket = message.payload.data.get("ticket")
        if not ticket:
            return {"error": "No ticket found in message."}
        # Analyze ticket with LLM
        analysis = await self.run_llm(f"Troubleshoot this ticket: {ticket}")
        # If network issue detected, consult NetworkSupportAgent
        if "network" in ticket.get("description", "").lower():
            consult_result = await self.send_message(
                recipient_id="network_support_agent",
                intent="consult",
                data={"ticket": ticket}
            )
        else:
            consult_result = None
        # Update ticket status
        update_result = await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="update_ticket_status",
            arguments={"ticket_id": ticket.get("id"), "status": "in_progress"}
        )
        # Add troubleshooting note
        await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="add_note",
            arguments={"ticket_id": ticket.get("id"), "note": analysis}
        )
        return {
            "analysis": analysis,
            "consulted_network": bool(consult_result),
            "update_result": update_result
        } 