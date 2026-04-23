from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_analysis import router as analysis_router
from app.api.routes_health import router as health_router
from app.api.routes_report import router as report_router
from app.api.routes_upload import router as upload_router
from app.core.config import ensure_directories, settings

ensure_directories()

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(report_router)


@app.get("/")
def root() -> dict:
    return {"message": f"{settings.app_name} backend is running."}
