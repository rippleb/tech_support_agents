To build a **demo app** that uses the [freshdesk-mcp](https://pypi.org/project/freshdesk-mcp/) server and adds a **policy-based access control layer** on top of the Freshdesk tools, you can follow this architecture and workflow:

---

## 1. **Understand the freshdesk-mcp Server**

- The `freshdesk-mcp` server exposes a set of **tools** (each corresponding to a Freshdesk operation, e.g., `create_ticket`, `get_agents`, etc.).
- Each tool has a well-defined input schema and is accessible via the MCP protocol (typically HTTP endpoints).

---

## 2. **Demo App Architecture**

Your demo app will:
- **Connect to the MCP server** (as a client or via HTTP).
- **Register the available Freshdesk tools** in your own `ToolRegistry` (one per operation, e.g., `create_ticket`, `get_agents`, etc.).
- **Define and enforce policies** for each tool/operation using your `PolicyEngine`.
- **Authenticate agents** and issue credentials.
- **Route tool calls through the policy engine** before forwarding to the MCP server.

---

## 3. **Implementation Steps**

### **A. Discover and Register Tools**

- For each Freshdesk operation (as listed in the [freshdesk-mcp docs](https://pypi.org/project/freshdesk-mcp/)), create a `ToolModel` and register it in your `ToolRegistry`.
- Example:
    ```python
    tool_registry.register_tool(ToolModel(
        id="create_ticket",
        name="Create Ticket",
        type=ToolType.API,
        capabilities=[Operation.WRITE],
        connection_config={"endpoint": "/mcp/tools/call", "operation": "create_ticket"},
        trust_requirements=0.7,
        policy_requirements=["can_create_ticket"],
        tool_metadata={"description": "Create new Freshdesk support ticket"}
    ))
    ```

### **B. Define Policies**

- Use your `PolicyEngine` to define rules for which agents can access which tools and under what conditions.
- Example policy: Only agents with the "support" role can `create_ticket`, and only during business hours.

### **C. Authenticate Agents**

- Use your `CredentialStore` to issue and validate credentials for agents.
- Agents must present valid credentials to access tools.

### **D. Route Tool Calls**

- When an agent requests to use a tool:
    1. **Authenticate** the agent.
    2. **Check policy** for the requested operation/tool.
    3. If allowed, **forward the request** to the MCP server (e.g., via HTTP POST to `/mcp/tools/call` with the right parameters).
    4. **Log the access** in your `AuditLogger`.

### **E. Example Demo Flow**

```python
from mcp_proxy import ToolRegistry, ToolModel, ToolType, Operation
from policy_engine.engine import PolicyEngine
from agent_auth import CredentialStore, CredentialType, CredentialMetadata
import requests

# 1. Setup
tool_registry = ToolRegistry()
policy_engine = PolicyEngine()
credential_store = CredentialStore()

# 2. Register tools (one per Freshdesk operation)
tool_registry.register_tool(ToolModel(
    id="create_ticket",
    name="Create Ticket",
    type=ToolType.API,
    capabilities=[Operation.WRITE],
    connection_config={"endpoint": "/mcp/tools/call", "operation": "create_ticket"},
    trust_requirements=0.7,
    policy_requirements=["can_create_ticket"],
    tool_metadata={"description": "Create new Freshdesk support ticket"}
))
# ...repeat for other tools...

# 3. Define policies
def can_create_ticket_policy(context, tool):
    return context.agent_type == "support" and context.trust_level >= 0.7

policy_engine.add_policy("create_ticket", can_create_ticket_policy)

# 4. Authenticate agent
agent_id = "support-agent"
credential = credential_store.create_credential(
    agent_id=agent_id,
    credential_type=CredentialType.API_KEY,
    secret="supersecret",
    credential_metadata=CredentialMetadata(name="Support Agent", description="Support team member")
)

# 5. Agent requests to create a ticket
def call_tool(agent_id, tool_name, operation, arguments, credential):
    # Authenticate
    if not credential_store.validate_credential(credential, "supersecret"):
        print("Authentication failed")
        return

    # Get tool
    tool = tool_registry.get_tool_by_name(tool_name)
    if not tool:
        print("Tool not found")
        return

    # Policy check
    policy_decision = policy_engine.evaluate_policy(agent_id=agent_id, tool=tool, operation=operation)
    if not policy_decision.allow:
        print(f"Access denied: {policy_decision.reason}")
        return

    # Forward to MCP server
    response = requests.post(
        "http://localhost:3000/mcp/tools/call",
        json={
            "method": "call_tool",
            "params": {
                "name": tool_name,
                "operation": operation,
                "arguments": arguments
            }
        },
        headers={"Authorization": f"Bearer {credential}"}
    )
    print(response.json())

# Example call
call_tool(
    agent_id="support-agent",
    tool_name="create_ticket",
    operation="write",
    arguments={
        "subject": "Demo Issue",
        "description": "This is a test ticket",
        "priority": 1,
        "status": 2
    },
    credential=credential
)
```

---

## 4. **Demo App Features**

- **Policy-based access**: Only authorized agents can perform certain Freshdesk operations.
- **Audit logging**: Every tool call is logged for compliance.
- **Credential management**: Agents must authenticate to use tools.
- **Extensible**: Add more tools, policies, or agent types as needed.

---

## 5. **References**

- [freshdesk-mcp PyPI documentation](https://pypi.org/project/freshdesk-mcp/)

---

**Summary:**  
You model each Freshdesk operation as a separate tool in your registry, define policies for each, and route all access through your policy engine before forwarding to the MCP server. This gives you fine-grained, auditable, and secure access control over all Freshdesk operations in your demo app.
