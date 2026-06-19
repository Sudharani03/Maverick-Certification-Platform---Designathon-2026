"""
AuditComponent — Business logic for audit trail logging and retrieval.
Append-only: no update or delete operations.
"""

import os
from modules.service_modules.FileManager import DATA_DIR, read_json, write_json, ensure_file
from modules.service_modules.HelperFunctions import generate_id, get_timestamp

AUDIT_FILE = os.path.join(DATA_DIR, "audit_logs.json")


def log_action(entity: str, entity_id: str, action: str, actor: str, before=None, after=None) -> dict:
    """Append an audit log entry. This is called by other modules on state changes."""
    ensure_file(AUDIT_FILE, [])
    logs = read_json(AUDIT_FILE)

    log_entry = {
        "log_id": generate_id("log"),
        "entity": entity,
        "entity_id": entity_id,
        "action": action,
        "actor": actor,
        "timestamp": get_timestamp(),
        "before": before,
        "after": after,
    }

    logs.append(log_entry)
    write_json(AUDIT_FILE, logs)

    return {"status": True, "message": "Audit log entry created", "output": log_entry}


def get_audit_logs(entity: str = None, action: str = None, actor: str = None,
                   date_from: str = None, date_to: str = None) -> dict:
    """Retrieve audit logs with optional filters."""
    ensure_file(AUDIT_FILE, [])
    logs = read_json(AUDIT_FILE)

    filtered = logs

    if entity:
        filtered = [l for l in filtered if l["entity"] == entity]
    if action:
        filtered = [l for l in filtered if l["action"] == action]
    if actor:
        filtered = [l for l in filtered if l["actor"] == actor]
    if date_from:
        filtered = [l for l in filtered if l["timestamp"] >= date_from]
    if date_to:
        filtered = [l for l in filtered if l["timestamp"] <= date_to]

    # Sort by timestamp descending (newest first)
    filtered.sort(key=lambda x: x["timestamp"], reverse=True)

    return {"status": True, "message": f"Found {len(filtered)} audit log entries", "output": filtered}


def get_audit_by_entity(entity_type: str, entity_id: str) -> dict:
    """Get all audit logs for a specific entity."""
    ensure_file(AUDIT_FILE, [])
    logs = read_json(AUDIT_FILE)

    filtered = [l for l in logs if l["entity"] == entity_type and l["entity_id"] == entity_id]
    filtered.sort(key=lambda x: x["timestamp"], reverse=True)

    return {"status": True, "message": f"Found {len(filtered)} entries", "output": filtered}
