contacts = [
  {
    "name": "Sarah Mitchell",
    "email": "sarah.mitchell@techcorp.com",
    "phone": "+1-555-0123",
    "job_title": "Software Engineer",
    "company_id": None,
    "description": "Senior developer working on web applications",
    "tags": ["developer", "web", "senior"]
  },
  {
    "name": "Michael Chen",
    "email": "michael.chen@techcorp.com",
    "phone": "+1-555-0124",
    "job_title": "Marketing Manager",
    "company_id": None,
    "description": "Handles digital marketing campaigns",
    "tags": ["marketing", "manager", "campaigns"]
  },
  {
    "name": "Emma Rodriguez",
    "email": "emma.rodriguez@techcorp.com",
    "phone": "+1-555-0125",
    "job_title": "Data Analyst",
    "company_id": None,
    "description": "Analyzes business data and creates reports",
    "tags": ["analytics", "data", "reports"]
  },
  {
    "name": "James Thompson",
    "email": "james.thompson@techcorp.com",
    "phone": "+1-555-0126",
    "job_title": "IT Specialist",
    "company_id": None,
    "description": "Manages internal IT infrastructure",
    "tags": ["IT", "infrastructure", "support"]
  },
  {
    "name": "Lisa Wang",
    "email": "lisa.wang@techcorp.com",
    "phone": "+1-555-0127",
    "job_title": "Product Manager",
    "company_id": None,
    "description": "Oversees product development lifecycle",
    "tags": ["product", "manager", "development"]
  },
  {
    "name": "David Kumar",
    "email": "david.kumar@techcorp.com",
    "phone": "+1-555-0128",
    "job_title": "UX Designer",
    "company_id": None,
    "description": "Creates user experience designs for applications",
    "tags": ["design", "UX", "applications"]
  },
  {
    "name": "Rachel Green",
    "email": "rachel.green@techcorp.com",
    "phone": "+1-555-0129",
    "job_title": "HR Manager",
    "company_id": None,
    "description": "Handles human resources and employee relations",
    "tags": ["HR", "manager", "employees"]
  },
  {
    "name": "Alex Johnson",
    "email": "alex.johnson@techcorp.com",
    "phone": "+1-555-0130",
    "job_title": "DevOps Engineer",
    "company_id": None,
    "description": "Manages deployment pipelines and cloud infrastructure",
    "tags": ["devops", "cloud", "deployment"]
  },
  {
    "name": "Maria Santos",
    "email": "maria.santos@techcorp.com",
    "phone": "+1-555-0131",
    "job_title": "Quality Assurance Tester",
    "company_id": None,
    "description": "Tests software applications for bugs and issues",
    "tags": ["QA", "testing", "quality"]
  },
  {
    "name": "Kevin Park",
    "email": "kevin.park@techcorp.com",
    "phone": "+1-555-0132",
    "job_title": "Sales Representative",
    "company_id": None,
    "description": "Manages client relationships and sales activities",
    "tags": ["sales", "client", "representative"]
  }
]

tickets = [
  {
    "subject": "Unable to connect to company VPN",
    "description": "I'm having trouble connecting to the company VPN from my home office. I get an authentication error every time I try to connect. I've already tried restarting my computer and checking my credentials.",
    "email": "sarah.mitchell@techcorp.com",
    "priority": 2,
    "status": 2,
    "type": "Incident",
    "tags": ["VPN", "authentication", "remote-work"]
  },
  {
    "subject": "Email not syncing on mobile device",
    "description": "My work email stopped syncing on my iPhone yesterday. I can access it on my computer but not on mobile. The last emails I received on mobile were from two days ago.",
    "email": "michael.chen@techcorp.com",
    "priority": 3,
    "status": 2,
    "type": "Incident",
    "tags": ["email", "mobile", "sync-issue"]
  },
  {
    "subject": "Request for additional storage space",
    "description": "I need additional cloud storage space for my data analysis projects. My current allocation is almost full and I have several large datasets to process this month.",
    "email": "emma.rodriguez@techcorp.com",
    "priority": 3,
    "status": 2,
    "type": "Service Request",
    "tags": ["storage", "cloud", "data-analysis"]
  },
  {
    "subject": "Printer not responding to print jobs",
    "description": "The printer on the 3rd floor (HP LaserJet Pro) is not responding to any print jobs. The printer shows as online but jobs are stuck in the queue. Multiple users are affected.",
    "email": "james.thompson@techcorp.com",
    "priority": 2,
    "status": 3,
    "type": "Incident",
    "tags": ["printer", "hardware", "queue"]
  },
  {
    "subject": "Software license renewal needed",
    "description": "Our Adobe Creative Suite licenses are expiring next month. We need to renew licenses for 15 users in the marketing and design teams.",
    "email": "lisa.wang@techcorp.com",
    "priority": 3,
    "status": 2,
    "type": "Service Request",
    "tags": ["license", "adobe", "renewal"]
  },
  {
    "subject": "Computer running very slow",
    "description": "My laptop has been extremely slow for the past week. It takes forever to open applications and sometimes freezes completely. I've tried restarting but the issue persists.",
    "email": "david.kumar@techcorp.com",
    "priority": 2,
    "status": 2,
    "type": "Incident",
    "tags": ["performance", "laptop", "slow"]
  },
  {
    "subject": "Password reset for new employee",
    "description": "We have a new employee starting Monday who needs their system password reset and access to the HR portal. Employee ID: EMP-2024-156",
    "email": "rachel.green@techcorp.com",
    "priority": 2,
    "status": 2,
    "type": "Service Request",
    "tags": ["password-reset", "new-employee", "access"]
  },
  {
    "subject": "Database connection timeout errors",
    "description": "Our production database is experiencing frequent connection timeouts. This is affecting our deployment pipeline and causing build failures. Error code: DB_TIMEOUT_001",
    "email": "alex.johnson@techcorp.com",
    "priority": 1,
    "status": 2,
    "type": "Incident",
    "tags": ["database", "timeout", "production", "critical"]
  },
  {
    "subject": "Testing environment setup request",
    "description": "I need a new testing environment set up for the upcoming release. Requirements: Windows 10, Chrome browser, access to staging database, and testing tools installation.",
    "email": "maria.santos@techcorp.com",
    "priority": 3,
    "status": 2,
    "type": "Service Request",
    "tags": ["testing", "environment", "setup"]
  },
  {
    "subject": "CRM system login issues",
    "description": "I can't log into the CRM system since this morning. I get an 'invalid credentials' error even though I'm using the correct username and password. This is blocking my sales activities.",
    "email": "kevin.park@techcorp.com",
    "priority": 2,
    "status": 2,
    "type": "Incident",
    "tags": ["CRM", "login", "credentials"]
  },
  {
    "subject": "Backup verification failed",
    "description": "Last night's automated backup verification failed with error code BKP-404. Need to investigate and ensure data integrity. Backup location: /backup/daily/2024-06-24",
    "email": "james.thompson@techcorp.com",
    "priority": 1,
    "status": 2,
    "type": "Incident",
    "tags": ["backup", "verification", "critical", "data-integrity"]
  },
  {
    "subject": "Request for video conferencing room booking",
    "description": "Need to book the large conference room with video conferencing setup for client presentation next Friday from 2-4 PM. Please confirm availability and setup requirements.",
    "email": "lisa.wang@techcorp.com",
    "priority": 3,
    "status": 2,
    "type": "Service Request",
    "tags": ["conference-room", "video", "booking"]
  }
]
agents = [
  {
    "name": "Triage Agent",
    "email": "triage@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": True,
    "signature": "Best regards,\nTriage Team"
  },
  {
    "name": "Technical Support Agent",
    "email": "techsupport@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": False,
    "signature": "Best regards,\nTechnical Support Team"
  },
  {
    "name": "Network Support Agent",
    "email": "networksupport@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": False,
    "signature": "Best regards,\nNetwork Support Team"
  },
  {
    "name": "Security Agent",
    "email": "security@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": True,
    "signature": "Best regards,\nSecurity Team"
  },
  {
    "name": "Escalation Manager",
    "email": "escalations@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": True,
    "signature": "Best regards,\nEscalation Management"
  },
  {
    "name": "Knowledge Base Agent",
    "email": "knowledgebase@company.com",
    "ticket_scope": 3,
    "occasional": False,
    "role_ids": [],
    "group_ids": [],
    "skill_ids": [],
    "agent_type": 1,
    "focus_mode": False,
    "signature": "Best regards,\nKnowledge Base Team"
  }
]