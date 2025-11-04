from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    id: Optional[int] = None
    comment: Optional[str] = None
    rating: Optional[int] = None
    date: Optional[datetime] = None
    product_id: Optional[int] = None

    class Config:
        from_attributes = True

class CreateComment(BaseModel):
    comment: Optional[str] = None
    rating: Optional[int] = None
    date: Optional[datetime] = None
    product_id: Optional[int] = None

    class Config:
        from_attributes = True