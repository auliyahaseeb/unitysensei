from app.models.game_design import UnityEditorStep


def default_player_setup_steps() -> list[UnityEditorStep]:
    return [
        UnityEditorStep(
            step_number=1,
            unity_area="Hierarchy",
            action="Create a Capsule and rename it Player.",
            why_it_matters="The script needs one clear object to control.",
        ),
        UnityEditorStep(
            step_number=2,
            unity_area="Inspector",
            action="With Player selected, choose Add Component, then add Rigidbody.",
            why_it_matters="Rigidbody lets Unity physics handle jumping and falling.",
        ),
        UnityEditorStep(
            step_number=3,
            unity_area="Inspector",
            action="Add the PlayerController script to the Player object.",
            why_it_matters="This connects the C# code to the object in the scene.",
        ),
        UnityEditorStep(
            step_number=4,
            unity_area="Tags & Layers",
            action="Create a Player tag and assign it to the Player object.",
            why_it_matters="Tags help future scripts find important objects by role.",
        ),
        UnityEditorStep(
            step_number=5,
            unity_area="Hierarchy",
            action="Create a Cube, scale it wide, and rename it Ground.",
            why_it_matters="A floor gives the player a safe place to test movement.",
        ),
        UnityEditorStep(
            step_number=6,
            unity_area="Console",
            action="Press Play and check the Console for helpful messages.",
            why_it_matters="The Console is where Unity tells you what the code is thinking.",
        ),
    ]

