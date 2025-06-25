from typing import Any, Dict
from .base import BaseAgent
from .system_prompts import SYSTEM_PROMPTS

class SecurityAgent(BaseAgent):
    """
    Agent for security incidents and compliance.
    """
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.system_prompt = SYSTEM_PROMPTS["security_agent"]

    async def receive_message(self, message: Any):
        ticket = message.payload.data.get("ticket")
        if not ticket:
            return {"error": "No ticket found in message."}
        # Analyze security incident with LLM
        analysis = await self.run_llm(f"Assess security incident: {ticket}")
        # Add security incident note
        await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="add_note",
            arguments={"ticket_id": ticket.get("id"), "note": analysis}
        )
        # Update ticket status
        update_result = await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="update_ticket_status",
            arguments={"ticket_id": ticket.get("id"), "status": "security_review"}
        )
        # Coordinate with other agents (stub)
        coordination = await self.send_message(
            recipient_id="escalation_manager",
            intent="security_incident",
            data={"ticket": ticket}
        )
        return {
            "analysis": analysis,
            "coordinated_with": "escalation_manager",
            "update_result": update_result
        } 