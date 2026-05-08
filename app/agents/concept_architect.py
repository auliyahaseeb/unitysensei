import os
from typing import Any, Literal

from app.core.safety import ensure_safe_game_idea
from app.core.unity_guide import default_player_setup_steps
from app.models.game_design import (
    AssetRequirement,
    GameDesignDocument,
    PlayerMechanics,
    WinLossConditions,
)

try:
    from pydantic_ai import Agent
except ImportError:  # pragma: no cover - keeps deterministic mode usable before dependencies are installed.
    Agent = None  # type: ignore[assignment]


CONCEPT_ARCHITECT_PROMPT = """
You are the Concept Architect for UnitySensei, an educational Unity 3D tutor for children ages 8-14.
Translate kid-speak into a safe, structured Game Design Document.

Rules:
- Keep the idea age-appropriate, non-violent, and encouraging.
- Prefer simple 3D Unity mechanics: movement, jumping, collecting, timers, checkpoints, and puzzles.
- Define player mechanics, win/loss conditions, and asset requirements.
- Include Unity Editor steps that mention Hierarchy, Inspector, Tags & Layers, and Console when useful.
- Use language a child can understand, but return only the structured output requested by the schema.
"""

_LLM_TRUE_VALUES = {"1", "true", "yes", "on"}
_MODEL_NAME = os.getenv("UNITYSENSEI_MODEL", "openai:gpt-5.2")

concept_architect_agent: Any | None = None
if Agent is not None:
    concept_architect_agent = Agent(
        _MODEL_NAME,
        output_type=GameDesignDocument,
        instructions=CONCEPT_ARCHITECT_PROMPT,
    )


def llm_enabled() -> bool:
    return os.getenv("UNITYSENSEI_USE_LLM", "false").lower() in _LLM_TRUE_VALUES


async def build_game_design(idea: str) -> tuple[GameDesignDocument, Literal["llm", "fallback"]]:
    ensure_safe_game_idea(idea)

    if llm_enabled() and concept_architect_agent is not None:
        try:
            result = await concept_architect_agent.run(
                f"Child idea: {idea}\nCreate the UnitySensei Game Design Document."
            )
            return result.output, "llm"
        except Exception as exc:
            fallback = create_fallback_game_design(idea)
            fallback.safe_mode_notes.append(
                f"LLM generation was unavailable, so UnitySensei used a deterministic starter plan ({exc.__class__.__name__})."
            )
            return fallback, "fallback"

    return create_fallback_game_design(idea), "fallback"


def create_fallback_game_design(idea: str) -> GameDesignDocument:
    lowered = idea.lower()
    genre: Literal[
        "platformer",
        "collecting",
        "maze",
        "racing",
        "puzzle",
        "adventure",
        "simulation",
        "other",
    ] = "platformer"
    title = "Jump Quest"
    main_collectible = "star"
    hazard = "wobbly platform"

    if "lava" in lowered:
        title = "Lava Leap"
        hazard = "lava floor"
    elif "space" in lowered or "rocket" in lowered:
        title = "Space Hopper"
        main_collectible = "moon gem"
    elif "race" in lowered or "car" in lowered:
        title = "Checkpoint Dash"
        genre = "racing"
        main_collectible = "checkpoint ring"
    elif "maze" in lowered:
        title = "Maze Explorer"
        genre = "maze"
        main_collectible = "key"
    elif "puzzle" in lowered:
        title = "Puzzle Path"
        genre = "puzzle"
        main_collectible = "logic cube"

    return GameDesignDocument(
        title=title,
        child_idea=idea,
        summary=(
            f"A beginner Unity 3D {genre} where the player moves, jumps, avoids the {hazard}, "
            f"and collects a {main_collectible} to reach the goal."
        ),
        genre=genre,
        player_mechanics=PlayerMechanics(
            movement="Use WASD or arrow keys to move a 3D player around the scene.",
            jump_or_action="Press Space to jump over beginner-friendly obstacles.",
            camera_style="Start with a fixed third-person camera looking down at the play area.",
            controls=["WASD / Arrow Keys: move", "Space: jump", "R: restart later as a stretch goal"],
        ),
        win_loss_conditions=WinLossConditions(
            win_conditions=[
                f"Collect the {main_collectible}.",
                "Reach the bright goal platform at the end of the course.",
            ],
            loss_conditions=[
                f"Touch the {hazard} and return to the start.",
                "Fall below the play area.",
            ],
            restart_rule="Move the Player back to the starting platform and reset any collected items.",
        ),
        asset_requirements=[
            AssetRequirement(
                name="Player capsule",
                asset_type="3d_model",
                purpose="The controllable character for the first prototype.",
                beginner_friendly_source="Unity built-in 3D Object > Capsule.",
            ),
            AssetRequirement(
                name="Ground and platforms",
                asset_type="3d_model",
                purpose="Safe places for the player to stand and jump between.",
                beginner_friendly_source="Unity built-in 3D Object > Cube.",
            ),
            AssetRequirement(
                name=hazard.title(),
                asset_type="material",
                purpose="A clear obstacle that teaches collision and restart logic.",
                beginner_friendly_source="Create a bright material in the Unity Project window.",
            ),
            AssetRequirement(
                name=main_collectible.title(),
                asset_type="prefab",
                purpose="A simple object the player can collect to win.",
                beginner_friendly_source="Unity built-in Sphere with a glowing material.",
            ),
            AssetRequirement(
                name="PlayerController.cs",
                asset_type="script",
                purpose="Moves the player and prints a Hello World message in the Console.",
                beginner_friendly_source="Generated by UnitySensei.",
            ),
        ],
        unity_setup_steps=default_player_setup_steps(),
        learning_goals=[
            "Understand how a script attaches to a GameObject.",
            "Tune public float variables in the Inspector.",
            "Use keyboard input to move and jump.",
            "Read Unity Console messages as helpful clues.",
        ],
        safe_mode_notes=[
            "The prototype uses obstacle-course danger instead of realistic harm.",
            "The first version keeps the scope small so a young learner can finish it.",
        ],
    )
