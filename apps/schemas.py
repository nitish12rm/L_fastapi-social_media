from pydantic import BaseModel,EmailStr,conint,ConfigDict
from typing import Optional
from fastapi.params import Body

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        form_attributes = True
class PostBase(BaseModel):
    title:str
    content:str
    is_published: Optional[bool] = False
class PostCreate(PostBase):
    pass

class PostOut(BaseModel):
    title: str
    content: str
    owner_id: int
    owner: UserOut

    class Config:
        form_attributes = True
class PostOut_vote(BaseModel):
    Post: PostOut
    votes: int
    class Config:
        form_attributes = True
        

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id:Optional[int] = None
     
class vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)