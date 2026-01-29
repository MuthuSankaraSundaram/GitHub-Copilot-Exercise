import pytest


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant"""
    response = client.post(
        "/activities/Basketball/unregister?email=alex@mergington.edu",
        json={}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "alex@mergington.edu" in data["message"]
    assert "Basketball" in data["message"]


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregister actually removes participant"""
    # Verify initial state
    response = client.get("/activities")
    initial_count = len(response.json()["Basketball"]["participants"])
    assert "alex@mergington.edu" in response.json()["Basketball"]["participants"]
    
    # Unregister participant
    client.post(
        "/activities/Basketball/unregister?email=alex@mergington.edu",
        json={}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    new_count = len(response.json()["Basketball"]["participants"])
    assert new_count == initial_count - 1
    assert "alex@mergington.edu" not in response.json()["Basketball"]["participants"]


def test_unregister_nonexistent_participant(client, reset_activities):
    """Test unregistering a participant who is not registered"""
    response = client.post(
        "/activities/Basketball/unregister?email=notregistered@mergington.edu",
        json={}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"]


def test_unregister_invalid_activity(client, reset_activities):
    """Test unregister from non-existent activity"""
    response = client.post(
        "/activities/NonExistentActivity/unregister?email=test@mergington.edu",
        json={}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_unregister_and_rejoin(client, reset_activities):
    """Test that a participant can unregister and then rejoin"""
    email = "rejointest@mergington.edu"
    
    # Sign up
    client.post(
        f"/activities/Basketball/signup?email={email}",
        json={}
    )
    
    response = client.get("/activities")
    assert email in response.json()["Basketball"]["participants"]
    
    # Unregister
    client.post(
        f"/activities/Basketball/unregister?email={email}",
        json={}
    )
    
    response = client.get("/activities")
    assert email not in response.json()["Basketball"]["participants"]
    
    # Rejoin
    response = client.post(
        f"/activities/Basketball/signup?email={email}",
        json={}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    assert email in response.json()["Basketball"]["participants"]
