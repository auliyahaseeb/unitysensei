from app.models.game_design import FillInBlankExercise


def generate_space_jump_fill_in_blank() -> FillInBlankExercise:
    code = '''using UnityEngine;

public class JumpChallenge : MonoBehaviour
{
    public float jumpForce = 7f;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        // Fill in the blank so the player jumps when Space is pressed.
        if (____________________________)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }
}
'''

    return FillInBlankExercise(
        title="Space Bar Jump Check",
        prompt="Complete the if statement so Unity listens for the Space key once per press.",
        filename="JumpChallenge.cs",
        code_with_blanks=code,
        answer_key="Input.GetKeyDown(KeyCode.Space)",
        hints=[
            "The answer starts with Input because Unity is checking the keyboard.",
            "Use GetKeyDown when you want one jump per button press.",
            "KeyCode.Space is Unity's name for the Space bar.",
        ],
    )

