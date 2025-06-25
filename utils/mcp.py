import os
import httpx
from typing import Dict, Any

class MCPClient:
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or os.getenv("MCP_PROXY_URL", "http://localhost:3000")
        self.token = token or os.getenv("AGENT_JWT_TOKEN", "dummy-token")

    async def call_tool(self, tool_name: str, operation: str, arguments: Dict[str, Any]) -> Any:
        url = f"{self.base_url}/mcp/tools/call"
        payload = {
            "method": "call",
            "params": {
                "name": tool_name,
                "operation": operation,
                "arguments": arguments
            }
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "error" in data and data["error"]:
                raise Exception(f"MCP error: {data['error']}")
            return data.get("result") 