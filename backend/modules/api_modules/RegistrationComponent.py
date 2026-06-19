"""
RegistrationComponent — Business logic for candidate registration management.
"""

import os
import csv
import io
from modules.service_modules.FileManager import DATA_DIR, UPLOADS_DIR, read_json, write_json, ensure_file
from modules.service_modules.HelperFunctions import generate_id, get_timestamp
from modules.api_modules.AuditComponent import log_action
from modules.api_modules.CommunicationComponent import trigger_communication

REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")


def register_candidate(drive_id: str, emp_id: str, name: str, email: str,
                       bu: str, location: str, manager_email: str,
                       exam_track: str, slot: str, prior_attempts: int,
                       actor: str) -> dict:
    """Register a single candidate for a drive."""
    ensure_file(REGISTRATIONS_FILE, [])
    registrations = read_json(REGISTRATIONS_FILE)

    # Check duplicate
    duplicate = next(
        (r for r in registrations if r["emp_id"] == emp_id and r["drive_id"] == drive_id),
        None
    )
    if duplicate:
        return {"status": False, "message": f"Candidate {emp_id} is already registered for this drive", "output": None}

    reg_id = generate_id("reg")
    now = get_timestamp()

    registration = {
        "reg_id": reg_id,
        "drive_id": drive_id,
        "emp_id": emp_id,
        "name": name,
        "email": email,
        "bu": bu,
        "location": location,
        "manager_email": manager_email,
        "exam_track": exam_track,
        "slot": slot,
        "prior_attempts": prior_attempts,
        "status": "registered",
        "registered_at": now,
        "ack_timestamp": now,
    }

    registrations.append(registration)
    write_json(REGISTRATIONS_FILE, registrations)

    # Audit
    log_action("Registration", reg_id, "created", actor, before=None, after=registration)

    # Trigger acknowledgement communication
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == drive_id), None)
    drive_name = drive["name"] if drive else drive_id
    trigger_communication(reg_id, "registration_ack", {
        "candidate_name": name,
        "drive_name": drive_name,
        "reg_id": reg_id,
    })

    return {"status": True, "message": "Candidate registered successfully", "output": registration}


def get_registrations_by_drive(drive_id: str) -> dict:
    """Get all registrations for a specific drive."""
    ensure_file(REGISTRATIONS_FILE, [])
    registrations = read_json(REGISTRATIONS_FILE)
    filtered = [r for r in registrations if r["drive_id"] == drive_id]
    filtered.sort(key=lambda x: x["registered_at"], reverse=True)
    return {"status": True, "message": f"Found {len(filtered)} registrations", "output": filtered}


def get_registration_by_id(reg_id: str) -> dict:
    """Get a single registration by ID."""
    ensure_file(REGISTRATIONS_FILE, [])
    registrations = read_json(REGISTRATIONS_FILE)
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    if not reg:
        return {"status": False, "message": "Registration not found", "output": None}
    return {"status": True, "message": "Registration found", "output": reg}


def update_registration_status(reg_id: str, new_status: str, actor: str) -> dict:
    """Update the status of a registration."""
    ensure_file(REGISTRATIONS_FILE, [])
    registrations = read_json(REGISTRATIONS_FILE)
    reg_index = next((i for i, r in enumerate(registrations) if r["reg_id"] == reg_id), None)

    if reg_index is None:
        return {"status": False, "message": "Registration not found", "output": None}

    valid_statuses = ["registered", "eligible", "ineligible", "scheduled", "passed", "failed"]
    if new_status not in valid_statuses:
        return {"status": False, "message": f"Invalid status. Must be one of: {valid_statuses}", "output": None}

    before = registrations[reg_index].copy()
    registrations[reg_index]["status"] = new_status
    write_json(REGISTRATIONS_FILE, registrations)

    log_action("Registration", reg_id, "status_updated", actor, before=before, after=registrations[reg_index])
    return {"status": True, "message": "Registration status updated", "output": registrations[reg_index]}


def bulk_import_registrations(drive_id: str, csv_content: str, actor: str) -> dict:
    """Import registrations from CSV content."""
    ensure_file(REGISTRATIONS_FILE, [])
    registrations = read_json(REGISTRATIONS_FILE)

    reader = csv.DictReader(io.StringIO(csv_content))
    success_count = 0
    error_count = 0
    errors = []

    required_fields = ["emp_id", "name", "email", "bu", "location", "manager_email", "exam_track", "slot"]

    for row_num, row in enumerate(reader, start=2):
        # Validate required fields
        missing = [f for f in required_fields if not row.get(f, "").strip()]
        if missing:
            error_count += 1
            errors.append(f"Row {row_num}: Missing fields: {', '.join(missing)}")
            continue

        emp_id = row["emp_id"].strip()

        # Check duplicate
        if any(r["emp_id"] == emp_id and r["drive_id"] == drive_id for r in registrations):
            error_count += 1
            errors.append(f"Row {row_num}: {emp_id} already registered")
            continue

        reg_id = generate_id("reg")
        now = get_timestamp()

        registration = {
            "reg_id": reg_id,
            "drive_id": drive_id,
            "emp_id": emp_id,
            "name": row["name"].strip(),
            "email": row["email"].strip(),
            "bu": row["bu"].strip(),
            "location": row["location"].strip(),
            "manager_email": row["manager_email"].strip(),
            "exam_track": row["exam_track"].strip(),
            "slot": row["slot"].strip(),
            "prior_attempts": int(row.get("prior_attempts", "0").strip() or "0"),
            "status": "registered",
            "registered_at": now,
            "ack_timestamp": now,
        }

        registrations.append(registration)
        success_count += 1

    write_json(REGISTRATIONS_FILE, registrations)

    log_action("Registration", drive_id, "bulk_imported", actor,
               before=None, after={"success": success_count, "errors": error_count})

    return {
        "status": True,
        "message": f"Imported {success_count} registrations, {error_count} errors",
        "output": {"success_count": success_count, "error_count": error_count, "errors": errors}
    }
