from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth_schema import RegisterRequest, LoginRequest,RefreshTokenRequest
from app.services import auth_service
from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await auth_service.register_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/login")
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await auth_service.login_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    user, access_token , refresh_token = result

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email
        }
    }

#get_my_profile 

@router.get("/me")
async def get_my_profile(
    current_user = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }

@router.post("/refresh")
async def refresh_token(
    token_data : RefreshTokenRequest,db:AsyncSession=Depends(get_db)
):

    new_access_token = await auth_service.refresh_access_token(db=db,refresh_token=token_data.refresh_token)

    if new_access_token is None:
        raise HTTPException(status_code=401,detail="Invalid or expired Refresh token")

    
    return {
        "message": "Access token refreshed successfully",
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(token_data:RefreshTokenRequest,db:AsyncSession = Depends(get_db)):
    result = await auth_service.logout_user(db.db,refresh_token=token_data.refresh_token)
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    
    return {
        "message": "Logout successful"
    }