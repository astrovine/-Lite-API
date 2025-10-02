# Course Management API🔗

A CRUD, RESTful API built with **FastAPI** for managing users, courses, and enrollments. This system allows users to register for courses, track completion, and manage course information with basic validation and relationships.

## Features

  * **User Management:** Create, Read, Update, Delete, and Deactivate users.
  * **Course Management:** Create, Read, Update, Delete, and Close enrollment for courses.
  * **Enrollment:** Enroll active users into open courses, prevent duplicate enrollments, and mark courses as completed.
  * **Reporting:** View all enrollments, enrollments for a specific user, or users enrolled in a specific course.
  * **Validation:** Utilizes **Pydantic** for robust data validation.
  * **Data Persistence:** Uses in-memory data structures (lists/dictionaries) for simple, fast development (Note: data will reset on API restart).

-----

## 🛠️ Technical Stack

  * **Framework:** FastAPI
  * **Data Validation:** Pydantic
  * **Language:** Python 3.13.7
  * **Data Storage:** In-memory lists/dictionaries (for simplicity, as per requirements)

-----

## Project Structure

The project follows a modular structure to separate concerns:

```
.
├── main.py            # Application entry point, mounts routes
├── test_main.py        
├── requirements.txt    
├── schemas/            # Pydantic models for data validation and response
│   ├── _init_.py
│   ├── models.py
├── routes/             # FastAPI routers for defining endpoints
│   ├── _init_.py
│   ├── users.py
│   ├── courses.py
│   └── enrollments.py
└── services/           # Business logic and in-memory data storage/manipulation
    ├── _init_.py
    ├── business_logic.py
    └── dependecies.py
```

-----

## ⚙️ Getting Started

### Prerequisites

You need **Python 3.8+** installed on your system.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/astrovine/-Lite-API
    cd lite-API
    ```

2.  **Create and activate a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the API

Start the server using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`.

### API Documentation (OpenAPI/Swagger UI)

You can access the interactive API documentation (Swagger UI) at:
👉 **`http://127.0.0.1:8000/docs`**

-----

## 🔗 API Endpoints

The API is structured around three main resources: **Users**, **Courses**, and **Enrollments**.

### User Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/users/` | Create a new user. |
| `GET` | `/users/` | Read all users. |
| `GET` | `/users/{user_id}` | Read a specific user. |
| `PUT` | `/users/{user_id}` | Update a user's information. |
| `DELETE` | `/users/{user_id}` | Delete a user. |
| `PATCH` | `/users/{user_id}/deactivate` | Deactivate a user (sets `is_active=False`). |

### Course Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/courses/` | Create a new course. |
| `GET` | `/courses/` | Read all courses. |
| `GET` | `/courses/{course_id}` | Read a specific course. |
| `PUT` | `/courses/{course_id}` | Update a course's information. |
| `DELETE` | `/courses/{course_id}` | Delete a course. |
| `PATCH` | `/courses/{course_id}/close` | Close enrollment for a course (sets `is_open=False`). |
| `GET` | `/courses/{course_id}/users` | View all users enrolled in a specific course. |

### Enrollment Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/enrollments/` | Enroll a user in a course (requires `user_id` and `course_id`). **Validation enforced:** User must be active, course must be open, no duplicate enrollments. |
| `GET` | `/enrollments/` | View all enrollments. |
| `GET` | `/enrollments/user/{user_id}` | View all enrollments for a specific user. |
| `PATCH` | `/enrollments/{enrollment_id}/complete` | Mark a course enrollment as completed (sets `completed=True`). |

-----

##  Running Tests

The API includes unit and integration tests to ensure all endpoints and business logic (like enrollment validation) work correctly.
-----

## 📝 Example Data Structure

The system manages three primary entities:

### User

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique identifier |
| `name` | `str` | Full name |
| `email` | `str` | Email address |
| `is_active` | `bool` | Whether the user can enroll (default: `True`) |

### Course

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique identifier |
| `title` | `str` | Name of the course |
| `description` | `str` | Brief description |
| `is_open` | `bool` | Whether enrollment is allowed (default: `True`) |

### Enrollment

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique identifier |
| `user_id` | `int` | ID of the enrolling user |
| `course_id` | `int` | ID of the course |
| `enrolled_date` | `str` | Date of enrollment (e.g., ISO format) |
| `completed` | `bool` | If the course was completed (default: `False`) |
