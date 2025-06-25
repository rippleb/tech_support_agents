import asyncio
from a2a_collaboration.registry import A2ARegistry
from a2a_collaboration.session_manager import A2ASessionManager
from a2a_collaboration.orchestration import A2AOrchestrationEngine, WorkflowStage, A2AWorkflow, SessionType
from utils.policy import OPAPolicyClient
from agents.triage import TriageAgent
from agents.tech_support import TechnicalSupportAgent
from agents.network_support import NetworkSupportAgent
from agents.security import SecurityAgent
from agents.escalation_manager import EscalationManagerAgent
from utils.mcp import MCPClient
from utils.logging import AuditLogger

# --- 1. Setup registry, session manager, policy client ---
registry = A2ARegistry()
session_manager = A2ASessionManager(registry)
policy_client = OPAPolicyClient()
mcp_client = MCPClient()

# --- 2. Instantiate real agent classes ---
# For demo, use dummy deps for comm/mcp
class DummyDep:
    def get_agent_credentials(self, agent_id): return ["dummy"]
    def create_credential(self, **kwargs): return "dummy"
    async def send_message(self, *a, **k): return "sent"
    async def call_mcp_tool(self, *a, **k): return {"result": "ok"}

credential_store = DummyDep()
communication_bus = DummyDep()

audit_logger = AuditLogger()

agent_instances = {
    "triage_agent": TriageAgent("triage_agent", credential_store, communication_bus, mcp_client, policy_client, secret="triage_secret", audit_logger=audit_logger),
    "tech_support_agent": TechnicalSupportAgent("tech_support_agent", credential_store, communication_bus, mcp_client, policy_client, secret="tech_secret", audit_logger=audit_logger),
    "network_support_agent": NetworkSupportAgent("network_support_agent", credential_store, communication_bus, mcp_client, policy_client, secret="network_secret", audit_logger=audit_logger),
    "security_agent": SecurityAgent("security_agent", credential_store, communication_bus, mcp_client, policy_client, secret="security_secret", audit_logger=audit_logger),
    "escalation_manager": EscalationManagerAgent("escalation_manager", credential_store, communication_bus, mcp_client, policy_client, secret="escalation_secret", audit_logger=audit_logger),
}

# --- 3. Register agents in registry ---
def register_agent(agent_id, agent_type, capabilities, trust_level=1.0, specializations=None):
    from a2a_collaboration.models import A2ACapabilities, CollaborationMetadata
    a2a_cap = A2ACapabilities(
        can_collaborate=True,
        communication_preferences=["async"],
        collaboration_metadata=CollaborationMetadata(
            max_concurrent_sessions=5,
            preferred_partners=[],
            blacklisted_agents=[],
            specializations=specializations or []
        )
    )
    registry.register_agent(
        agent_id=agent_id,
        agent_type=agent_type,
        capabilities=capabilities,
        trust_level=trust_level,
        a2a_capabilities=a2a_cap
    )

register_agent("triage_agent", "triage", ["triage", "categorize"], specializations=["ticket triage"])
register_agent("tech_support_agent", "tech_support", ["troubleshoot", "software", "hardware"], specializations=["troubleshooting"])
register_agent("network_support_agent", "network_support", ["network", "connectivity"], specializations=["network"])
register_agent("security_agent", "security", ["security", "compliance"], specializations=["security"])
register_agent("escalation_manager", "escalation_manager", ["escalate", "monitor"], specializations=["escalation"])

# --- 4. Define workflows ---
# Ticket Triage Workflow
triage_stage = WorkflowStage(
    id="triage",
    name="Ticket Triage",
    agent_requirements={"type": "triage"},
    input_schema={"ticket": "object"},
    output_schema={"category": "string", "assigned_to": "string"},
    dependencies=[],
    timeout=300,
    retry_policy={"max_retries": 2}
)
assign_stage = WorkflowStage(
    id="assign",
    name="Assign Specialist",
    agent_requirements={"type": "tech_support"},
    input_schema={"ticket": "object", "category": "string"},
    output_schema={"status": "string"},
    dependencies=["triage"],
    timeout=300,
    retry_policy={"max_retries": 2}
)
workflow_triage = A2AWorkflow(
    id="ticket_triage_workflow",
    name="Ticket Triage Workflow",
    description="Triage and assign incoming support tickets.",
    stages=[triage_stage, assign_stage]
)

# Network Issue Resolution Workflow
network_stage = WorkflowStage(
    id="network_support",
    name="Network Support",
    agent_requirements={"type": "network_support"},
    input_schema={"ticket": "object"},
    output_schema={"network_status": "string"},
    dependencies=["triage"],
    timeout=300,
    retry_policy={"max_retries": 2}
)
workflow_network = A2AWorkflow(
    id="network_issue_workflow",
    name="Network Issue Resolution Workflow",
    description="Triage, network support, and tech support for network issues.",
    stages=[triage_stage, network_stage, assign_stage]
)

# Security Incident Response Workflow
security_stage = WorkflowStage(
    id="security",
    name="Security Response",
    agent_requirements={"type": "security"},
    input_schema={"ticket": "object"},
    output_schema={"incident_status": "string"},
    dependencies=["triage"],
    timeout=300,
    retry_policy={"max_retries": 2}
)
escalate_stage = WorkflowStage(
    id="escalate",
    name="Escalation Manager",
    agent_requirements={"type": "escalation_manager"},
    input_schema={"ticket": "object", "incident_status": "string"},
    output_schema={"escalation_status": "string"},
    dependencies=["security"],
    timeout=300,
    retry_policy={"max_retries": 2}
)
workflow_security = A2AWorkflow(
    id="security_incident_workflow",
    name="Security Incident Response Workflow",
    description="Triage, security response, and escalation for incidents.",
    stages=[triage_stage, security_stage, escalate_stage]
)

# --- 5. Orchestration Engine with real agent logic ---
class IntegratedOrchestrationEngine(A2AOrchestrationEngine):
    def __init__(self, *a, agent_instances=None, **kw):
        super().__init__(*a, **kw)
        self.agent_instances = agent_instances or {}

    async def _execute_stage(self, stage, execution, execution_config):
        # Select agent for stage
        agent_record = await self._select_agent_for_stage(stage, execution)
        if not agent_record:
            raise RuntimeError(f"No suitable agent found for stage {stage.id}")
        agent_id = agent_record.id
        agent = self.agent_instances.get(agent_id)
        if not agent:
            raise RuntimeError(f"Agent instance not found for {agent_id}")
        # Policy enforcement
        allowed = await agent.authorize(action="execute_stage", resource=stage.id, context={"workflow_id": execution.workflow_id})
        if not allowed:
            raise PermissionError(f"Policy denied execution of stage {stage.id} by agent {agent_id}")
        # Prepare message for agent
        class Msg: pass
        msg = Msg(); msg.payload = Msg();
        # Compose input for this stage
        stage_input = execution.input_data.copy()
        # Add outputs from dependencies
        for dep in stage.dependencies:
            if dep in execution.stage_results:
                stage_input.update(execution.stage_results[dep])
        msg.payload.data = stage_input
        # Call agent logic
        result = await agent.receive_message(msg)
        return result

# --- 6. Register workflows and run orchestration ---
orchestration_engine = IntegratedOrchestrationEngine(
    registry, session_manager, communication_bus=None, agent_instances=agent_instances
)
orchestration_engine.register_workflow(workflow_triage)
orchestration_engine.register_workflow(workflow_network)
orchestration_engine.register_workflow(workflow_security)

async def main():
    # Ticket Triage Workflow
    session_id = await session_manager.create_session(
        initiator_id="triage_agent",
        participants=["triage_agent", "tech_support_agent"],
        session_type=SessionType.MULTIPARTY
    )
    print(f"Session created: {session_id}")
    input_data = {"ticket": {"id": "T999", "description": "Laptop not booting."}}
    execution_id = await orchestration_engine.execute_workflow(
        workflow_id="ticket_triage_workflow",
        input_data=input_data
    )
    print(f"Triage Workflow execution started: {execution_id}")
    await asyncio.sleep(2)
    status = orchestration_engine.get_execution_status(execution_id)
    print("Triage Workflow execution status:", status)

    # Network Issue Workflow
    input_data_network = {"ticket": {"id": "N100", "description": "Cannot access VPN."}}
    execution_id_network = await orchestration_engine.execute_workflow(
        workflow_id="network_issue_workflow",
        input_data=input_data_network
    )
    print(f"Network Workflow execution started: {execution_id_network}")
    await asyncio.sleep(2)
    status_network = orchestration_engine.get_execution_status(execution_id_network)
    print("Network Workflow execution status:", status_network)

    # Security Incident Workflow
    input_data_security = {"ticket": {"id": "S200", "description": "Suspicious login detected."}}
    execution_id_security = await orchestration_engine.execute_workflow(
        workflow_id="security_incident_workflow",
        input_data=input_data_security
    )
    print(f"Security Workflow execution started: {execution_id_security}")
    await asyncio.sleep(2)
    status_security = orchestration_engine.get_execution_status(execution_id_security)
    print("Security Workflow execution status:", status_security)

if __name__ == "__main__":
    asyncio.run(main()) 