"""
VoucherComponent — Business logic for voucher pool management and allocation.
"""

import os
from datetime import datetime, timedelta
from modules.service_modules.FileManager import DATA_DIR, UPLOADS_DIR, read_json, write_json, ensure_file
from modules.service_modules.HelperFunctions import generate_id, get_timestamp, mask_voucher_code
from modules.api_modules.AuditComponent import log_action
from modules.api_modules.CommunicationComponent import trigger_communication

VOUCHERS_FILE = os.path.join(DATA_DIR, "vouchers.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")


def add_vouchers_to_pool(drive_id: str, vendor: str, value: float,
                         expiry_date: str, codes: list, actor: str) -> dict:
    """Add vouchers to the pool for a drive."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)

    added = []
    for code in codes:
        code = code.strip()
        if not code:
            continue

        # Check duplicate code
        if any(v["code"] == code for v in vouchers):
            continue

        voucher = {
            "voucher_id": generate_id("vch"),
            "drive_id": drive_id,
            "vendor": vendor,
            "code": code,
            "masked_code": mask_voucher_code(code),
            "value": value,
            "expiry_date": expiry_date,
            "status": "available",
            "assigned_to": None,
            "allocated_date": None,
            "delivery_status": "pending",
            "redeemed_date": None,
            "reminder_sent": [],
        }
        vouchers.append(voucher)
        added.append(voucher["voucher_id"])

    write_json(VOUCHERS_FILE, vouchers)

    log_action("Voucher", drive_id, "pool_added", actor,
               before=None, after={"count": len(added), "vendor": vendor})

    return {"status": True, "message": f"Added {len(added)} vouchers to pool", "output": {"count": len(added)}}


def allocate_voucher(reg_id: str, actor: str) -> dict:
    """Allocate a single voucher to a passed candidate."""
    ensure_file(VOUCHERS_FILE, [])
    ensure_file(REGISTRATIONS_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    if not reg:
        return {"status": False, "message": "Registration not found", "output": None}

    if reg["status"] != "passed":
        return {"status": False, "message": f"Candidate status is '{reg['status']}', must be 'passed'", "output": None}

    vouchers = read_json(VOUCHERS_FILE)

    # Check for existing active allocation (no duplicates)
    existing = next(
        (v for v in vouchers if v["assigned_to"] == reg_id and v["status"] == "allocated"),
        None
    )
    if existing:
        return {"status": False, "message": "Candidate already has an active voucher allocated", "output": None}

    # Find available voucher for this drive
    available = next(
        (v for v in vouchers if v["drive_id"] == reg["drive_id"] and v["status"] == "available"),
        None
    )
    if not available:
        return {"status": False, "message": "No available vouchers in the pool", "output": None}

    # Allocate
    before = available.copy()
    v_index = next(i for i, v in enumerate(vouchers) if v["voucher_id"] == available["voucher_id"])
    vouchers[v_index]["status"] = "allocated"
    vouchers[v_index]["assigned_to"] = reg_id
    vouchers[v_index]["allocated_date"] = get_timestamp()
    vouchers[v_index]["delivery_status"] = "delivered"

    write_json(VOUCHERS_FILE, vouchers)

    log_action("Voucher", available["voucher_id"], "allocated", actor,
               before=before, after=vouchers[v_index])

    # Communication
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == reg["drive_id"]), None)
    trigger_communication(reg_id, "voucher_issued", {
        "candidate_name": reg["name"],
        "drive_name": drive["name"] if drive else "",
        "voucher_masked_code": vouchers[v_index]["masked_code"],
        "vendor": vouchers[v_index]["vendor"],
        "expiry_date": vouchers[v_index]["expiry_date"],
    })

    return {"status": True, "message": "Voucher allocated successfully", "output": _sanitize_voucher(vouchers[v_index])}


def auto_allocate_for_drive(drive_id: str, actor: str) -> dict:
    """Auto-allocate vouchers to all passed candidates without existing allocation."""
    ensure_file(VOUCHERS_FILE, [])
    ensure_file(REGISTRATIONS_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    vouchers = read_json(VOUCHERS_FILE)

    passed_candidates = [
        r for r in registrations
        if r["drive_id"] == drive_id and r["status"] == "passed"
    ]

    allocated_reg_ids = {
        v["assigned_to"] for v in vouchers
        if v["drive_id"] == drive_id and v["status"] == "allocated"
    }

    to_allocate = [r for r in passed_candidates if r["reg_id"] not in allocated_reg_ids]

    success_count = 0
    failed_count = 0

    for reg in to_allocate:
        result = allocate_voucher(reg["reg_id"], actor)
        if result["status"]:
            success_count += 1
        else:
            failed_count += 1
            # If no more vouchers, stop
            if "No available vouchers" in result["message"]:
                failed_count += len(to_allocate) - success_count - 1
                break

    return {
        "status": True,
        "message": f"Allocated {success_count} vouchers, {failed_count} failed",
        "output": {"allocated": success_count, "failed": failed_count, "total_candidates": len(to_allocate)}
    }


def get_vouchers_by_drive(drive_id: str) -> dict:
    """Get all vouchers for a drive (masked codes only)."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)
    filtered = [_sanitize_voucher(v) for v in vouchers if v["drive_id"] == drive_id]
    return {"status": True, "message": f"Found {len(filtered)} vouchers", "output": filtered}


def revoke_voucher(voucher_id: str, actor: str) -> dict:
    """Revoke an allocated voucher."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)

    v_index = next((i for i, v in enumerate(vouchers) if v["voucher_id"] == voucher_id), None)
    if v_index is None:
        return {"status": False, "message": "Voucher not found", "output": None}

    if vouchers[v_index]["status"] != "allocated":
        return {"status": False, "message": "Can only revoke allocated vouchers", "output": None}

    before = vouchers[v_index].copy()
    vouchers[v_index]["status"] = "revoked"
    vouchers[v_index]["assigned_to"] = None
    vouchers[v_index]["delivery_status"] = "pending"

    write_json(VOUCHERS_FILE, vouchers)
    log_action("Voucher", voucher_id, "revoked", actor, before=before, after=vouchers[v_index])

    return {"status": True, "message": "Voucher revoked", "output": _sanitize_voucher(vouchers[v_index])}


def reissue_voucher(reg_id: str, actor: str) -> dict:
    """Revoke current voucher and allocate a new one."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)

    # Find current active voucher
    current = next(
        (v for v in vouchers if v["assigned_to"] == reg_id and v["status"] == "allocated"),
        None
    )
    if current:
        revoke_voucher(current["voucher_id"], actor)

    # Allocate new
    result = allocate_voucher(reg_id, actor)
    return result


def mark_redeemed(voucher_id: str, actor: str) -> dict:
    """Mark a voucher as redeemed."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)

    v_index = next((i for i, v in enumerate(vouchers) if v["voucher_id"] == voucher_id), None)
    if v_index is None:
        return {"status": False, "message": "Voucher not found", "output": None}

    if vouchers[v_index]["status"] != "allocated":
        return {"status": False, "message": "Can only redeem allocated vouchers", "output": None}

    before = vouchers[v_index].copy()
    vouchers[v_index]["status"] = "redeemed"
    vouchers[v_index]["redeemed_date"] = get_timestamp()

    write_json(VOUCHERS_FILE, vouchers)
    log_action("Voucher", voucher_id, "redeemed", actor, before=before, after=vouchers[v_index])

    return {"status": True, "message": "Voucher marked as redeemed", "output": _sanitize_voucher(vouchers[v_index])}


def get_expiring_vouchers(days: int = 30) -> dict:
    """Get vouchers expiring within specified days."""
    ensure_file(VOUCHERS_FILE, [])
    vouchers = read_json(VOUCHERS_FILE)

    today = datetime.now().date()
    threshold = today + timedelta(days=days)

    expiring = []
    for v in vouchers:
        if v["status"] == "allocated":
            try:
                expiry = datetime.strptime(v["expiry_date"], "%Y-%m-%d").date()
                if today <= expiry <= threshold:
                    expiring.append(_sanitize_voucher(v))
            except (ValueError, KeyError):
                continue

    return {"status": True, "message": f"Found {len(expiring)} expiring vouchers", "output": expiring}


def _sanitize_voucher(voucher: dict) -> dict:
    """Return voucher data without the full code (only masked)."""
    sanitized = voucher.copy()
    sanitized.pop("code", None)
    return sanitized
