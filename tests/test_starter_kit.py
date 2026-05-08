from fastapi.testclient import TestClient

from app.core.scripts import create_hello_world_player_controller
from app.main import app


client = TestClient(app)


def test_generate_starter_kit_returns_plan_and_script() -> None:
    response = client.post("/generate-starter-kit", json={"idea": "I want a lava jump game"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["game_plan"]["title"] == "Lava Leap"
    assert payload["player_controller_script"]["filename"] == "PlayerController.cs"
    assert "public float speed" in payload["player_controller_script"]["code"]
    assert payload["scaffolded_challenge"]["answer_key"] == "Input.GetKeyDown(KeyCode.Space)"


def test_safe_mode_rejects_inappropriate_mechanics() -> None:
    response = client.post("/generate-starter-kit", json={"idea": "make a gun shooting game"})

    assert response.status_code == 400
    assert response.json()["detail"]["allowed"] is False


def test_error_interpreter_explains_semicolon_errors() -> None:
    response = client.post("/interpret-error", json={"raw_error": "error CS1002: ; expected"})

    assert response.status_code == 200
    assert response.json()["simple_title"] == "A semicolon is missing"


def test_player_controller_escapes_game_title_for_csharp() -> None:
    snippet = create_hello_world_player_controller('Quest "Beta" \\ Zone')

    assert 'Debug.Log("Hello from UnitySensei! " + "Quest \\"Beta\\" \\\\ Zone" + " is ready to move.");' in snippet.code
