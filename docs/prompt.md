# Cursor AI Prompt for IT Helpdesk Application with Multi-Agent Framework

## Project Overview
Create a comprehensive IT helpdesk application using a secure, policy-driven middleware framework for AI agents. The application should demonstrate agent-to-agent collaboration, authentication, authorization, and governance layers while integrating with Freshdesk through MCP (Model Context Protocol).

## Requirements

### Core Framework Integration
- Use the provided middleware framework for secure agent communication
- Implement MCP proxy to interface with Freshdesk MCP server (https://github.com/effytech/freshdesk_mcp)
- All agents use Gemini LLM for AI capabilities
- Python-based implementation with async/await patterns

### Agent Architecture
Create a team of specialized AI agents with distinct roles:

1. **Triage Agent** - Initial ticket assessment and categorization
2. **Technical Support Agent** - Hardware/software troubleshooting
3. **Network Support Agent** - Network and connectivity issues
4. **Security Agent** - Security-related incidents and compliance
5. **Escalation Manager** - Manages complex cases and escalations
6. **Knowledge Base Agent** - Maintains and searches knowledge articles

### Technical Specifications

#### Authentication & Authorization
```python
# Each agent must authenticate with the middleware framework
# Implement role-based access control (RBAC)
# Use JWT tokens for agent-to-agent communication
# Implement policy-driven governance
```

#### MCP Integration
```python
# Proxy Freshdesk MCP server through the middleware
# Expose Freshdesk tools securely to authenticated agents
# Handle rate limiting and error recovery
# Log all MCP interactions for audit
```

#### Agent Capabilities
Each agent should have:
- Gemini LLM integration for natural language processing
- Specific tool access based on role permissions
- Ability to collaborate with other agents
- State management for ongoing conversations
- Error handling and recovery mechanisms


#### MCP Proxy Integration
Expose these Freshdesk capabilities through the framework:
- Create support tickets
- Update ticket status and priority
- Add notes and comments
- Assign tickets to agents
- Search and filter tickets
- Manage customer information
- Generate reports and analytics


## Sample Use Cases to Implement

#### 5. Agent Collaboration Patterns

### 1. New Ticket Triage Flow
- User creates ticket in Freshdesk
- Triage Agent receives notification
- Agent analyzes ticket content using Gemini
- Categorizes and assigns to appropriate specialist
- Updates ticket with initial assessment

### 2. Multi-Agent Collaboration
- Technical issue requires network expertise
- Technical Support Agent consults Network Support Agent
- Both agents work together to resolve issue
- Knowledge Base Agent updates documentation
- Escalation Manager monitors progress

### 3. Security Incident Response
- Security-related ticket detected
- Security Agent takes immediate action
- Coordinates with other agents for impact assessment
- Implements containment measures
- Documents incident for compliance

## Configuration Requirements

## Implementation Guidelines

### 1. Error Handling
- Implement comprehensive error handling for MCP connections and OPA policy evaluations
- Add retry logic with exponential backoff for both MCP and OPA calls
- Log all errors for debugging and monitoring


### 2. Security Considerations
- Validate all inputs to prevent injection attacks in both MCP calls and OPA policy evaluations
- Implement rate limiting per agent with OPA policy enforcement
- Audit all agent actions, tool usage, and policy decisions
- Encrypt sensitive data in transit and at rest
- Secure OPA policy storage and updates
- Implement policy versioning and rollback capabilities

### 3. Performance Optimization
- Use connection pooling for MCP connections and OPA HTTP clients
- Implement caching for frequently accessed data and policy decisions
- Use async/await throughout for better concurrency
- Cache OPA policy evaluations for identical requests
- Implement policy decision caching with TTL

### 4. Testing Strategy
- Unit tests for each agent class and OPA integration
- Integration tests for MCP proxy and policy engine
- End-to-end tests for complete workflows with policy enforcement
- Mock Freshdesk API and OPA server for testing
- Test policy loading, evaluation, and edge cases
- Policy regression testing

### 5. Monitoring and Observability
- Log agent interactions, decisions, and policy evaluations
- Monitor MCP connection health and OPA server status
- Track ticket resolution times and success rates
- Generate reports on agent performance and policy compliance
- Monitor policy decision latency and cache hit rates
- Alert on policy violations and authorization failures

## Deliverables

1. **Complete Python application** following the specified architecture with OPA integration
2. **Rego policy files** for comprehensive agent authorization and governance
3. **Configuration files** for agents, OPA policies, and environment
4. **Documentation** including setup instructions, policy authoring guide, and API reference
5. **Test suite** with comprehensive coverage including policy testing
6. **Docker configuration** for easy deployment with OPA server
7. **Sample data** for testing and demonstration
8. **OPA policy management utilities** for loading, updating, and versioning policies

## Success Criteria

The application should demonstrate:
- Successful agent authentication and authorization with OPA policy enforcement
- Secure MCP proxy functionality with Freshdesk and policy-driven access control
- Effective multi-agent collaboration governed by Rego policies
- Dynamic policy enforcement and governance with real-time evaluation
- Robust error handling and recovery for both MCP and OPA systems
- Real-time ticket processing and updates with fine-grained authorization
- Comprehensive logging and audit trails including policy decisions
- Policy management capabilities (loading, updating, testing policies)

## Additional Notes

- Use modern Python practices (type hints, dataclasses, async/await)
- Follow PEP 8 style guidelines
- Include comprehensive docstrings and comments
- Implement graceful shutdown handling for both MCP and OPA connections
- Support hot-reloading of agent configurations and OPA policies
- Provide clear separation of concerns between components
- Include OPA policy testing utilities and documentation
- Implement policy validation and syntax checking
- Support policy versioning and rollback mechanisms
- Provide policy authoring guidelines and best practices documentation

Please generate a complete, production-ready implementation that showcases the power of the middleware framework with OPA-based policy enforcement for building secure, collaborative AI agent applications with fine-grained authorization control.