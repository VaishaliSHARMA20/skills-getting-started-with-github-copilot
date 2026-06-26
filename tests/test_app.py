from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    # Arrange
    email = "test_student@example.com"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    email = "duplicate_student@example.com"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    duplicate_response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant():
    # Arrange
    email = "removable_student@example.com"
    activity = "Programming Class"
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    delete_response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert "Removed" in delete_response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
