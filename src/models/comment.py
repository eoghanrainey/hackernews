from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    id: int
    text: Optional[str] = None
    by: Optional[str] = None
    parent: Optional[int]
    time: Optional[int]
    deleted: Optional[bool] = None
    dead: Optional[bool] = None

class Comment_Most_Used(BaseModel):
    id: int
    text: Optional[str] = None
    by: Optional[str] = None
    parent: Optional[int]
    time: Optional[int]
    deleted: Optional[bool] = False
    dead: Optional[bool] = False