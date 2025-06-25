from typing import Any, Dict, Optional
from agent_auth.credentials import CredentialStore, CredentialType
from a2a_collaboration.communication import A2ACommunicationBus
from utils.mcp import MCPClient
from utils.policy import OPAPolicyClient
from utils.logging import AuditLogger
# from policy_engine import PolicyClient  # Assume a client for OPA policy evaluation

class BaseAgent:
    """
    Base class for all IT Helpdesk agents.
    Handles authentication, authorization, communication, MCP proxy, and LLM integration.
    """
    def __init__(
        self,
        agent_id: str,
        credential_store: CredentialStore,
        communication_bus: A2ACommunicationBus,
        mcp_client: MCPClient,
        policy_client: OPAPolicyClient,
        # policy_client: PolicyClient,
        secret: str,
        audit_logger: AuditLogger,
        **kwargs
    ):
        self.agent_id = agent_id
        self.credential_store = credential_store
        self.communication_bus = communication_bus
        self.mcp_client = mcp_client
        self.policy_client = policy_client
        # self.policy_client = policy_client
        self.secret = secret
        self.jwt_token: Optional[str] = None
        self.authenticated = False
        self.extra = kwargs
        self.audit_logger = audit_logger

    async def authenticate(self) -> bool:
        """Authenticate the agent and obtain a JWT token."""
        # For demo: create and validate credential, then generate JWT
        creds = self.credential_store.get_agent_credentials(self.agent_id)
        if not creds:
            self.credential_store.create_credential(
                agent_id=self.agent_id,
                credential_type=CredentialType.JWT,
                secret=self.secret,
                credential_metadata=None
            )
        # In real use, fetch/generate JWT here
        self.jwt_token = f"jwt-token-for-{self.agent_id}"
        self.authenticated = True
        return self.authenticated

    async def authorize(self, action: str, resource: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Check OPA policy for the given action/resource/context."""
        input_data = {
            "agent_id": self.agent_id,
            "action": action,
            "resource": resource,
            "context": context or {}
        }
        result = await self.policy_client.evaluate(input_data)
        allowed = result.get("allow", False)
        await self.audit_logger.log_audit_event(
            event_type="policy_decision",
            agent_id=self.agent_id,
            action=action,
            details={"resource": resource, "context": context, "policy_result": result}
        )
        return allowed

    async def send_message(self, recipient_id: str, intent: str, data: Dict[str, Any], **kwargs) -> str:
        """Send a message to another agent via the communication bus."""
        return await self.communication_bus.send_message(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            intent=intent,
            data=data,
            **kwargs
        )

    async def receive_message(self, message):
        """Handle an incoming message (to be implemented by subclasses)."""
        raise NotImplementedError

    async def call_mcp_tool(self, tool_name: str, operation: str, arguments: Dict[str, Any]) -> Any:
        result = await self.mcp_client.call_tool(tool_name, operation, arguments)
        await self.audit_logger.log_audit_event(
            event_type="mcp_call",
            agent_id=self.agent_id,
            action=f"{tool_name}.{operation}",
            details={"arguments": arguments, "result": result}
        )
        return result

    async def run_llm(self, prompt: str) -> str:
        """Call Gemini LLM (stub)."""
        # Replace with real Gemini API call
        return f"[Gemini LLM output for prompt: {prompt}]" 