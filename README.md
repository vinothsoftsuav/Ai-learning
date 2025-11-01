# OpenRouter Chatbot

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- An [OpenRouter](https://openrouter.ai/) API key

## Backend Setup (`backend/`)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
copy env.example .env       # or rename manually and add your API key

uvicorn main:app --reload
```

`main.py` exposes a single `POST /chat` endpoint. It expects a JSON payload such as:

```json
{ "message": "Hello, who are you?" }
```

The server loads `OPENROUTER_API_KEY` from the environment, calls OpenRouter's `/chat/completions` endpoint, and returns a JSON response:

```json
{ "reply": "I am an AI assistant..." }
```

## Frontend Setup (`frontend/`)

```bash
cd frontend
npm install
npm run dev
```

During development, Vite proxies requests from `/api` to `http://127.0.0.1:8000` (see `vite.config.ts`). With both the FastAPI server and Vite dev server running, open the printed local URL (typically `http://localhost:5173`).

## Production Notes

- Update the proxy target in `vite.config.ts` or use environment variables when deploying.
- Serve the React build (`npm run build`) from any static host and point it to your FastAPI deployment.
- FastAPI is currently configured with `allow_origins=['*']` for simplicity. Tighten this before deploying to production.

## Deploying / Publishing

Once you have confirmed everything works locally:

```bash
git add .
git commit -m "Add OpenRouter chatbot app"
git remote add origin <your-repo-url>  # if not already set
git push origin main
```

Happy building! ✨


