"""
ResultComponent — Business logic for assessment result management.
"""

import os
from modules.service_modules.FileManager import DATA_DIR, UPLOADS_DIR, read_json, write_json, ensure_file, ensure_directory
from modules.service_modules.HelperFunctions import generate_id, get_timestamp
from modules.api_modules.AuditComponent import log_action
from modules.api_modules.CommunicationComponent import trigger_communication

RESULTS_FILE = os.path.join(DATA_DIR, "results.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")


def import_result(reg_id: str, score: float, exam_date: str,
                  evidence_filename: str, actor: str) -> dict:
    """Import a single assessment result."""
    ensure_file(RESULTS_FILE, [])
    ensure_file(REGISTRATIONS_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    reg = next((r for r in registrations if r["reg_id"] == reg_id), None)
    if not reg:
        return {"status": False, "message": "Registration not found", "output": None}

    # Check candidate is eligible
    if reg["status"] not in ["eligible", "scheduled"]:
        return {"status": False, "message": f"Candidate status is '{reg['status']}', must be 'eligible' or 'scheduled'", "output": None}

    # Get drive for pass threshold
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == reg["drive_id"]), None)
    if not drive:
        return {"status": False, "message": "Drive not found", "output": None}

    pass_threshold = drive.get("pass_threshold", 70)
    outcome = "passed" if score >= pass_threshold else "failed"

    result_id = generate_id("res")
    result = {
        "result_id": result_id,
        "reg_id": reg_id,
        "drive_id": reg["drive_id"],
        "score": score,
        "pass_threshold": pass_threshold,
        "outcome": outcome,
        "exam_date": exam_date,
        "evidence_filename": evidence_filename or "",
        "uploaded_at": get_timestamp(),
    }

    results = read_json(RESULTS_FILE)
    results.append(result)
    write_json(RESULTS_FILE, results)

    # Update registration status
    reg_index = next(i for i, r in enumerate(registrations) if r["reg_id"] == reg_id)
    registrations[reg_index]["status"] = outcome
    write_json(REGISTRATIONS_FILE, registrations)

    # Audit
    log_action("Result", result_id, "created", actor, before=None, after=result)

    # Communication
    template_key = "result_passed" if outcome == "passed" else "result_failed"
    trigger_communication(reg_id, template_key, {
        "candidate_name": reg["name"],
        "drive_name": drive["name"],
        "score": str(score),
        "pass_threshold": str(pass_threshold),
    })

    return {"status": True, "message": f"Result imported — candidate {outcome}", "output": result}


def bulk_import_results(drive_id: str, csv_content: str, actor: str) -> dict:
    """Import results from CSV content. Columns: emp_id, score, exam_date"""
    import csv
    import io

    ensure_file(RESULTS_FILE, [])
    ensure_file(REGISTRATIONS_FILE, [])

    registrations = read_json(REGISTRATIONS_FILE)
    drives = read_json(DRIVES_FILE)
    drive = next((d for d in drives if d["drive_id"] == drive_id), None)
    if not drive:
        return {"status": False, "message": "Drive not found", "output": None}

    reader = csv.DictReader(io.StringIO(csv_content))
    success_count = 0
    error_count = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):
        emp_id = row.get("emp_id", "").strip()
        score_str = row.get("score", "").strip()
        exam_date = row.get("exam_date", "").strip()

        if not emp_id or not score_str:
            error_count += 1
            errors.append(f"Row {row_num}: Missing emp_id or score")
            continue

        try:
            score = float(score_str)
        except ValueError:
            error_count += 1
            errors.append(f"Row {row_num}: Invalid score '{score_str}'")
            continue

        # Find registration
        reg = next(
            (r for r in registrations if r["emp_id"] == emp_id and r["drive_id"] == drive_id),
            None
        )
        if not reg:
            error_count += 1
            errors.append(f"Row {row_num}: No registration found for {emp_id}")
            continue

        if reg["status"] not in ["eligible", "scheduled"]:
            error_count += 1
            errors.append(f"Row {row_num}: {emp_id} status is '{reg['status']}', cannot import result")
            continue

        result = import_result(reg["reg_id"], score, exam_date, "", actor)
        if result["status"]:
            success_count += 1
            # Reload registrations since import_result modified the file
            registrations = read_json(REGISTRATIONS_FILE)
        else:
            error_count += 1
            errors.append(f"Row {row_num}: {result['message']}")

    return {
        "status": True,
        "message": f"Imported {success_count} results, {error_count} errors",
        "output": {"success_count": success_count, "error_count": error_count, "errors": errors}
    }


def get_results_by_drive(drive_id: str) -> dict:
    """Get all results for a drive."""
    ensure_file(RESULTS_FILE, [])
    results = read_json(RESULTS_FILE)
    filtered = [r for r in results if r["drive_id"] == drive_id]
    filtered.sort(key=lambda x: x["uploaded_at"], reverse=True)
    return {"status": True, "message": f"Found {len(filtered)} results", "output": filtered}


def save_evidence_file(drive_id: str, reg_id: str, filename: str, file_content: bytes) -> dict:
    """Save an uploaded evidence file to the local file system."""
    evidence_dir = os.path.join(UPLOADS_DIR, drive_id, "03_Assessments")
    ensure_directory(evidence_dir)

    # Create safe filename
    ext = os.path.splitext(filename)[1] if "." in filename else ".pdf"
    safe_filename = f"{reg_id}_evidence{ext}"
    file_path = os.path.join(evidence_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(file_content)

    return {"status": True, "message": "Evidence file saved", "output": {"filename": safe_filename}}
