from typing import List

from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from app.crud.comment import comment_crud
from app.db.database import get_db
from app.schemas.comment import Comment, CreateComment
from app.service.mock_comment_data import process_comment

router = APIRouter(prefix="/category", tags=["category"])


@router.post('/', response_model=Comment)
async def create_description(comment: CreateComment, db: Session = Depends(get_db)):
    return comment_crud.create(db, comment=comment.comment, rating=comment.rating, product_id=comment.product_id)


@router.post('/mock_data')
async def create_description(db: Session = Depends(get_db)):
    return process_comment(db)


@router.get("/{product_id}", response_model=List[Comment])
async def get_all_categories(product_id: int,
                             skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
                             limit: int = Query(10, ge=1, le=1000, description="Лимит записей"),
                             db: Session = Depends(get_db)):
    return comment_crud.get_all_by_product_id(db, product_id, skip, limit)

