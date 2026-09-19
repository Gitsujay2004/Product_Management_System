from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth_schema import(RegisterRequest,LoginRequest)
from app.services import auth_service
router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
async def register(user_data:RegisterRequest,db:AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(
        db=db,username=user_data.username,email=user_data.email,password=user_data.password

    )

    return{
        "message":"User registered successfully",
        "user":{
            "id":str(user.id),
            "username":user.user.username,
            "email":user.email
        }
    }

@router.post("/login")
async def login(
    login_data:LoginRequest,db:AsyncSession = Depends(get_db)):

    user = await auth_service.login_user(db=db,email=login_data.email,password=login_data.password)

    return{
        "message":"login successful",
        "user":{
            "id":str(user.id),
            "username":user.username,
            "email":user.email
        }
    }

    