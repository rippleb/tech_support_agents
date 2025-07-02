from typing import Any, Dict, Optional, List
from agent_auth.credentials import CredentialStore, CredentialType
from a2a_collaboration.communication import A2ACommunicationBus
from utils.mcp import MCPClient
from utils.policy import OPAPolicyClient
from utils.audit_logging import AuditLogger
from a2a_collaboration.models import A2AAgent, A2ACapabilities, CollaborationMetadata
from a2a_collaboration.registry import A2ARegistry
from .llm import LLMClient, LLMConfig, LLMProvider
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
        llm_config: LLMConfig,
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
        self.llm_config = llm_config
        self.llm_client = LLMClient(self.llm_config)
        # self.policy_client = policy_client
        self.secret = secret
        self.jwt_token: Optional[str] = None
        self.authenticated = False
        self.extra = kwargs
        self.audit_logger = audit_logger

    async def authenticate(self) -> bool:
        """Authenticate the agent and obtain a JWT token."""
        # TODO: Replace with real authentication logic
        # OFor demo: create and validate credential, then generate JWT
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

    async def run_llm(
        self, 
        prompt: str, 
        override_config: Optional[LLMConfig] = None
        ) -> str:
        """
        Call LLM with the given prompt and optional system prompt.
        
        Args:
            prompt: The user prompt to send to the LLM
            system_prompt: Optional system prompt to set context/behavior
            override_config: Optional LLM config to use instead of default
            
        Returns:
            Generated response from the LLM
            
        Raises:
            Exception: If LLM generation fails or no LLM is configured
        """
        if not self.llm_client and not override_config:
            raise Exception("No LLM client configured for this agent")
        
        # Use override config if provided
        client = self.llm_client
        if override_config:
            client = LLMClient(override_config)
        
        try:
            # Generate response
            response = await client.generate(prompt, self.system_prompt)
            
            # Log the LLM call for audit purposes
            await self.audit_logger.log_audit_event(
                event_type="llm_call",
                agent_id=self.agent_id,
                action="generate_response",
                details={
                    "provider": (override_config or self.llm_config).provider.value,
                    "model": (override_config or self.llm_config).model,
                    "prompt_length": len(prompt),
                    "response_length": len(response),
                    "has_system_prompt": bool(self.system_prompt)
                }
            )
            
            return response
            
        except Exception as e:
            # Log the error
            await self.audit_logger.log_audit_event(
                event_type="llm_error",
                agent_id=self.agent_id,
                action="generate_response",
                details={
                    "error": str(e),
                    "provider": (override_config or self.llm_config).provider.value,
                    "model": (override_config or self.llm_config).model
                }
            )
            raise Exception(f"LLM generation failed: {str(e)}")

    async def run_llm_with_tools(
        self, 
        prompt: str, 
        available_tools: Optional[List[Dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run LLM with tool calling capability (for providers that support it).
        
        Args:
            prompt: The user prompt
            available_tools: List of tool definitions in OpenAI format
            system_prompt: Optional system prompt
            
        Returns:
            Dict containing response and any tool calls
        """
        if self.llm_config.provider not in [LLMProvider.OPENAI, LLMProvider.AZURE_OPENAI]:
            # Fallback to regular LLM call for providers without tool support
            response = await self.run_llm(prompt, system_prompt)
            return {"response": response, "tool_calls": []}
        
        # For OpenAI-compatible providers with tool support
        messages = []
        if system_prompt:
            agent_context = f"You are agent {self.agent_id} in an IT helpdesk system."
            full_system_prompt = f"{agent_context}\n\n{system_prompt}"
            messages.append({"role": "system", "content": full_system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.llm_config.model,
            "messages": messages,
            "temperature": self.llm_config.temperature,
            "max_tokens": self.llm_config.max_tokens
        }
        
        if available_tools:
            kwargs["tools"] = available_tools
            kwargs["tool_choice"] = "auto"
        
        try:
            response = await self.llm_client._client.chat.completions.create(**kwargs)
            
            message = response.choices[0].message
            result = {
                "response": message.content or "",
                "tool_calls": []
            }
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result["tool_calls"].append({
                        "id": tool_call.id,
                        "function": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
            
            return result
            
        except Exception as e:
            await self.audit_logger.log_audit_event(
                event_type="llm_tools_error",
                agent_id=self.agent_id,
                action="generate_with_tools",
                details={"error": str(e)}
            )
            raise Exception(f"LLM with tools failed: {str(e)}")


    @classmethod
    def from_a2aagent(cls, a2a_agent: A2AAgent, credential_store, communication_bus, mcp_client, policy_client, secret, audit_logger: AuditLogger, **kwargs):
        # Map A2AAgent fields to BaseAgent
        return cls(
            agent_id=a2a_agent.id,
            credential_store=credential_store,
            communication_bus=communication_bus,
            mcp_client=mcp_client,
            policy_client=policy_client,
            secret=secret,
            audit_logger=audit_logger,
            agent_type=a2a_agent.type,
            capabilities=a2a_agent.capabilities,
            trust_level=a2a_agent.trust_level,
            a2a_capabilities=A2ACapabilities(
                can_collaborate=True,
                communication_preferences=a2a_agent.communication_preferences,
                collaboration_metadata=CollaborationMetadata(**a2a_agent.collaboration_metadata)
            ),
            **kwargs
        )

    def register(self, registry: A2ARegistry):
        # Register this agent in the A2ARegistry
        a2a_cap = getattr(self, 'a2a_capabilities', None)
        if not a2a_cap:
            # Fallback: create from fields if not present
            a2a_cap = A2ACapabilities(
                can_collaborate=True,
                communication_preferences=getattr(self, 'communication_preferences', ["async"]),
                collaboration_metadata=CollaborationMetadata(
                    max_concurrent_sessions=5,
                    preferred_partners=[],
                    blacklisted_agents=[],
                    specializations=getattr(self, 'specializations', [])
                )
            )
        return registry.register_agent(
            agent_id=self.agent_id,
            agent_type=getattr(self, 'agent_type', 'generic'),
            capabilities=getattr(self, 'capabilities', []),
            trust_level=getattr(self, 'trust_level', 1.0),
            a2a_capabilities=a2a_cap
        ) 