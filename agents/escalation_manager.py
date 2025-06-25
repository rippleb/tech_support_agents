from typing import Any, Dict
from .base import BaseAgent
from .system_prompts import SYSTEM_PROMPTS

class EscalationManagerAgent(BaseAgent):
    """
    Agent for managing complex cases and escalations.
    """
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.system_prompt = SYSTEM_PROMPTS["escalation_manager_agent"]

    async def receive_message(self, message: Any):
        ticket = message.payload.data.get("ticket")
        if not ticket:
            return {"error": "No ticket found in message."}
        # Monitor progress with LLM
        progress = await self.run_llm(f"Monitor escalation progress for ticket: {ticket}")
        reassigned = False
        if "stalled" in progress.lower():
            reassigned = True
            await self.call_mcp_tool(
                tool_name="freshdesk",
                operation="assign_ticket",
                arguments={"ticket_id": ticket.get("id"), "assignee": "senior_tech_support"}
            )
        return {
            "progress": progress,
            "reassigned": reassigned
        } 