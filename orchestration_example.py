import asyncio
from a2a_collaboration.registry import A2ARegistry
from a2a_collaboration.session_manager import A2ASessionManager
from a2a_collaboration.orchestration import A2AOrchestrationEngine
from a2a_collaboration.models import (
    A2ACapabilities, CollaborationMetadata, WorkflowStage, A2AWorkflow, SessionType
)

# --- 1. Agent Registration ---
registry = A2ARegistry()

def register_agent(agent_id, agent_type, capabilities, trust_level=1.0, specializations=None):
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

# --- 2. Session Management ---
session_manager = A2ASessionManager(registry)

# --- 3. Workflow Definition ---
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

workflow = A2AWorkflow(
    id="ticket_triage_workflow",
    name="Ticket Triage Workflow",
    description="Triage and assign incoming support tickets.",
    stages=[triage_stage, assign_stage]
)

# --- 4. Orchestration Engine ---
orchestration_engine = A2AOrchestrationEngine(registry, session_manager, communication_bus=None)
orchestration_engine.register_workflow(workflow)

async def main():
    # Create a session for the workflow
    session_id = await session_manager.create_session(
        initiator_id="triage_agent",
        participants=["triage_agent", "tech_support_agent"],
        session_type=SessionType.MULTIPARTY
    )
    print(f"Session created: {session_id}")

    # Execute the workflow
    input_data = {"ticket": {"id": "T999", "description": "Laptop not booting."}}
    execution_id = await orchestration_engine.execute_workflow(
        workflow_id="ticket_triage_workflow",
        input_data=input_data
    )
    print(f"Workflow execution started: {execution_id}")

if __name__ == "__main__":
    asyncio.run(main()) 