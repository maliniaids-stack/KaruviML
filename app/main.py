from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from groq import Groq

from app.config import Settings, get_settings
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]
usage_log: list[dict] = []

@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }

@app.get("/usage")
def get_usage() -> dict:
    """Return usage records collected since the app started."""
    return {
        "request_count": len(usage_log),
        "total_prompt_tokens": sum(item["prompt_tokens"] for item in usage_log),
        "total_completion_tokens": sum(item["completion_tokens"] for item in usage_log),
        "total_tokens": sum(item["total_tokens"] for item in usage_log),
        "requests": usage_log,
    }
@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    settings: SettingsDep,
) -> ChatResponse:
    """Send a question to Groq and return a structured answer."""
    if not settings.groq_api_key:
        raise HTTPException(
            status_code=503,
            detail="Groq API key is not configured.",
        )

    try:
        client = Groq(
            api_key=settings.groq_api_key,
            timeout=10.0,
            max_retries=2,
            )
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer the user's question clearly and accurately. "
                        f"Respond in {request.language}. "
                        "If you are unsure, say so."
                    ),
                },
                {"role": "user", "content": request.message},
            ],
        )

        answer = completion.choices[0].message.content or ""
        usage_log.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "model": settings.groq_model,
                "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                "total_tokens": completion.usage.total_tokens if completion.usage else 0,
            }
        )
        return ChatResponse(
            answer=answer,
            language=request.language,
            status="success",
        )

    except Exception as exc:
        print(f"Groq request failed: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete the request. Check the terminal for details.",
        ) from exc
        