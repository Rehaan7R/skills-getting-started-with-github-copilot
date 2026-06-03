"""Tests for the /activities endpoint"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        ARRANGE: Create a test client
        ACT: Make a GET request to /activities
        ASSERT: Verify response status and that all activities are returned
        """
        # ARRANGE
        # (client fixture already provides the test client)

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert "Soccer Team" in activities
        assert "Basketball Club" in activities
        assert "Art Club" in activities
        assert "Drama Society" in activities
        assert "Debate Team" in activities
        assert "Science Club" in activities

    def test_get_activities_response_structure(self, client):
        """
        ARRANGE: Create a test client
        ACT: Make a GET request to /activities
        ASSERT: Verify each activity has required fields
        """
        # ARRANGE
        # (client fixture already provides the test client)

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_contains_initial_participants(self, client):
        """
        ARRANGE: Create a test client
        ACT: Make a GET request to /activities
        ASSERT: Verify activities have initial participants
        """
        # ARRANGE
        # (client fixture already provides the test client)

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
