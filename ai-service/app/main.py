from fastapi import FastAPI

from app.api.planner import router as planner_router


app = FastAPI(
    title="Academic Co-Pilot AI Service",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "academic-copilot-ai",
    }


app.include_router(
    planner_router,
    prefix="/api/v1/planner",
)