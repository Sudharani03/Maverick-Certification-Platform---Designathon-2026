"""
AuthRoute — Simplified login endpoint. No real auth — just returns user object by role.
"""

import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.service_modules.FileManager import DATA_DIR, read_json

router = APIRouter(prefix="/auth", tags=["Auth"])

USERS_FILE = os.path.join(DATA_DIR, "users.json")


class LoginRequest(BaseModel):
    role: str  # "Admin" or "User"


@router.post("/login")
async def login(request_data: LoginRequest):
    """Dummy login — returns user object based on role selection."""
    try:
        users = read_json(USERS_FILE)
        user = next(
            (u for u in users if u["role"].lower() == request_data.role.lower()),
            None
        )

        if not user:
            return JSONResponse(
                status_code=400,
                content={"data": None, "message": "Invalid role specified"}
            )

        return JSONResponse(
            status_code=200,
            content={"data": user, "message": "Login successful"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"data": None, "message": str(e)}
        )
