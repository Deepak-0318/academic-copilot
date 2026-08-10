from fastapi import APIRouter, HTTPException

from app.schemas.planner import (
    AcademicPlanResponse,
    AcademicPlannerRequest,
)
from app.services.planner_service import PlannerService


router = APIRouter()

planner_service = PlannerService()


@router.post(
    "/lesson-plan",
    response_model=AcademicPlanResponse,
)
async def generate_lesson_plan(
    request: AcademicPlannerRequest,
):
    try:
        return await planner_service.generate_lesson_plan(
            request
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc