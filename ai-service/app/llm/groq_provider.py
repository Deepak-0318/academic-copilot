from groq import AsyncGroq

from app.config.settings import settings
from app.llm.base import LLMProvider


class GroqProvider(LLMProvider):

    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return content