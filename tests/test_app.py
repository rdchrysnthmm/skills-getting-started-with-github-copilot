from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Activities should match in-memory database keys
    assert isinstance(data, dict)
    for name in activities.keys():
        assert name in data


def test_signup_and_unregister():
    # pick an activity
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # ensure participant is not already there
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # unregister
    r2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r2.status_code == 200
    assert email not in activities[activity]["participants"]


def test_signup_unknown_activity():
    r = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert r.status_code == 404


def test_unregister_unknown_participant():
    activity = "Chess Club"
    r = client.delete(f"/activities/{activity}/participants?email=notthere@none.com")
    assert r.status_code == 404
