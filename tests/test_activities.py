import pytest


def test_get_activities(client, reset_activities):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "Tennis Club" in data
    assert "Debate Team" in data


def test_get_activities_structure(client, reset_activities):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Basketball"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    assert isinstance(activity["participants"], list)
    assert "alex@mergington.edu" in activity["participants"]


def test_get_activities_count(client, reset_activities):
    """Test that all activities are returned"""
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = 9  # Basketball, Tennis Club, Debate Team, Math Club, Drama Club, Art Studio, Chess Club, Programming Class, Gym Class
    assert len(data) == expected_activities


def test_root_redirects(client):
    """Test that root path redirects to static page"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
