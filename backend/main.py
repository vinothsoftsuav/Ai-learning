from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


def create_app() -> FastAPI:
    load_dotenv()

    app = FastAPI(title="OpenRouter Chat API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Missing OpenRouter API key")

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.message},
            ],
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(base_url="https://openrouter.ai/api/v1") as client:
            try:
                response = await client.post("/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
            except httpx.HTTPError as exc:
                raise HTTPException(status_code=502, detail=str(exc)) from exc

        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            raise HTTPException(status_code=502, detail="Invalid response from OpenRouter")

        return ChatResponse(reply=content.strip())

    return app


app = create_app()


