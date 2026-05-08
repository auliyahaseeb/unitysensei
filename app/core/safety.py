import re

from app.models.game_design import SafetyDecision


class UnsafeGameIdeaError(ValueError):
    def __init__(self, decision: SafetyDecision) -> None:
        super().__init__(decision.reason)
        self.decision = decision


_BLOCKED_PATTERNS: dict[str, str] = {
    r"\bblood\b|\bgore\b|\bviolence\b|\bdismember\b|\bdecapitat": "graphic violence",
    r"\bkill\b|\bkiller\b|\bmurder\b|\bassassin\b|\bexecute\b": "realistic harm",
    r"\bguns?\b|\brifles?\b|\bpistols?\b|\bshoot\b": "weapons",
    r"\bsuicide\b|\bself[- ]?harm\b": "self-harm",
    r"\bdrug\b|\bcocaine\b|\bheroin\b|\bvape\b": "drugs",
    r"\bsex\b|\bnude\b|\bporn\b": "sexual content",
    r"\bhate\b|\bracist\b|\bslur\b": "hateful content",
}


def check_game_idea(idea: str) -> SafetyDecision:
    """Reject mechanics that are not appropriate for children ages 8-14."""
    lowered = idea.lower()
    flagged: list[str] = []

    for pattern, label in _BLOCKED_PATTERNS.items():
        if re.search(pattern, lowered):
            flagged.append(label)

    if flagged:
        return SafetyDecision(
            allowed=False,
            reason="That idea needs a safer twist before we build it for young learners.",
            flagged_terms=sorted(set(flagged)),
            suggested_revision=(
                "Try changing danger into obstacle-course play, rescue missions, silly traps, "
                "collecting, racing, puzzles, or cartoon hazards like lava floors."
            ),
        )

    return SafetyDecision(
        allowed=True,
        reason="This idea is safe to turn into a beginner Unity project.",
    )


def ensure_safe_game_idea(idea: str) -> SafetyDecision:
    decision = check_game_idea(idea)
    if not decision.allowed:
        raise UnsafeGameIdeaError(decision)
    return decision
