from pydantic import BaseModel, EmailStr

class SchemaUserRegister(BaseModel):
    email: EmailStr
    password: str