"""
RegistrationRoutes — API endpoints for candidate registration.
"""

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.api_modules.RegistrationComponent import (
    register_candidate, get_registrations_by_drive,
    get_registration_by_id, update_registration_status,
    bulk_import_registrations
)

router = APIRouter(prefix="/registrations", tags=["Registrations"])


class RegisterRequest(BaseModel):
    drive_id: str
    emp_id: str
    name: str
    email: str
    bu: str
    location: str
    manager_email: str
    exam_track: str
    slot: str
    prior_attempts: int = 0
    user_id: str


class GetByDriveRequest(BaseModel):
    drive_id: str


class GetDetailsRequest(BaseModel):
    reg_id: str


class UpdateStatusRequest(BaseModel):
    reg_id: str
    status: str
    user_id: str


@router.post("/register")
async def register_endpoint(request_data: RegisterRequest):
    """Register a single candidate."""
    try:
        result = register_candidate(
            drive_id=request_data.drive_id,
            emp_id=request_data.emp_id,
            name=request_data.name,
            email=request_data.email,
            bu=request_data.bu,
            location=request_data.location,
            manager_email=request_data.manager_email,
            exam_track=request_data.exam_track,
            slot=request_data.slot,
            prior_attempts=request_data.prior_attempts,
            actor=request_data.user_id,
        )
        status_code = 201 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-by-drive")
async def get_by_drive_endpoint(request_data: GetByDriveRequest):
    """Get all registrations for a drive."""
    try:
        result = get_registrations_by_drive(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-details")
async def get_details_endpoint(request_data: GetDetailsRequest):
    """Get a single registration by ID."""
    try:
        result = get_registration_by_id(request_data.reg_id)
        status_code = 200 if result["status"] else 404
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/update-status")
async def update_status_endpoint(request_data: UpdateStatusRequest):
    """Update registration status."""
    try:
        result = update_registration_status(request_data.reg_id, request_data.status, request_data.user_id)
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
    """Bulk import registrations from CSV file."""
    try:
        content = await file.read()
        csv_content = content.decode("utf-8")
        result = bulk_import_registrations(drive_id, csv_content, user_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
