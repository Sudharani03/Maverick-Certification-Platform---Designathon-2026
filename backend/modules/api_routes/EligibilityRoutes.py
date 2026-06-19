"""
EligibilityRoutes — API endpoints for eligibility evaluation and approvals.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.api_modules.EligibilityComponent import (
    evaluate_eligibility, bulk_evaluate,
    approve_candidate, reject_candidate,
    get_eligibility_by_drive
)

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


class EvaluateRequest(BaseModel):
    reg_id: str
    user_id: str


class BulkEvaluateRequest(BaseModel):
    drive_id: str
    user_id: str


class ApproveRequest(BaseModel):
    elig_id: str
    user_id: str


class RejectRequest(BaseModel):
    elig_id: str
    user_id: str
    reason: str


class GetByDriveRequest(BaseModel):
    drive_id: str


@router.post("/evaluate")
async def evaluate_endpoint(request_data: EvaluateRequest):
    """Evaluate eligibility for a single candidate."""
    try:
        result = evaluate_eligibility(request_data.reg_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/bulk-evaluate")
async def bulk_evaluate_endpoint(request_data: BulkEvaluateRequest):
    """Evaluate eligibility for all registered candidates in a drive."""
    try:
        result = bulk_evaluate(request_data.drive_id, request_data.user_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/approve")
async def approve_endpoint(request_data: ApproveRequest):
    """Approve a pending candidate."""
    try:
        result = approve_candidate(request_data.elig_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/reject")
async def reject_endpoint(request_data: RejectRequest):
    """Reject a pending candidate."""
    try:
        result = reject_candidate(request_data.elig_id, request_data.user_id, request_data.reason)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-by-drive")
async def get_by_drive_endpoint(request_data: GetByDriveRequest):
    """Get all eligibility records for a drive."""
    try:
        result = get_eligibility_by_drive(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
