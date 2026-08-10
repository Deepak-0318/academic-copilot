from app.agents.lesson_plan_agent import LessonPlanAgent
from app.llm.groq_provider import GroqProvider
from app.schemas.planner import (
    AcademicPlanResponse,
    AcademicPlannerRequest,
)


class PlannerService:

    def __init__(self) -> None:
        self.agent = LessonPlanAgent(
            llm=GroqProvider()
        )

    async def generate_lesson_plan(
        self,
        request: AcademicPlannerRequest,
    ) -> AcademicPlanResponse:

        return await self.agent.run(request)