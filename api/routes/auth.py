from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from api.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from api.middleware.rbac import get_current_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(req: LoginRequest):
    # Mocking DB check
    if req.email == "admin@nexra.com" and req.password == "admin":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": "mock-uuid-1234"}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
