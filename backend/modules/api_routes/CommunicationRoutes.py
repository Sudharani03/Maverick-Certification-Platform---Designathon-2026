"""
CommunicationRoutes — API endpoints for communication history.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.api_modules.CommunicationComponent import get_communications_by_registration

router = APIRouter(prefix="/communications", tags=["Communications"])


class GetByRegistrationRequest(BaseModel):
    reg_id: str


@router.post("/get-by-registration")
async def get_by_registration_endpoint(request_data: GetByRegistrationRequest):
    """Get all communications for a registration."""
    try:
        result = get_communications_by_registration(request_data.reg_id)
        return JSONResponse(status_code=200, content={"data": result["output"], "message": result["message"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": None, "message": str(e)})
