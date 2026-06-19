"""
DriveRoutes — API endpoints for certification drive management.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from modules.api_modules.DriveComponent import (
    create_drive, get_all_drives, get_drive_by_id,
    update_drive, close_drive, delete_drive
)

router = APIRouter(prefix="/drives", tags=["Drives"])


class CreateDriveRequest(BaseModel):
    name: str
    sponsor: str
    budget: float
    start_date: str
    end_date: str
    target_count: int
    policy_notes: str = ""
    pass_threshold: int = 70
    user_id: str


class GetDriveDetailsRequest(BaseModel):
    drive_id: str


class UpdateDriveRequest(BaseModel):
    drive_id: str
    user_id: str
    name: Optional[str] = None
    sponsor: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    target_count: Optional[int] = None
    policy_notes: Optional[str] = None
    pass_threshold: Optional[int] = None


class CloseDriveRequest(BaseModel):
    drive_id: str
    user_id: str


class DeleteDriveRequest(BaseModel):
    drive_id: str
    user_id: str


@router.post("/create")
async def create_drive_endpoint(request_data: CreateDriveRequest):
    """Create a new certification drive."""
    try:
        result = create_drive(
            name=request_data.name,
            sponsor=request_data.sponsor,
            budget=request_data.budget,
            start_date=request_data.start_date,
            end_date=request_data.end_date,
            target_count=request_data.target_count,
            policy_notes=request_data.policy_notes,
            pass_threshold=request_data.pass_threshold,
            created_by=request_data.user_id,
        )
        status_code = 201 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-all")
async def get_all_drives_endpoint():
    """Get all drives."""
    try:
        result = get_all_drives()
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-details")
async def get_drive_details_endpoint(request_data: GetDriveDetailsRequest):
    """Get drive details by ID."""
    try:
        result = get_drive_by_id(request_data.drive_id)
        status_code = 200 if result["status"] else 404
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/update")
async def update_drive_endpoint(request_data: UpdateDriveRequest):
    """Update drive metadata."""
    try:
        updates = {}
        for field in ["name", "sponsor", "budget", "start_date", "end_date", "target_count", "policy_notes", "pass_threshold"]:
            val = getattr(request_data, field, None)
            if val is not None:
                updates[field] = val

        result = update_drive(request_data.drive_id, updates, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/close")
async def close_drive_endpoint(request_data: CloseDriveRequest):
    """Close a drive."""
    try:
        result = close_drive(request_data.drive_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/delete")
async def delete_drive_endpoint(request_data: DeleteDriveRequest):
    """Delete a drive."""
    try:
        result = delete_drive(request_data.drive_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
