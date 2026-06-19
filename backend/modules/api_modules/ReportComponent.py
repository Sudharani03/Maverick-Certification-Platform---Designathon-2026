"""
ReportComponent — Business logic for reporting and dashboard analytics.
"""

import os
from datetime import datetime
from modules.service_modules.FileManager import DATA_DIR, read_json, ensure_file

DRIVES_FILE = os.path.join(DATA_DIR, "drives.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")
ELIGIBILITY_FILE = os.path.join(DATA_DIR, "eligibility.json")
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")
VOUCHERS_FILE = os.path.join(DATA_DIR, "vouchers.json")


def get_drive_summary(drive_id: str) -> dict:
    """Get aggregated summary for a single drive."""
    registrations = read_json(REGISTRATIONS_FILE)
    eligibility = read_json(ELIGIBILITY_FILE)
    results = read_json(RESULTS_FILE)
    vouchers = read_json(VOUCHERS_FILE)

    drive_regs = [r for r in registrations if r["drive_id"] == drive_id]
    drive_elig = [e for e in eligibility if e["drive_id"] == drive_id]
    drive_results = [r for r in results if r["drive_id"] == drive_id]
    drive_vouchers = [v for v in vouchers if v["drive_id"] == drive_id]

    summary = {
        "total_registered": len(drive_regs),
        "eligible": len([e for e in drive_elig if e["decision"] == "eligible"]),
        "ineligible": len([e for e in drive_elig if e["decision"] == "ineligible"]),
        "pending_approval": len([e for e in drive_elig if e["decision"] == "pending_approval"]),
        "assessed": len(drive_results),
        "passed": len([r for r in drive_results if r["outcome"] == "passed"]),
        "failed": len([r for r in drive_results if r["outcome"] == "failed"]),
        "vouchers_total": len(drive_vouchers),
        "vouchers_available": len([v for v in drive_vouchers if v["status"] == "available"]),
        "vouchers_allocated": len([v for v in drive_vouchers if v["status"] == "allocated"]),
        "vouchers_redeemed": len([v for v in drive_vouchers if v["status"] == "redeemed"]),
        "vouchers_expired": len([v for v in drive_vouchers if v["status"] == "expired"]),
    }

    return {"status": True, "message": "Drive summary generated", "output": summary}


def get_funnel_data(drive_id: str) -> dict:
    """Get certification journey funnel data."""
    registrations = read_json(REGISTRATIONS_FILE)
    eligibility = read_json(ELIGIBILITY_FILE)
    results = read_json(RESULTS_FILE)
    vouchers = read_json(VOUCHERS_FILE)

    drive_regs = [r for r in registrations if r["drive_id"] == drive_id]
    drive_elig = [e for e in eligibility if e["drive_id"] == drive_id and e["decision"] == "eligible"]
    drive_results = [r for r in results if r["drive_id"] == drive_id]
    drive_passed = [r for r in drive_results if r["outcome"] == "passed"]
    drive_vouchers_issued = [v for v in vouchers if v["drive_id"] == drive_id and v["status"] in ["allocated", "redeemed"]]
    drive_vouchers_redeemed = [v for v in vouchers if v["drive_id"] == drive_id and v["status"] == "redeemed"]

    funnel = [
        {"step": "Registered", "count": len(drive_regs)},
        {"step": "Eligible", "count": len(drive_elig)},
        {"step": "Assessed", "count": len(drive_results)},
        {"step": "Passed", "count": len(drive_passed)},
        {"step": "Voucher Issued", "count": len(drive_vouchers_issued)},
        {"step": "Redeemed", "count": len(drive_vouchers_redeemed)},
    ]

    return {"status": True, "message": "Funnel data generated", "output": funnel}


def get_pass_fail_by_track(drive_id: str) -> dict:
    """Get pass/fail breakdown by exam track."""
    registrations = read_json(REGISTRATIONS_FILE)
    results = read_json(RESULTS_FILE)

    drive_results = [r for r in results if r["drive_id"] == drive_id]

    # Map reg_id to exam_track
    reg_map = {r["reg_id"]: r["exam_track"] for r in registrations if r["drive_id"] == drive_id}

    tracks = {}
    for result in drive_results:
        track = reg_map.get(result["reg_id"], "Unknown")
        if track not in tracks:
            tracks[track] = {"track": track, "passed": 0, "failed": 0}
        if result["outcome"] == "passed":
            tracks[track]["passed"] += 1
        else:
            tracks[track]["failed"] += 1

    return {"status": True, "message": "Pass/fail by track generated", "output": list(tracks.values())}


def get_voucher_utilization(drive_id: str) -> dict:
    """Get voucher utilization statistics."""
    vouchers = read_json(VOUCHERS_FILE)
    drive_vouchers = [v for v in vouchers if v["drive_id"] == drive_id]

    total = len(drive_vouchers)
    allocated = len([v for v in drive_vouchers if v["status"] == "allocated"])
    redeemed = len([v for v in drive_vouchers if v["status"] == "redeemed"])
    expired = len([v for v in drive_vouchers if v["status"] == "expired"])
    available = len([v for v in drive_vouchers if v["status"] == "available"])

    issued = allocated + redeemed
    utilization_pct = round((redeemed / issued * 100), 1) if issued > 0 else 0

    # Calculate avg days to redeem
    days_list = []
    for v in drive_vouchers:
        if v["status"] == "redeemed" and v.get("allocated_date") and v.get("redeemed_date"):
            try:
                alloc = datetime.fromisoformat(v["allocated_date"].replace("Z", "+00:00"))
                redeem = datetime.fromisoformat(v["redeemed_date"].replace("Z", "+00:00"))
                days_list.append((redeem - alloc).days)
            except (ValueError, TypeError):
                continue

    avg_days = round(sum(days_list) / len(days_list), 1) if days_list else 0

    utilization = {
        "total_pool": total,
        "available": available,
        "allocated": allocated,
        "redeemed": redeemed,
        "expired": expired,
        "utilization_percentage": utilization_pct,
        "avg_days_to_redeem": avg_days,
    }

    return {"status": True, "message": "Voucher utilization generated", "output": utilization}


def get_overall_stats() -> dict:
    """Get aggregate stats across all drives."""
    drives = read_json(DRIVES_FILE)
    registrations = read_json(REGISTRATIONS_FILE)
    results = read_json(RESULTS_FILE)
    vouchers = read_json(VOUCHERS_FILE)

    total_candidates = len(registrations)
    total_passed = len([r for r in results if r["outcome"] == "passed"])
    total_failed = len([r for r in results if r["outcome"] == "failed"])
    total_assessed = total_passed + total_failed
    pass_rate = round((total_passed / total_assessed * 100), 1) if total_assessed > 0 else 0

    total_voucher_value = sum(v["value"] for v in vouchers if v["status"] in ["allocated", "redeemed"])
    total_redeemed = len([v for v in vouchers if v["status"] == "redeemed"])
    total_issued = len([v for v in vouchers if v["status"] in ["allocated", "redeemed"]])
    overall_utilization = round((total_redeemed / total_issued * 100), 1) if total_issued > 0 else 0

    stats = {
        "total_drives": len(drives),
        "active_drives": len([d for d in drives if d["status"] == "active"]),
        "total_candidates": total_candidates,
        "total_assessed": total_assessed,
        "total_passed": total_passed,
        "overall_pass_rate": pass_rate,
        "total_voucher_spend": total_voucher_value,
        "total_vouchers_issued": total_issued,
        "total_vouchers_redeemed": total_redeemed,
        "overall_utilization": overall_utilization,
    }

    return {"status": True, "message": "Overall stats generated", "output": stats}
