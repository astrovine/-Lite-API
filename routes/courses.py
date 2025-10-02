from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.models import Course, CourseCreate, CourseUpdate, User
from services.business_logic import CourseService, UserService, EnrollmentService
from services.dependencies import get_course_service, get_user_service, get_enrollment_service

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, course_service: CourseService = Depends(get_course_service)):
    return course_service.create_course(course)

@router.get("/", response_model=List[Course])
def get_all_courses(course_service: CourseService = Depends(get_course_service)):
    return course_service.get_all_courses()

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: str, course_service: CourseService = Depends(get_course_service)):
    course = course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=Course)
def update_course(course_id: str, course_data: CourseUpdate, course_service: CourseService = Depends(get_course_service)):
    course = course_service.update_course(course_id, course_data)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: str, course_service: CourseService = Depends(get_course_service)):
    if not course_service.delete_course(course_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

@router.patch("/{course_id}/close-enrollment", response_model=Course)
def close_enrollment(course_id: str, course_service: CourseService = Depends(get_course_service)):
    course = course_service.close_enrollment(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.get("/{course_id}/users", response_model=List[User])
def get_course_users(
    course_id: str,
    course_service: CourseService = Depends(get_course_service),
    user_service: UserService = Depends(get_user_service),
    enrollment_service: EnrollmentService = Depends(get_enrollment_service)
):
    course = course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    enrollments = enrollment_service.get_course_enrollments(course_id)
    users = []
    for enrollment in enrollments:
        user = user_service.get_user(enrollment.user_id)
        if user:
            users.append(user)

    return users
