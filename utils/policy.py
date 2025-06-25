import httpx
from typing import Dict, Any

class OPAPolicyClient:
    def __init__(self, opa_url: str = "http://localhost:8181/v1/data/agent/policy"):
        self.opa_url = opa_url

    async def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.opa_url, json={"input": input_data})
            response.raise_for_status()
            return response.json().get("result", {}) 