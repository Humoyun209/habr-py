from pydantic import BaseModel, EmailStr, model_validator, ValidationError


class UserScheme(BaseModel):
    username: str
    email: EmailStr
    password: str
    password2: str
    
    @model_validator(mode='after')
    def root_validate(cls, user: 'UserScheme'):
        if user.password != user.password2:
            return None
        return user
    

class UserLogin(BaseModel):
    username: str
    password: str


class ProfileUser(BaseModel):
    id: int
    username: str
    email: EmailStr
