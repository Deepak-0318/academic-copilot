from fastapi import APIRouter, HTTPException

from app.schemas.rag import RAGRequest, RAGResponse
from app.services.rag_service import RAGService


router = APIRouter()

rag_service = RAGService()


@router.post(
    "/ask",
    response_model=RAGResponse,
)
async def ask_academic_question(
    request: RAGRequest,
):
    try:
        return await rag_service.ask(request)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc