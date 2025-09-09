from pydantic import BaseModel, EmailStr, SecretStr, field_validator, model_validator
from .models import User
from app.users import auth

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @field_validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        password = values.data["password"]
        password_confirm = v
        if password != password_confirm:
            raise ValueError("Password doesn't match!")
        return v

    @field_validator("email")
    def email_available(cls, v, values, **kwargs):
        q = User.objects().filter(email=v).allow_filtering()
        if q.count() != 0:
            raise ValueError("Email is not available.")
        return v
    
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: str = None

    @model_validator(mode='before')
    @classmethod
    def validate_user(cls, values):
        err_msg = "Incorrect credentials, please try again."
        email = values["email"] or None
        password = values["password"] or None
        if email is None or password is None:
            raise ValueError(err_msg)
        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(err_msg)
        token = auth.login(user_obj)
        values["session_id"] = token
        return values

