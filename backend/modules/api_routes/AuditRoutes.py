"""
AuditRoutes — API endpoints for audit trail retrieval.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from modules.api_modules.AuditComponent import get_audit_logs, get_audit_by_entity

router = APIRouter(prefix="/audit", tags=["Audit"])


class GetLogsRequest(BaseModel):
    entity: Optional[str] = None
    action: Optional[str] = None
    actor: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class GetByEntityRequest(BaseModel):
    entity_type: str
    entity_id: str


@router.post("/get-logs")
async def get_logs_endpoint(request_data: GetLogsRequest):
    """Get audit logs with optional filters."""
    try:
        result = get_audit_logs(
            entity=request_data.entity,
            action=request_data.action,
            actor=request_data.actor,
            date_from=request_data.date_from,
            date_to=request_data.date_to,
        )
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})


@router.post("/get-by-entity")
async def get_by_entity_endpoint(request_data: GetByEntityRequest):
    """Get audit logs for a specific entity."""
    try:
        result = get_audit_by_entity(request_data.entity_type, request_data.entity_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
