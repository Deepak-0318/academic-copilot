from pydantic import BaseModel, Field


class AcademicPlannerRequest(BaseModel):
    subject: str = Field(min_length=2)
    courseCode: str | None = None
    branch: str = Field(min_length=2)
    semester: int = Field(ge=1, le=12)
    courseRole: str
    credits: float | None = Field(default=None, ge=0, le=20)
    hoursPerWeek: float | None = Field(default=None, ge=1, le=40)
    university: str | None = None
    regulation: str | None = None
    additionalRequirements: str | None = Field(
        default=None,
        max_length=2000,
    )


class CourseOutcome(BaseModel):
    code: str
    description: str


class LessonPlanItem(BaseModel):
    unit: str
    topic: str
    hours: float
    learningObjectives: list[str]
    teachingMethod: str
    bloomLevel: str


class AssessmentItem(BaseModel):
    type: str
    description: str
    weightage: float | None = None


class COPOMapping(BaseModel):
    courseOutcome: str
    mappings: dict[str, str]


class AcademicPlanResponse(BaseModel):
    courseOverview: str
    courseOutcomes: list[CourseOutcome]
    lessonPlan: list[LessonPlanItem]
    assessmentPlan: list[AssessmentItem]
    coPoMapping: list[COPOMapping]