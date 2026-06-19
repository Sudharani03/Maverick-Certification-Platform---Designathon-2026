"""
EligibilityComponent — Business logic for eligibility evaluation and approvals.
"""

import os
from modules.service_modules.FileManager import DATA_DIR, read_json, write_json, ensure_file
from modules.service_modules.HelperFunctions import generate_id, get_timestamp
from modules.api_modules.AuditComponent import log_action
from modules.api_modules.CommunicationComponent import trigger_communication

ELIGIBILITY_FILE = os.path.join(DATA_DIR, "eligibility.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")


def evaluate_eligibility(reg_id: str, actor: str) -> dict:
    """Evaluate eligibility for a single registration using rules engine."""
    ensure_file(ELIGIBILITY_FILE, [])
    ensure_file(REGISTRATIONS_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    if not reg:
        return {"status": False, "message": "Registration not found", "output": None}

    # Check if already evaluated
    eligibility_records = read_json(ELIGIBILITY_FILE)
    existing = next((e for e in eligibility_records if e["reg_id"] == reg_id), None)
    if existing:
        return {"status": False, "message": "Eligibility already evaluated for this candidate", "output": existing}

    # Get drive details for rules
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == reg["drive_id"]), None)
    if not drive:
        return {"status": False, "message": "Drive not found", "output": None}

    # Apply rules engine
    criteria = _apply_rules(reg, drive, registrations)
    all_passed = all([
        criteria["tenure_check"],
        criteria["training_complete"],
        criteria["prior_attempts_check"],
        criteria["budget_check"],
    ])

    decision = "eligible" if all_passed else "ineligible"

    elig_record = {
        "elig_id": generate_id("elig"),
        "reg_id": reg_id,
        "drive_id": reg["drive_id"],
        "criteria": criteria,
        "decision": decision,
        "approver": actor if all_passed else None,
        "decision_date": get_timestamp(),
        "notes": "" if all_passed else _get_failure_reasons(criteria),
    }

    eligibility_records.append(elig_record)
    write_json(ELIGIBILITY_FILE, eligibility_records)

    # Update registration status
    _update_reg_status(reg_id, decision, registrations)

    # Audit
    log_action("Eligibility", elig_record["elig_id"], "evaluated", actor,
               before=None, after=elig_record)

    # Communication
    drive_name = drive["name"]
    template_key = "eligibility_approved" if decision == "eligible" else "eligibility_rejected"
    context = {
        "candidate_name": reg["name"],
        "drive_name": drive_name,
        "reason": elig_record["notes"],
    }
    trigger_communication(reg_id, template_key, context)

    return {"status": True, "message": f"Candidate evaluated as {decision}", "output": elig_record}


def bulk_evaluate(drive_id: str, actor: str) -> dict:
    """Evaluate eligibility for all registered candidates in a drive."""
    ensure_file(REGISTRATIONS_FILE, [])
    ensure_file(ELIGIBILITY_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    eligibility_records = read_json(ELIGIBILITY_FILE)

    drive_regs = [r for r in registrations if r["drive_id"] == drive_id and r["status"] == "registered"]
    already_evaluated = {e["reg_id"] for e in eligibility_records}

    to_evaluate = [r for r in drive_regs if r["reg_id"] not in already_evaluated]

    results = {"eligible": 0, "ineligible": 0, "total": len(to_evaluate)}

    for reg in to_evaluate:
        result = evaluate_eligibility(reg["reg_id"], actor)
        if result["status"] and result["output"]:
            if result["output"]["decision"] == "eligible":
                results["eligible"] += 1
            else:
                results["ineligible"] += 1

    return {"status": True, "message": f"Evaluated {results['total']} candidates", "output": results}


def approve_candidate(elig_id: str, approver: str) -> dict:
    """Approve a pending candidate."""
    ensure_file(ELIGIBILITY_FILE, [])
    eligibility_records = read_json(ELIGIBILITY_FILE)

    elig_index = next((i for i, e in enumerate(eligibility_records) if e["elig_id"] == elig_id), None)
    if elig_index is None:
        return {"status": False, "message": "Eligibility record not found", "output": None}

    before = eligibility_records[elig_index].copy()
    eligibility_records[elig_index]["decision"] = "eligible"
    eligibility_records[elig_index]["approver"] = approver
    eligibility_records[elig_index]["decision_date"] = get_timestamp()

    write_json(ELIGIBILITY_FILE, eligibility_records)

    # Update registration status
    reg_id = eligibility_records[elig_index]["reg_id"]
    registrations = read_json(REGISTRATIONS_FILE)
    _update_reg_status(reg_id, "eligible", registrations)

    log_action("Eligibility", elig_id, "approved", approver, before=before, after=eligibility_records[elig_index])

    # Communication
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == eligibility_records[elig_index]["drive_id"]), None)
    if reg and drive:
        trigger_communication(reg_id, "eligibility_approved", {
            "candidate_name": reg["name"],
            "drive_name": drive["name"],
            "reason": "",
        })

    return {"status": True, "message": "Candidate approved", "output": eligibility_records[elig_index]}


def reject_candidate(elig_id: str, approver: str, reason: str) -> dict:
    """Reject a pending candidate."""
    ensure_file(ELIGIBILITY_FILE, [])
    eligibility_records = read_json(ELIGIBILITY_FILE)

    elig_index = next((i for i, e in enumerate(eligibility_records) if e["elig_id"] == elig_id), None)
    if elig_index is None:
        return {"status": False, "message": "Eligibility record not found", "output": None}

    before = eligibility_records[elig_index].copy()
    eligibility_records[elig_index]["decision"] = "ineligible"
    eligibility_records[elig_index]["approver"] = approver
    eligibility_records[elig_index]["decision_date"] = get_timestamp()
    eligibility_records[elig_index]["notes"] = reason

    write_json(ELIGIBILITY_FILE, eligibility_records)

    # Update registration status
    reg_id = eligibility_records[elig_index]["reg_id"]
    registrations = read_json(REGISTRATIONS_FILE)
    _update_reg_status(reg_id, "ineligible", registrations)

    log_action("Eligibility", elig_id, "rejected", approver, before=before, after=eligibility_records[elig_index])

    # Communication
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == eligibility_records[elig_index]["drive_id"]), None)
    if reg and drive:
        trigger_communication(reg_id, "eligibility_rejected", {
            "candidate_name": reg["name"],
            "drive_name": drive["name"],
            "reason": reason,
        })

    return {"status": True, "message": "Candidate rejected", "output": eligibility_records[elig_index]}


def get_eligibility_by_drive(drive_id: str) -> dict:
    """Get all eligibility records for a drive."""
    ensure_file(ELIGIBILITY_FILE, [])
    records = read_json(ELIGIBILITY_FILE)
    filtered = [e for e in records if e["drive_id"] == drive_id]
    return {"status": True, "message": f"Found {len(filtered)} records", "output": filtered}


def _apply_rules(registration: dict, drive: dict, all_registrations: list) -> dict:
    """Apply eligibility rules engine."""
    prior_attempts = registration.get("prior_attempts", 0)

    # Rule 1: Tenure check (simulated — we assume tenure >= 90 days if prior_attempts < 5)
    tenure_days = 120  # Simulated
    tenure_check = tenure_days >= 90

    # Rule 2: Training completion (simulated — always true for demo)
    training_complete = True

    # Rule 3: Prior attempts < 2
    prior_attempts_check = prior_attempts < 2

    # Rule 4: Budget check (count eligible candidates vs target)
    eligible_count = len([
        r for r in all_registrations
        if r["drive_id"] == drive["drive_id"] and r["status"] == "eligible"
    ])
    budget_check = eligible_count < drive.get("target_count", 999)

    return {
        "tenure_days": tenure_days,
        "tenure_check": tenure_check,
        "training_complete": training_complete,
        "prior_attempts": prior_attempts,
        "prior_attempts_check": prior_attempts_check,
        "budget_check": budget_check,
    }


def _get_failure_reasons(criteria: dict) -> str:
    """Generate human-readable failure reasons."""
    reasons = []
    if not criteria["tenure_check"]:
        reasons.append("Tenure less than 90 days")
    if not criteria["training_complete"]:
        reasons.append("Training not completed")
    if not criteria["prior_attempts_check"]:
        reasons.append(f"Prior attempts ({criteria['prior_attempts']}) exceed limit of 2")
    if not criteria["budget_check"]:
        reasons.append("Drive target count reached (budget limit)")
    return "; ".join(reasons)


def _update_reg_status(reg_id: str, status: str, registrations: list) -> None:
    """Helper to update registration status in the registrations list and save."""
    for i, r in enumerate(registrations):
        if r["reg_id"] == reg_id:
            registrations[i]["status"] = status
            break
    write_json(REGISTRATIONS_FILE, registrations)
