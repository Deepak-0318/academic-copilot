import pytest

from app.services.rag_service import RAGService
from app.schemas.rag import RAGRequest


class FakeRetrievalService:

    def __init__(self, results):
        self.results = results
        self.last_kwargs = None

    def search(self, query, **kwargs):
        self.last_kwargs = {
            "query": query,
            **kwargs,
        }
        return self.results


class FakeLLM:

    def __init__(self, response):
        self.response = response
        self.last_system_prompt = None
        self.last_user_prompt = None

    async def generate(
        self,
        system_prompt,
        user_prompt,
    ):
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return self.response


def make_result(
    *,
    chunk_id="chunk-1",
    document_id="document-1",
    section="course_objectives",
    chunk_index=1,
    content="Course objectives content.",
    similarity=0.85,
):
    return {
        "chunk_id": chunk_id,
        "document_id": document_id,
        "chunk_index": chunk_index,
        "section": section,
        "content": content,
        "similarity": similarity,
        "distance": 1.0 - similarity,
        "metadata": {},
    }


@pytest.mark.asyncio
async def test_returns_grounded_answer_and_sources():
    retrieval = FakeRetrievalService(
        [
            make_result(
                section="course_objectives",
                content="Understand fundamental programming concepts.",
            )
        ]
    )

    llm = FakeLLM(
        '{"answer": "The course teaches fundamental programming concepts.", '
        '"source_indexes": [1]}'
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    response = await service.ask(
        RAGRequest(
            question="What are the objectives?"
        )
    )

    assert response.answer == (
        "The course teaches fundamental programming concepts."
    )

    assert len(response.sources) == 1
    assert response.sources[0].section == "course_objectives"
    assert response.sources[0].chunk_index == 1

    assert retrieval.last_kwargs["query"] == (
        "What are the objectives?"
    )


@pytest.mark.asyncio
async def test_passes_course_filters_to_retrieval():
    retrieval = FakeRetrievalService(
        [
            make_result(
                section="course_objectives",
            )
        ]
    )

    llm = FakeLLM(
        '{"answer": "Course objectives.", "source_indexes": [1]}'
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    await service.ask(
        RAGRequest(
            question="What are the objectives?",
            subject="Data Structures using C",
            course_code="CS1083",
            semester=2,
            top_k=3,
        )
    )

    assert retrieval.last_kwargs["limit"] == 3
    assert retrieval.last_kwargs["subject"] == (
        "Data Structures using C"
    )
    assert retrieval.last_kwargs["course_code"] == "CS1083"
    assert retrieval.last_kwargs["semester"] == 2


@pytest.mark.asyncio
async def test_returns_refusal_when_no_context_is_retrieved():
    retrieval = FakeRetrievalService([])

    llm = FakeLLM(
        '{"answer": "This should not be called.", '
        '"source_indexes": []}'
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    response = await service.ask(
        RAGRequest(
            question="What is the course objective?"
        )
    )

    assert response.answer == (
        "The available academic documents do not contain enough "
        "information to answer this question."
    )

    assert response.sources == []

    assert llm.last_system_prompt is None


@pytest.mark.asyncio
async def test_maps_multiple_source_indexes():
    retrieval = FakeRetrievalService(
        [
            make_result(
                chunk_id="chunk-1",
                section="references",
                chunk_index=4,
            ),
            make_result(
                chunk_id="chunk-2",
                section="lesson_plan",
                chunk_index=8,
            ),
        ]
    )

    llm = FakeLLM(
        '{"answer": "Recommended references are listed in the document.", '
        '"source_indexes": [1, 2]}'
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    response = await service.ask(
        RAGRequest(
            question="What references are recommended?"
        )
    )

    assert len(response.sources) == 2

    assert response.sources[0].chunk_id == "chunk-1"
    assert response.sources[0].section == "references"

    assert response.sources[1].chunk_id == "chunk-2"
    assert response.sources[1].section == "lesson_plan"


@pytest.mark.asyncio
async def test_ignores_invalid_source_indexes():
    retrieval = FakeRetrievalService(
        [
            make_result(
                chunk_id="chunk-1",
                section="references",
            )
        ]
    )

    llm = FakeLLM(
        '{"answer": "References are available.", '
        '"source_indexes": [1, 99, 0, -1]}'
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    response = await service.ask(
        RAGRequest(
            question="What references are available?"
        )
    )

    assert len(response.sources) == 1
    assert response.sources[0].chunk_id == "chunk-1"


@pytest.mark.asyncio
async def test_rejects_invalid_llm_json():
    retrieval = FakeRetrievalService(
        [
            make_result()
        ]
    )

    llm = FakeLLM(
        "This is not JSON."
    )

    service = RAGService(
        retrieval_service=retrieval,
        llm=llm,
    )

    with pytest.raises(RuntimeError, match="invalid JSON"):
        await service.ask(
            RAGRequest(
                question="What are the objectives?"
            )
        )