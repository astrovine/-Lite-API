from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.models import Enrollment, EnrollmentCreate
from services.business_logic import EnrollmentService, UserService
from services.dependencies import get_enrollment_service, get_user_service

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def enroll_user(enrollment_data: EnrollmentCreate, enrollment_service: EnrollmentService = Depends(get_enrollment_service)):
    enrollment = enrollment_service.enroll_user(enrollment_data)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot enroll user. User may be inactive, course may be closed, or user already enrolled"
        )
    return enrollment

@router.get("/", response_model=List[Enrollment])
def get_all_enrollments(enrollment_service: EnrollmentService = Depends(get_enrollment_service)):
    return enrollment_service.get_all_enrollments()

@router.get("/{enrollment_id}", response_model=Enrollment)
def get_enrollment(enrollment_id: str, enrollment_service: EnrollmentService = Depends(get_enrollment_service)):
    enrollment = enrollment_service.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment

@router.patch("/{enrollment_id}/complete", response_model=Enrollment)
def mark_completion(enrollment_id: str, enrollment_service: EnrollmentService = Depends(get_enrollment_service)):
    enrollment = enrollment_service.mark_completion(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment

@router.get("/user/{user_id}", response_model=List[Enrollment])
def get_user_enrollments(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    enrollment_service: EnrollmentService = Depends(get_enrollment_service)
):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return enrollment_service.get_user_enrollments(user_id)
