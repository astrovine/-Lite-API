from typing import List, Optional, Dict
from datetime import datetime
import uuid
from schemas.models import User, UserCreate, UserUpdate, Course, CourseCreate, CourseUpdate, Enrollment, EnrollmentCreate

class UserService:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def create_user(self, user_data: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        user = User(id=user_id, **user_data.model_dump())
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self.users.values())

    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        return user

    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def deactivate_user(self, user_id: str) -> Optional[User]:
        if user_id not in self.users:
            return None

        self.users[user_id].is_active = False
        return self.users[user_id]

class CourseService:
    def __init__(self):
        self.courses: Dict[str, Course] = {}

    def create_course(self, course_data: CourseCreate) -> Course:
        course_id = str(uuid.uuid4())
        course = Course(id=course_id, **course_data.model_dump())
        self.courses[course_id] = course
        return course

    def get_course(self, course_id: str) -> Optional[Course]:
        return self.courses.get(course_id)

    def get_all_courses(self) -> List[Course]:
        return list(self.courses.values())

    def update_course(self, course_id: str, course_data: CourseUpdate) -> Optional[Course]:
        if course_id not in self.courses:
            return None

        course = self.courses[course_id]
        update_data = course_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)

        return course

    def delete_course(self, course_id: str) -> bool:
        if course_id in self.courses:
            del self.courses[course_id]
            return True
        return False

    def close_enrollment(self, course_id: str) -> Optional[Course]:
        if course_id not in self.courses:
            return None

        self.courses[course_id].is_open = False
        return self.courses[course_id]

class EnrollmentService:
    def __init__(self, user_service: UserService, course_service: CourseService):
        self.enrollments: Dict[str, Enrollment] = {}
        self.user_service = user_service
        self.course_service = course_service

    def enroll_user(self, enrollment_data: EnrollmentCreate) -> Optional[Enrollment]:
        user = self.user_service.get_user(enrollment_data.user_id)
        if not user or not user.is_active:
            return None

        course = self.course_service.get_course(enrollment_data.course_id)
        if not course or not course.is_open:
            return None

        existing_enrollment = self.get_user_course_enrollment(
            enrollment_data.user_id, enrollment_data.course_id
        )
        if existing_enrollment:
            return None

        enrollment_id = str(uuid.uuid4())
        enrollment = Enrollment(
            id=enrollment_id,
            user_id=enrollment_data.user_id,
            course_id=enrollment_data.course_id,
            enrolled_date=datetime.now()
        )
        self.enrollments[enrollment_id] = enrollment
        return enrollment

    def get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        return self.enrollments.get(enrollment_id)

    def get_all_enrollments(self) -> List[Enrollment]:
        return list(self.enrollments.values())

    def get_user_enrollments(self, user_id: str) -> List[Enrollment]:
        return [e for e in self.enrollments.values() if e.user_id == user_id]

    def get_course_enrollments(self, course_id: str) -> List[Enrollment]:
        return [e for e in self.enrollments.values() if e.course_id == course_id]

    def get_user_course_enrollment(self, user_id: str, course_id: str) -> Optional[Enrollment]:
        for enrollment in self.enrollments.values():
            if enrollment.user_id == user_id and enrollment.course_id == course_id:
                return enrollment
        return None

    def mark_completion(self, enrollment_id: str) -> Optional[Enrollment]:
        if enrollment_id not in self.enrollments:
            return None

        self.enrollments[enrollment_id].completed = True
        return self.enrollments[enrollment_id]
