from services.business_logic import UserService, CourseService, EnrollmentService

user_service = UserService()
course_service = CourseService()
enrollment_service = EnrollmentService(user_service, course_service)

def get_user_service():
    return user_service

def get_course_service():
    return course_service

def get_enrollment_service():
    return enrollment_service
