from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.models import User, UserCreate, UserUpdate
from services.business_logic import UserService
from services.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)

@router.get("/", response_model=List[User])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)):
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.patch("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    user = user_service.deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
