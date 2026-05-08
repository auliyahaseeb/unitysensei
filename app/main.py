from fastapi import FastAPI, HTTPException

from app.agents.concept_architect import build_game_design
from app.core.error_interpreter import interpret_unity_error
from app.core.safety import UnsafeGameIdeaError, check_game_idea
from app.core.scaffold import generate_space_jump_fill_in_blank
from app.core.scripts import create_hello_world_player_controller
from app.models.game_design import (
    ErrorInterpreterRequest,
    FillInBlankExercise,
    FillInBlankRequest,
    FriendlyErrorExplanation,
    StarterKitRequest,
    StarterKitResponse,
)

app = FastAPI(
    title="UnitySensei API",
    version="0.1.0",
    description="Multi-agent educational backend for turning children's Unity ideas into guided starter kits.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "UnitySensei"}


@app.post("/generate-starter-kit", response_model=StarterKitResponse)
async def generate_starter_kit(request: StarterKitRequest) -> StarterKitResponse:
    safety = check_game_idea(request.idea)
    if not safety.allowed:
        raise HTTPException(status_code=400, detail=safety.model_dump())

    try:
        game_plan, generation_mode = await build_game_design(request.idea)
    except UnsafeGameIdeaError as exc:
        raise HTTPException(status_code=400, detail=exc.decision.model_dump()) from exc

    return StarterKitResponse(
        input_idea=request.idea,
        generation_mode=generation_mode,
        safety=safety,
        game_plan=game_plan,
        player_controller_script=create_hello_world_player_controller(game_plan.title),
        scaffolded_challenge=generate_space_jump_fill_in_blank(),
    )


@app.post("/interpret-error", response_model=FriendlyErrorExplanation)
async def interpret_error(request: ErrorInterpreterRequest) -> FriendlyErrorExplanation:
    return interpret_unity_error(request.raw_error)


@app.post("/fill-in-the-blank", response_model=FillInBlankExercise)
async def fill_in_the_blank(request: FillInBlankRequest) -> FillInBlankExercise:
    if request.mechanic == "space_jump":
        return generate_space_jump_fill_in_blank()

    raise HTTPException(status_code=404, detail="That scaffolded exercise is not available yet.")

