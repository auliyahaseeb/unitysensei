from app.models.game_design import CodeSnippet


def _csharp_string_literal(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def create_hello_world_player_controller(game_title: str) -> CodeSnippet:
    title_literal = _csharp_string_literal(game_title)
    code = f'''using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class PlayerController : MonoBehaviour
{{
    // A float stores decimal numbers, so speed can be 4.5 instead of only 4 or 5.
    // That helps movement feel smooth while a learner experiments in the Inspector.
    public float speed = 5f;

    // Another float is useful here because jump strength may need tiny adjustments.
    public float jumpForce = 7f;

    // A bool is a true/false switch. It helps us avoid double-jumping for now.
    private bool isGrounded = true;

    private Rigidbody rb;

    void Start()
    {{
        rb = GetComponent<Rigidbody>();
        Debug.Log("Hello from UnitySensei! " + {title_literal} + " is ready to move.");
    }}

    void Update()
    {{
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(horizontal, 0f, vertical);
        transform.Translate(movement * speed * Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {{
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            isGrounded = false;
        }}
    }}

    void OnCollisionEnter(Collision collision)
    {{
        isGrounded = true;
    }}

    public string DebugLogic(string unityError)
    {{
        if (string.IsNullOrEmpty(unityError))
        {{
            return "There is no error text yet. Press Play, then copy the first Console message if one appears.";
        }}

        string lowerError = unityError.ToLower();

        if (lowerError.Contains("nullreferenceexception"))
        {{
            return "NullReferenceException is like pressing a button that is not plugged in yet. Check that the object or component exists in the Inspector.";
        }}

        if (lowerError.Contains("cs1002"))
        {{
            return "CS1002 usually means a semicolon is missing. A semicolon is like a period at the end of a C# instruction.";
        }}

        if (lowerError.Contains("unassignedreferenceexception"))
        {{
            return "UnassignedReferenceException means Unity sees an empty slot in the Inspector. Drag the missing object into that slot.";
        }}

        return "Unity found a clue. Read the first line, then check the script name, Inspector slots, and missing punctuation.";
    }}
}}
'''

    return CodeSnippet(
        filename="PlayerController.cs",
        language="csharp",
        purpose="A beginner Hello World movement controller for a Unity 3D player object.",
        code=code,
        educational_notes=[
            "The public float variables appear in the Unity Inspector so learners can tune them safely.",
            "Input.GetAxis keeps movement beginner-friendly with Unity's built-in Horizontal and Vertical controls.",
            "DebugLogic models how the Scripting Mentor will translate errors into simple explanations.",
        ],
    )
