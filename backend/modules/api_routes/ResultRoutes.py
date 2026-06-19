"""
ResultRoutes — API endpoints for assessment results.
"""

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.api_modules.ResultComponent import (
    import_result, bulk_import_results,
    get_results_by_drive, save_evidence_file
)

router = APIRouter(prefix="/results", tags=["Results"])


class ImportResultRequest(BaseModel):
    reg_id: str
    score: float
    exam_date: str
    evidence_filename: str = ""
    user_id: str


class GetByDriveRequest(BaseModel):
    drive_id: str


@router.post("/import")
async def import_result_endpoint(request_data: ImportResultRequest):
    """Import a single assessment result."""
    try:
        result = import_result(
            reg_id=request_data.reg_id,
            score=request_data.score,
            exam_date=request_data.exam_date,
            evidence_filename=request_data.evidence_filename,
            actor=request_data.user_id,
        )
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/bulk-import")
async def bulk_import_endpoint(
    drive_id: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Bulk import results from CSV file."""
    try:
        content = await file.read()
        csv_content = content.decode("utf-8")
        result = bulk_import_results(drive_id, csv_content, user_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-by-drive")
async def get_by_drive_endpoint(request_data: GetByDriveRequest):
    """Get all results for a drive."""
    try:
        result = get_results_by_drive(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/upload-evidence")
async def upload_evidence_endpoint(
    drive_id: str = Form(...),
    reg_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload evidence file for an assessment result."""
    try:
        content = await file.read()
        result = save_evidence_file(drive_id, reg_id, file.filename, content)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
