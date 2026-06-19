"""
Maverick Certification Hub — FastAPI Application Entry Point.
Manages MAP Certification Drives with local JSON file-based storage.
"""

import os
import sys

# Add backend directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from modules.api_routes.AuthRoute import router as auth_router
from modules.api_routes.DriveRoutes import router as drive_router
from modules.api_routes.RegistrationRoutes import router as registration_router
from modules.api_routes.EligibilityRoutes import router as eligibility_router
from modules.api_routes.ResultRoutes import router as result_router
from modules.api_routes.VoucherRoutes import router as voucher_router
from modules.api_routes.ReportRoutes import router as report_router
from modules.api_routes.AuditRoutes import router as audit_router
from modules.api_routes.CommunicationRoutes import router as communication_router
from modules.service_modules.FileManager import ensure_directory, DATA_DIR, UPLOADS_DIR

# Ensure data and uploads directories exist
ensure_directory(DATA_DIR)
ensure_directory(UPLOADS_DIR)

app = FastAPI(
    title="Maverick Certification Hub API",
    description="Backend API for MAP Certification Drive Automation",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routers
app.include_router(auth_router, prefix="/api")
app.include_router(drive_router, prefix="/api")
app.include_router(registration_router, prefix="/api")
app.include_router(eligibility_router, prefix="/api")
app.include_router(result_router, prefix="/api")
app.include_router(voucher_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(audit_router, prefix="/api")
app.include_router(communication_router, prefix="/api")

# Mount uploads directory for file downloads
if os.path.exists(UPLOADS_DIR):
    app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Maverick Certification Hub API is running"}


@app.get("/api/health")
async def health_check():
    """API health check."""
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8016, reload=True)
