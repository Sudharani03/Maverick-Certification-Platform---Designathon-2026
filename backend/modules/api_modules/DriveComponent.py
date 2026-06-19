"""
DriveComponent — Business logic for certification drive management.
"""

import os
from modules.service_modules.FileManager import (
    DATA_DIR, UPLOADS_DIR, read_json, write_json, ensure_file, ensure_directory
)
from modules.service_modules.HelperFunctions import generate_id, get_timestamp
from modules.api_modules.AuditComponent import log_action

DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")


def create_drive(name: str, sponsor: str, budget: float, start_date: str,
                 end_date: str, target_count: int, policy_notes: str,
                 pass_threshold: int, created_by: str) -> dict:
    """Create a new certification drive and provision folder structure."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)

    # Check for duplicate drive name
    if any(d["name"].lower() == name.lower() for d in drives):
        return {"status": False, "message": "A drive with this name already exists", "output": None}

    drive_id = generate_id("drv")
    drive = {
        "drive_id": drive_id,
        "name": name,
        "sponsor": sponsor,
        "budget": budget,
        "start_date": start_date,
        "end_date": end_date,
        "target_count": target_count,
        "policy_notes": policy_notes,
        "pass_threshold": pass_threshold,
        "status": "active",
        "created_at": get_timestamp(),
        "created_by": created_by,
    }

    drives.append(drive)
    write_json(DRIVES_FILE, drives)

    # Auto-provision folder structure
    _provision_drive_folders(drive_id)

    # Audit log
    log_action("Drive", drive_id, "created", created_by, before=None, after=drive)

    return {"status": True, "message": "Drive created successfully", "output": drive}


def get_all_drives() -> dict:
    """Retrieve all drives."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)
    drives.sort(key=lambda x: x["created_at"], reverse=True)
    return {"status": True, "message": f"Found {len(drives)} drives", "output": drives}


def get_drive_by_id(drive_id: str) -> dict:
    """Retrieve a single drive by ID."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == drive_id), None)
    if not drive:
        return {"status": False, "message": "Drive not found", "output": None}
    return {"status": True, "message": "Drive found", "output": drive}


def update_drive(drive_id: str, updates: dict, actor: str) -> dict:
    """Update drive metadata."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)
    drive_index = next((i for i, d in enumerate(drives) if d["drive_id"] == drive_id), None)

    if drive_index is None:
        return {"status": False, "message": "Drive not found", "output": None}

    before = drives[drive_index].copy()

    # Apply allowed updates
    allowed_fields = ["name", "sponsor", "budget", "start_date", "end_date",
                      "target_count", "policy_notes", "pass_threshold"]
    for key, value in updates.items():
        if key in allowed_fields:
            drives[drive_index][key] = value

    write_json(DRIVES_FILE, drives)
    log_action("Drive", drive_id, "updated", actor, before=before, after=drives[drive_index])

    return {"status": True, "message": "Drive updated successfully", "output": drives[drive_index]}


def close_drive(drive_id: str, actor: str) -> dict:
    """Close a drive (set status to closed)."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)
    drive_index = next((i for i, d in enumerate(drives) if d["drive_id"] == drive_id), None)

    if drive_index is None:
        return {"status": False, "message": "Drive not found", "output": None}

    before = drives[drive_index].copy()
    drives[drive_index]["status"] = "closed"
    write_json(DRIVES_FILE, drives)

    log_action("Drive", drive_id, "closed", actor, before=before, after=drives[drive_index])
    return {"status": True, "message": "Drive closed successfully", "output": drives[drive_index]}


def delete_drive(drive_id: str, actor: str) -> dict:
    """Delete a drive."""
    ensure_file(DRIVES_FILE, [])
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == drive_id), None)

    if not drive:
        return {"status": False, "message": "Drive not found", "output": None}

    drives = [d for d in drives if d["drive_id"] != drive_id]
    write_json(DRIVES_FILE, drives)

    log_action("Drive", drive_id, "deleted", actor, before=drive, after=None)
    return {"status": True, "message": "Drive deleted successfully", "output": None}


def _provision_drive_folders(drive_id: str) -> None:
    """Create the standard folder structure for a drive."""
    base_path = os.path.join(UPLOADS_DIR, drive_id)
    subfolders = ["01_Registrations", "02_Attendance", "03_Assessments", "04_Vouchers", "99_Audit"]
    for folder in subfolders:
        ensure_directory(os.path.join(base_path, folder))
