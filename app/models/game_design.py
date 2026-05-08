from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SafetyDecision(BaseModel):
    allowed: bool = Field(description="Whether the game idea is appropriate for children ages 8-14.")
    reason: str = Field(description="A child-friendly explanation of the safety decision.")
    flagged_terms: list[str] = Field(default_factory=list)
    suggested_revision: str | None = Field(default=None)


class PlayerMechanics(BaseModel):
    movement: str = Field(description="How the player moves in the game.")
    jump_or_action: str = Field(description="The main button action, such as jumping or collecting.")
    camera_style: str = Field(description="Beginner-friendly camera recommendation.")
    controls: list[str] = Field(default_factory=list, description="Simple controls the child can test.")


class WinLossConditions(BaseModel):
    win_conditions: list[str] = Field(default_factory=list)
    loss_conditions: list[str] = Field(default_factory=list)
    restart_rule: str = Field(description="How the player can try again after losing.")


class AssetRequirement(BaseModel):
    name: str
    asset_type: Literal["3d_model", "material", "sound", "ui", "script", "scene", "prefab", "animation"]
    purpose: str
    beginner_friendly_source: str = Field(description="Where a young learner can make or find this asset safely.")


class UnityEditorStep(BaseModel):
    step_number: int = Field(ge=1)
    unity_area: Literal["Hierarchy", "Inspector", "Project", "Scene", "Tags & Layers", "Console"]
    action: str
    why_it_matters: str


class GameDesignDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    child_idea: str
    summary: str
    target_age_range: str = Field(default="8-14")
    genre: Literal["platformer", "collecting", "maze", "racing", "puzzle", "adventure", "simulation", "other"]
    player_mechanics: PlayerMechanics
    win_loss_conditions: WinLossConditions
    asset_requirements: list[AssetRequirement]
    unity_setup_steps: list[UnityEditorStep]
    learning_goals: list[str]
    safe_mode_notes: list[str] = Field(default_factory=list)


class CodeSnippet(BaseModel):
    filename: str
    language: Literal["csharp", "python"]
    purpose: str
    code: str
    educational_notes: list[str] = Field(default_factory=list)


class FillInBlankExercise(BaseModel):
    title: str
    prompt: str
    filename: str
    code_with_blanks: str
    answer_key: str
    hints: list[str] = Field(default_factory=list)


class FriendlyErrorExplanation(BaseModel):
    raw_error: str
    simple_title: str
    kid_friendly_explanation: str
    metaphor: str
    likely_cause: str
    fix_steps: list[str]
    unity_area_to_check: Literal["Hierarchy", "Inspector", "Project", "Scene", "Tags & Layers", "Console"]


class StarterKitRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=500, description="The child's plain-language game idea.")

    @field_validator("idea")
    @classmethod
    def strip_idea(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            raise ValueError("Please describe the game idea.")
        return cleaned


class StarterKitResponse(BaseModel):
    input_idea: str
    generation_mode: Literal["llm", "fallback"]
    safety: SafetyDecision
    game_plan: GameDesignDocument
    player_controller_script: CodeSnippet
    scaffolded_challenge: FillInBlankExercise


class ErrorInterpreterRequest(BaseModel):
    raw_error: str = Field(min_length=3, max_length=2000)


class FillInBlankRequest(BaseModel):
    mechanic: Literal["space_jump"] = Field(default="space_jump")

