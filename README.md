# UnitySensei

UnitySensei is a FastAPI backend for a multi-agent educational system that helps children ages 8-14 turn Unity 3D game ideas into structured plans, friendly editor guidance, and beginner C# scripts.

## Current Scaffold

- `Concept Architect`: Pydantic AI agent definition that converts kid-speak into a typed `GameDesignDocument`.
- Safe-mode filter for age-appropriate game mechanics.
- Starter-kit endpoint that returns a game plan, Unity setup steps, a commented player-controller script, and a fill-in-the-blank jump challenge.
- Friendly Unity console error interpreter.

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## LLM Configuration

The API works without LLM credentials by using a deterministic educational fallback. To enable the Pydantic AI Concept Architect:

```powershell
$env:UNITYSENSEI_USE_LLM = "true"
$env:UNITYSENSEI_MODEL = "openai:gpt-5.2"
$env:OPENAI_API_KEY = "..."
```

## Example Request

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/generate-starter-kit `
  -ContentType "application/json" `
  -Body '{"idea":"I want a lava jump game where I collect glowing gems"}'
```

