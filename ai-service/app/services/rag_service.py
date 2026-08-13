from __future__ import annotations

import json

from app.llm.groq_provider import GroqProvider
from app.prompts.rag import SYSTEM_PROMPT, build_user_prompt
from app.retrieval.context_builder import build_context
from app.retrieval.service import AcademicRetrievalService
from app.schemas.rag import RAGRequest, RAGResponse, RAGSource


class RAGService:
    """Orchestrates academic retrieval and grounded answer generation."""

    def __init__(
        self,
        retrieval_service: AcademicRetrievalService | None = None ,
        llm: GroqProvider | None = None,
    ) -> None:
        self.retrieval_service = (
            retrieval_service 
            if retrieval_service is not None
            else AcademicRetrievalService()
        )
        self.llm = (
            llm
            if llm is not None
            else GroqProvider()
        )

    async def ask(
        self,
        request: RAGRequest,
    ) -> RAGResponse:

        results = self.retrieval_service.search(
            request.question,
            limit=request.top_k,
            subject=request.subject,
            course_code=request.course_code,
            semester=request.semester,
        )

        if not results:
            return RAGResponse(
                answer=(
                    "The available academic documents do not contain "
                    "enough information to answer this question."
                ),
                sources=[],
            )

        context = build_context(results)

        if not context:
            return RAGResponse(
                answer=(
                    "The available academic documents do not contain "
                    "enough information to answer this question."
                ),
                sources=[],
            )

        user_prompt = build_user_prompt(
            request.question,
            context,
        )

        raw_response = await self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        parsed_response = self._parse_llm_response(
            raw_response
        )

        answer = parsed_response.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError(
                "LLM response did not contain a valid answer."
            )

        source_indexes = parsed_response.get(
            "source_indexes",
            [],
        )

        if not isinstance(source_indexes, list):
            raise RuntimeError(
                "LLM response contained invalid source indexes."
            )

        sources = self._build_sources(
            results,
            source_indexes,
        )

        return RAGResponse(
            answer=answer.strip(),
            sources=sources,
        )

    @staticmethod
    def _parse_llm_response(
        raw_response: str,
    ) -> dict:
        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "LLM returned invalid JSON."
            ) from exc

        answer = parsed.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError(
                "LLM response must be a JSON object."
            )

        return parsed

    @staticmethod
    def _build_sources(
        results: list[dict],
        source_indexes: list,
    ) -> list[RAGSource]:

        sources: list[RAGSource] = []

        for source_index in source_indexes:

            if not isinstance(source_index, int):
                continue

            if source_index < 1 or source_index > len(results):
                continue

            result = results[source_index - 1]

            sources.append(
                RAGSource(
                    document_id=result["document_id"],
                    chunk_id=result["chunk_id"],
                    section=result.get("section"),
                    chunk_index=result["chunk_index"],
                )
            )

        return sources