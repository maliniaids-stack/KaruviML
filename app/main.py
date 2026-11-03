from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from groq import Groq, APIConnectionError, APITimeoutError, RateLimitError, APIStatusError

from app.config import Settings, get_settings
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
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
        