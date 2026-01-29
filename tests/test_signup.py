import pytest


def test_signup_new_participant(client, reset_activities):
    """Test signing up a new participant"""
    response = client.post(
        "/activities/Basketball/signup?email=newstudent@mergington.edu",
        json={}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball" in data["message"]


def test_signup_adds_participant(client, reset_activities):
    """Test that signup actually adds participant to the activity"""
    # Verify initial state
    response = client.get("/activities")
    initial_count = len(response.json()["Basketball"]["participants"])
    
    # Sign up new participant
    client.post(
        "/activities/Basketball/signup?email=newstudent@mergington.edu",
        json={}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()["Basketball"]["participants"])
    assert new_count == initial_count + 1
    assert "newstudent@mergington.edu" in response.json()["Basketball"]["participants"]


def test_signup_duplicate_participant(client, reset_activities):
    """Test that duplicate signup is rejected"""
    response = client.post(
        "/activities/Basketball/signup?email=alex@mergington.edu",
        json={}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity(client, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/NonExistentActivity/signup?email=test@mergington.edu",
        json={}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_signup_multiple_activities(client, reset_activities):
    """Test that a participant can sign up for multiple activities"""
    email = "multistudent@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        f"/activities/Basketball/signup?email={email}",
        json={}
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/Tennis Club/signup?email={email}",
        json={}
    )
    assert response2.status_code == 200
    
    # Verify both signups
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Basketball"]["participants"]
    assert email in activities["Tennis Club"]["participants"]
