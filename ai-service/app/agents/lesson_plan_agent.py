import json

from app.llm.base import LLMProvider
from app.prompts.lesson_plan import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.schemas.planner import (
    AcademicPlanResponse,
    AcademicPlannerRequest,
)


class LessonPlanAgent:

    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def run(
        self,
        request: AcademicPlannerRequest,
    ) -> AcademicPlanResponse:

        course_data = request.model_dump()

        user_prompt = build_user_prompt(
            course_data
        )

        raw_response = await self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        try:
            parsed = json.loads(raw_response)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "LLM returned invalid JSON."
            ) from exc

        return AcademicPlanResponse.model_validate(
            parsed
        )