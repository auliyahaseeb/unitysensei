from app.models.game_design import FriendlyErrorExplanation


def interpret_unity_error(raw_error: str) -> FriendlyErrorExplanation:
    lowered = raw_error.lower()

    if "nullreferenceexception" in lowered:
        return FriendlyErrorExplanation(
            raw_error=raw_error,
            simple_title="Something is not plugged in",
            kid_friendly_explanation=(
                "Your code tried to use an object or component, but Unity could not find it yet."
            ),
            metaphor="It is like trying to turn on a lamp before plugging it into the wall.",
            likely_cause="A script variable, Rigidbody, Camera, or other component is missing.",
            fix_steps=[
                "Click the object that has the script.",
                "Look in the Inspector for empty script slots.",
                "Make sure the object has the component your code asks for.",
            ],
            unity_area_to_check="Inspector",
        )

    if "cs1002" in lowered or "; expected" in lowered:
        return FriendlyErrorExplanation(
            raw_error=raw_error,
            simple_title="A semicolon is missing",
            kid_friendly_explanation="C# needs many instructions to end with a semicolon.",
            metaphor="A semicolon is like the period at the end of a sentence.",
            likely_cause="One line of code probably forgot its ending semicolon.",
            fix_steps=[
                "Double-click the Console error to jump to the line.",
                "Look at that line and the line above it.",
                "Add a semicolon after the finished instruction.",
            ],
            unity_area_to_check="Console",
        )

    if "cs0246" in lowered or "type or namespace" in lowered:
        return FriendlyErrorExplanation(
            raw_error=raw_error,
            simple_title="Unity does not know that name",
            kid_friendly_explanation="The script used a class or type name Unity cannot recognize.",
            metaphor="It is like asking for a teammate by a nickname nobody has heard before.",
            likely_cause="There may be a typo, missing using statement, or mismatched script/class name.",
            fix_steps=[
                "Check spelling and capital letters.",
                "Make sure the file name and class name match for MonoBehaviour scripts.",
                "Look for missing using UnityEngine; at the top of the file.",
            ],
            unity_area_to_check="Project",
        )

    if "unassignedreferenceexception" in lowered:
        return FriendlyErrorExplanation(
            raw_error=raw_error,
            simple_title="An Inspector slot is empty",
            kid_friendly_explanation="Unity expected you to drag an object into a script field.",
            metaphor="It is like a recipe saying add the sauce, but the sauce bowl is empty.",
            likely_cause="A public or serialized field was not assigned in the Inspector.",
            fix_steps=[
                "Select the GameObject with the script.",
                "Find the empty field in the Inspector.",
                "Drag the correct object from the Hierarchy or Project window into the slot.",
            ],
            unity_area_to_check="Inspector",
        )

    return FriendlyErrorExplanation(
        raw_error=raw_error,
        simple_title="Unity found a clue",
        kid_friendly_explanation="The Console message is pointing at the next thing to check.",
        metaphor="It is like a treasure map: start at the first X, then follow the line number.",
        likely_cause="The issue may be a typo, missing component, missing tag, or script setup problem.",
        fix_steps=[
            "Read the first line of the error.",
            "Double-click it in the Console to open the script.",
            "Check the named object, component, tag, or line number.",
        ],
        unity_area_to_check="Console",
    )

