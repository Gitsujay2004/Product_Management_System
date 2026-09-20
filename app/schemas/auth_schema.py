from pydantic import BaseModel,EmailStr

class RegisterRequest(BaseModel):
    username:str
    email:EmailStr
    password:str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class RefreshTokenRequest(BaseModel):
    refresh_token:str
    token_type:str