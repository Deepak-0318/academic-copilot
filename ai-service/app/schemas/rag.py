from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=2000,
    )

    subject: str | None = None
    course_code: str | None = None
    semester: int | None = Field(
        default=None,
        ge=1,
        le=12,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
    )


class RAGSource(BaseModel):
    document_id: str
    chunk_id: str
    section: str | None
    chunk_index: int


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]