def test_unregister_success_removes_participant(client):
    email = "daniel@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "not-signed@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_without_email_returns_422(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
