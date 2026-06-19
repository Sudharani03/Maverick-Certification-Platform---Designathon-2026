"""
VoucherRoutes — API endpoints for voucher pool management and allocation.
"""

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from modules.api_modules.VoucherComponent import (
    add_vouchers_to_pool, allocate_voucher,
    auto_allocate_for_drive, get_vouchers_by_drive,
    revoke_voucher, reissue_voucher,
    mark_redeemed, get_expiring_vouchers
)

router = APIRouter(prefix="/vouchers", tags=["Vouchers"])


class AddPoolRequest(BaseModel):
    drive_id: str
    vendor: str
    value: float
    expiry_date: str
    codes: List[str]
    user_id: str


class AllocateRequest(BaseModel):
    reg_id: str
    user_id: str


class AutoAllocateRequest(BaseModel):
    drive_id: str
    user_id: str


class GetByDriveRequest(BaseModel):
    drive_id: str


class VoucherActionRequest(BaseModel):
    voucher_id: str
    user_id: str


class ReissueRequest(BaseModel):
    reg_id: str
    user_id: str


class GetExpiringRequest(BaseModel):
    days: int = 30


@router.post("/add-pool")
async def add_pool_endpoint(request_data: AddPoolRequest):
    """Add vouchers to the pool."""
    try:
        result = add_vouchers_to_pool(
            drive_id=request_data.drive_id,
            vendor=request_data.vendor,
            value=request_data.value,
            expiry_date=request_data.expiry_date,
            codes=request_data.codes,
            actor=request_data.user_id,
        )
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/bulk-add")
async def bulk_add_endpoint(
    drive_id: str = Form(...),
    vendor: str = Form(...),
    value: float = Form(...),
    expiry_date: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    """Bulk add vouchers from CSV file (one code per line or column 'code')."""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        # Parse codes: one per line
        codes = [line.strip() for line in text.splitlines() if line.strip()]
        # If first line looks like a header, skip it
        if codes and codes[0].lower() in ["code", "voucher_code", "codes"]:
            codes = codes[1:]

        result = add_vouchers_to_pool(drive_id, vendor, value, expiry_date, codes, user_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/allocate")
async def allocate_endpoint(request_data: AllocateRequest):
    """Allocate a voucher to a single candidate."""
    try:
        result = allocate_voucher(request_data.reg_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/auto-allocate")
async def auto_allocate_endpoint(request_data: AutoAllocateRequest):
    """Auto-allocate vouchers to all passed candidates."""
    try:
        result = auto_allocate_for_drive(request_data.drive_id, request_data.user_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-by-drive")
async def get_by_drive_endpoint(request_data: GetByDriveRequest):
    """Get all vouchers for a drive (masked codes)."""
    try:
        result = get_vouchers_by_drive(request_data.drive_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/revoke")
async def revoke_endpoint(request_data: VoucherActionRequest):
    """Revoke an allocated voucher."""
    try:
        result = revoke_voucher(request_data.voucher_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/reissue")
async def reissue_endpoint(request_data: ReissueRequest):
    """Revoke current voucher and allocate a new one."""
    try:
        result = reissue_voucher(request_data.reg_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/mark-redeemed")
async def mark_redeemed_endpoint(request_data: VoucherActionRequest):
    """Mark a voucher as redeemed."""
    try:
        result = mark_redeemed(request_data.voucher_id, request_data.user_id)
        status_code = 200 if result["status"] else 400
        return JSONResponse(status_code=status_code, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-expiring")
async def get_expiring_endpoint(request_data: GetExpiringRequest):
    """Get vouchers expiring within specified days."""
    try:
        result = get_expiring_vouchers(request_data.days)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
