"""
CommunicationComponent — Simulated communication logging.
No real emails are sent. Events are logged to communications.json.
"""

import os
from modules.service_modules.FileManager import DATA_DIR, read_json, write_json, ensure_file
from modules.service_modules.HelperFunctions import generate_id, get_timestamp

COMMUNICATIONS_FILE = os.path.join(DATA_DIR, "communications.json")
TEMPLATES_FILE = os.path.join(DATA_DIR, "templates.json")


def render_template(template_key: str, context: dict) -> str:
    """Render a communication template with context data."""
    templates = read_json(TEMPLATES_FILE)
    if isinstance(templates, list):
        return f"Template {template_key} not found"

    template_text = templates.get(template_key, f"Template {template_key} not found")

    # Replace placeholders
    for key, value in context.items():
        template_text = template_text.replace(f"{{{key}}}", str(value))

    return template_text


def trigger_communication(reg_id: str, template_key: str, context: dict) -> dict:
    """Log a simulated communication event."""
    ensure_file(COMMUNICATIONS_FILE, [])
    communications = read_json(COMMUNICATIONS_FILE)

    rendered = render_template(template_key, context)

    comm_entry = {
        "comm_id": generate_id("comm"),
        "reg_id": reg_id,
        "template_key": template_key,
        "rendered_content": rendered,
        "simulated_sent_at": get_timestamp(),
        "status": "sent",
    }

    communications.append(comm_entry)
    write_json(COMMUNICATIONS_FILE, communications)

    return {"status": True, "message": "Communication logged", "output": comm_entry}


def get_communications_by_registration(reg_id: str) -> dict:
    """Get all communications for a specific registration."""
    ensure_file(COMMUNICATIONS_FILE, [])
    communications = read_json(COMMUNICATIONS_FILE)

    filtered = [c for c in communications if c["reg_id"] == reg_id]
    filtered.sort(key=lambda x: x["simulated_sent_at"], reverse=True)

    return {"status": True, "message": f"Found {len(filtered)} communications", "output": filtered}
