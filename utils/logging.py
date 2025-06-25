import os
import json
import asyncio
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file: str = None, to_stdout: bool = True):
        self.log_file = log_file or os.getenv("AUDIT_LOG_FILE", "audit.log")
        self.to_stdout = to_stdout
        self._lock = asyncio.Lock()

    async def log_audit_event(self, event_type: str, agent_id: str, action: str, details: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "agent_id": agent_id,
            "action": action,
            "details": details
        }
        line = json.dumps(entry)
        async with self._lock:
            if self.log_file:
                with open(self.log_file, "a") as f:
                    f.write(line + "\n")
            if self.to_stdout:
                print("[AUDIT]", line) 