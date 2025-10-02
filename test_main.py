from fastapi.testclient import TestClient
from main import app
import pytest
import json

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Course Management API"}

class TestUsers:
    def test_create_user(self):
        response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["is_active"] == True
        assert "id" in data
        return data["id"]

    def test_get_all_users(self):
        client.post("/users/", json={"name": "Jane Doe", "email": "jane@example.com"})
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_user(self):
        create_response = client.post("/users/", json={"name": "Test User", "email": "test@example.com"})
        user_id = create_response.json()["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"

    def test_get_nonexistent_user(self):
        response = client.get("/users/nonexistent")
        assert response.status_code == 404

    def test_update_user(self):
        create_response = client.post("/users/", json={"name": "Update Test", "email": "update@example.com"})
        user_id = create_response.json()["id"]

        response = client.put(f"/users/{user_id}", json={"name": "Updated Name"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "update@example.com"

    def test_deactivate_user(self):
        create_response = client.post("/users/", json={"name": "Deactivate Test", "email": "deactivate@example.com"})
        user_id = create_response.json()["id"]

        response = client.patch(f"/users/{user_id}/deactivate")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] == False

    def test_delete_user(self):
        create_response = client.post("/users/", json={"name": "Delete Test", "email": "delete@example.com"})
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

class TestCourses:
    def test_create_course(self):
        response = client.post("/courses/", json={
            "title": "Python Basics",
            "description": "Learn Python programming fundamentals"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Python Basics"
        assert data["description"] == "Learn Python programming fundamentals"
        assert data["is_open"] == True
        assert "id" in data

    def test_get_all_courses(self):
        client.post("/courses/", json={"title": "Test Course", "description": "Test Description"})
        response = client.get("/courses/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_course(self):
        create_response = client.post("/courses/", json={
            "title": "Test Course",
            "description": "Test Description"
        })
        course_id = create_response.json()["id"]

        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Course"

    def test_update_course(self):
        create_response = client.post("/courses/", json={
            "title": "Original Title",
            "description": "Original Description"
        })
        course_id = create_response.json()["id"]

        response = client.put(f"/courses/{course_id}", json={"title": "Updated Title"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Original Description"

    def test_close_enrollment(self):
        create_response = client.post("/courses/", json={
            "title": "Close Test",
            "description": "Test closing enrollment"
        })
        course_id = create_response.json()["id"]

        response = client.patch(f"/courses/{course_id}/close-enrollment")
        assert response.status_code == 200
        data = response.json()
        assert data["is_open"] == False

    def test_delete_course(self):
        create_response = client.post("/courses/", json={
            "title": "Delete Test",
            "description": "Test deletion"
        })
        course_id = create_response.json()["id"]

        response = client.delete(f"/courses/{course_id}")
        assert response.status_code == 204

    def test_get_course_users(self):
        course_response = client.post("/courses/", json={
            "title": "Users Test",
            "description": "Test getting users"
        })
        course_id = course_response.json()["id"]

        user_response = client.post("/users/", json={
            "name": "Course User",
            "email": "courseuser@example.com"
        })
        user_id = user_response.json()["id"]

        client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })

        response = client.get(f"/courses/{course_id}/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Course User"

class TestEnrollments:
    def setup_test_data(self):
        user_response = client.post("/users/", json={
            "name": "Enrollment User",
            "email": "enrolluser@example.com"
        })
        course_response = client.post("/courses/", json={
            "title": "Enrollment Course",
            "description": "Test enrollment"
        })
        return user_response.json()["id"], course_response.json()["id"]

    def test_enroll_user(self):
        user_id, course_id = self.setup_test_data()

        response = client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["course_id"] == course_id
        assert data["completed"] == False
        assert "enrolled_date" in data

    def test_enroll_inactive_user(self):
        user_id, course_id = self.setup_test_data()

        client.patch(f"/users/{user_id}/deactivate")

        response = client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })
        assert response.status_code == 400

    def test_enroll_closed_course(self):
        user_id, course_id = self.setup_test_data()

        client.patch(f"/courses/{course_id}/close-enrollment")

        response = client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })
        assert response.status_code == 400

    def test_duplicate_enrollment(self):
        user_id, course_id = self.setup_test_data()

        client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })

        response = client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })
        assert response.status_code == 400

    def test_get_all_enrollments(self):
        user_id, course_id = self.setup_test_data()
        client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })

        response = client.get("/enrollments/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_mark_completion(self):
        user_id, course_id = self.setup_test_data()
        enroll_response = client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })
        enrollment_id = enroll_response.json()["id"]

        response = client.patch(f"/enrollments/{enrollment_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True

    def test_get_user_enrollments(self):
        user_id, course_id = self.setup_test_data()
        client.post("/enrollments/", json={
            "user_id": user_id,
            "course_id": course_id
        })

        response = client.get(f"/enrollments/user/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
