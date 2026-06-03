"""Tests for the /activities/{activity_name}/signup and /unregister endpoints"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_for_activity_success(self, client):
        """
        ARRANGE: Prepare a new student email and activity name
        ACT: Make a POST request to sign up for an activity
        ASSERT: Verify the signup succeeds and response is correct
        """
        # ARRANGE
        email = "new_student@example.com"
        activity_name = "Chess Club"

        # ACT
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_for_activity_adds_participant(self, client):
        """
        ARRANGE: Prepare a new student email
        ACT: Sign up for an activity, then fetch activities list
        ASSERT: Verify the participant was added to the activity
        """
        # ARRANGE
        email = "student_xyz@example.com"
        activity_name = "Programming Class"

        # ACT
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")

        # ASSERT
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """
        ARRANGE: Prepare email and a nonexistent activity name
        ACT: Make a POST request to sign up for an activity that doesn't exist
        ASSERT: Verify 404 error is returned
        """
        # ARRANGE
        email = "student@example.com"
        activity_name = "Nonexistent Club"

        # ACT
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_for_activity_without_email_param_returns_error(self, client):
        """
        ARRANGE: Prepare only activity name (no email)
        ACT: Make a POST request without email parameter
        ASSERT: Verify error is returned (422 Unprocessable Entity)
        """
        # ARRANGE
        activity_name = "Chess Club"

        # ACT
        response = client.post(f"/activities/{activity_name}/signup")

        # ASSERT
        assert response.status_code == 422

    def test_signup_duplicate_returns_400(self, client):
        """
        ARRANGE: Prepare an email that's already signed up for an activity
        ACT: Make a POST request to sign up with an already-registered email
        ASSERT: Verify 400 error is returned
        """
        # ARRANGE
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # ACT
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_can_register_multiple_activities(self, client):
        """
        ARRANGE: Prepare a new student email
        ACT: Sign up the same student for two different activities
        ASSERT: Verify both signups succeed
        """
        # ARRANGE
        email = "multi_activity_student@example.com"
        activity1 = "Chess Club"
        activity2 = "Debate Team"

        # ACT
        response1 = client.post(f"/activities/{activity1}/signup", params={"email": email})
        response2 = client.post(f"/activities/{activity2}/signup", params={"email": email})

        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_from_activity_success(self, client):
        """
        ARRANGE: Sign up a student, then prepare to unregister
        ACT: Make a DELETE request to unregister from an activity
        ASSERT: Verify the unregister succeeds
        """
        # ARRANGE
        email = "temp_student@example.com"
        activity_name = "Programming Class"
        # First sign up
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ACT
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant(self, client):
        """
        ARRANGE: Sign up a student, then unregister
        ACT: Fetch activities list after unregister
        ASSERT: Verify the participant was removed
        """
        # ARRANGE
        email = "remove_me@example.com"
        activity_name = "Soccer Team"
        # First sign up
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # ACT
        client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
        response = client.get("/activities")

        # ASSERT
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """
        ARRANGE: Prepare email and a nonexistent activity name
        ACT: Make a DELETE request to unregister from a nonexistent activity
        ASSERT: Verify 404 error is returned
        """
        # ARRANGE
        email = "student@example.com"
        activity_name = "Nonexistent Club"

        # ACT
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered_returns_400(self, client):
        """
        ARRANGE: Prepare email for a student not registered in the activity
        ACT: Make a DELETE request to unregister a non-registered student
        ASSERT: Verify 400 error is returned
        """
        # ARRANGE
        email = "not_registered@example.com"
        activity_name = "Chess Club"

        # ACT
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_without_email_param_returns_error(self, client):
        """
        ARRANGE: Prepare only activity name (no email)
        ACT: Make a DELETE request without email parameter
        ASSERT: Verify error is returned (422 Unprocessable Entity)
        """
        # ARRANGE
        activity_name = "Chess Club"

        # ACT
        response = client.delete(f"/activities/{activity_name}/unregister")

        # ASSERT
        assert response.status_code == 422

    def test_can_signup_again_after_unregister(self, client):
        """
        ARRANGE: Sign up, unregister, then sign up again
        ACT: Verify all operations succeed
        ASSERT: Student is registered for the activity again
        """
        # ARRANGE
        email = "rejoin_student@example.com"
        activity_name = "Art Club"

        # ACT & ASSERT - First signup
        response1 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response1.status_code == 200

        # ACT & ASSERT - Unregister
        response2 = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
        assert response2.status_code == 200

        # ACT & ASSERT - Sign up again
        response3 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response3.status_code == 200

        # Verify student is registered again
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
