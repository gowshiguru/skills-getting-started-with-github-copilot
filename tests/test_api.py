from fastapi.testclient import TestClient
from src.app import app, activities
from urllib.parse import quote

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Basketball Team" in data
    assert "Chess Club" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_and_remove_participant():
    activity = "Basketball Team"
    email = "tester@example.com"

    # Make sure test email is not present to start
    activities[activity]["participants"] = [p for p in activities[activity]["participants"] if p != email]

    # Sign up
    resp = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    assert resp2.status_code == 400

    # Remove participant
    resp3 = client.delete(f"/activities/{quote(activity)}/participants?email={email}")
    assert resp3.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    resp = client.delete("/activities/Chess%20Club/participants?email=notexists@example.com")
    assert resp.status_code == 404
