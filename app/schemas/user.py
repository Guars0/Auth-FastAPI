from pydantic import BaseModel, EmailStr, field_validator

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def password_length(cls, v):
        if len(v) < 72:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(UserBase):
    id: int
    is_superuser: bool

    class Config: 
        from_attributes = True

