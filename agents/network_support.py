from typing import Any, Dict
from .base import BaseAgent
from .system_prompts import SYSTEM_PROMPTS

class NetworkSupportAgent(BaseAgent):
    """
    Agent for network and connectivity issues.
    """
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.system_prompt = SYSTEM_PROMPTS["network_support_agent"]

    async def receive_message(self, message: Any):
        ticket = message.payload.data.get("ticket")
        if not ticket:
            return {"error": "No ticket found in message."}
        # Analyze network issue with LLM
        analysis = await self.run_llm(f"Diagnose network issue: {ticket}")
        # Update ticket with network status
        update_result = await self.call_mcp_tool(
            tool_name="freshdesk",
            operation="add_note",
            arguments={"ticket_id": ticket.get("id"), "note": analysis}
        )
        return {
            "analysis": analysis,
            "update_result": update_result
        } 