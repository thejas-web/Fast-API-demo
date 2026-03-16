from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    email : str
    password : str



class UserResponse(BaseModel):
    id : int
    name : str
    email : str

    class config:
        from_attributes = True


class Login(BaseModel):
    email : str
    password : str