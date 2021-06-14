from pydantic import BaseModel


class CreatePost(BaseModel):
    title: str
    text: str


class AddComment(BaseModel):
    text: str
