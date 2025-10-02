from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    id: str = None
    name: str
    email: str
    is_active: bool = True

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class Course(BaseModel):
    id: str = None
    title: str
    description: str
    is_open: bool = True

class CourseCreate(BaseModel):
    title: str
    description: str

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None

class Enrollment(BaseModel):
    id: str = None
    user_id: str
    course_id: str
    enrolled_date: datetime = None
    completed: bool = False

class EnrollmentCreate(BaseModel):
    user_id: str
    course_id: str

class EnrollmentUpdate(BaseModel):
    completed: Optional[bool] = None
