"""
ReportRoutes — API endpoints for reporting and dashboard analytics.
"""

import csv
import io
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from modules.api_modules.ReportComponent import (
    get_drive_summary, get_funnel_data,
    get_pass_fail_by_track, get_voucher_utilization,
    get_overall_stats
)

router = APIRouter(prefix="/reports", tags=["Reports"])


class DriveRequest(BaseModel):
    drive_id: str


class ExportRequest(BaseModel):
    drive_id: str
    report_type: str  # "summary", "funnel", "pass_fail", "utilization"


@router.post("/drive-summary")
async def drive_summary_endpoint(request_data: DriveRequest):
    """Get drive summary statistics."""
    try:
        result = get_drive_summary(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/funnel")
async def funnel_endpoint(request_data: DriveRequest):
    """Get certification journey funnel data."""
    try:
        result = get_funnel_data(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/pass-fail-trends")
async def pass_fail_endpoint(request_data: DriveRequest):
    """Get pass/fail breakdown by exam track."""
    try:
        result = get_pass_fail_by_track(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/voucher-utilization")
async def voucher_utilization_endpoint(request_data: DriveRequest):
    """Get voucher utilization stats."""
    try:
        result = get_voucher_utilization(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/overall-stats")
async def overall_stats_endpoint():
    """Get overall stats across all drives."""
    try:
        result = get_overall_stats()
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/export-csv")
async def export_csv_endpoint(request_data: ExportRequest):
    """Export report data as CSV download."""
    try:
        # Get the appropriate data
        if request_data.report_type == "summary":
            result = get_drive_summary(request_data.drive_id)
            data = result["output"]
            # Convert dict to list of rows
            rows = [{"metric": k, "value": v} for k, v in data.items()]
        elif request_data.report_type == "funnel":
            result = get_funnel_data(request_data.drive_id)
            rows = result["output"]
        elif request_data.report_type == "pass_fail":
            result = get_pass_fail_by_track(request_data.drive_id)
            rows = result["output"]
        elif request_data.report_type == "utilization":
            result = get_voucher_utilization(request_data.drive_id)
            data = result["output"]
            rows = [{"metric": k, "value": v} for k, v in data.items()]
        else:
            return JSONResponse(status_code=400, content={"data": None, "message": "Invalid report type"})

        if not rows:
            return JSONResponse(status_code=400, content={"data": None, "message": "No data to export"})

        # Generate CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

        response = StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={request_data.report_type}_report.csv"}
        )
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
