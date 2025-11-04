from app.crud.base import CreateReadBase
from app.db.base import Comment
from sqlalchemy.orm import Session


class CommentCRUD(CreateReadBase[Comment]):
    def get_all_by_product_id(self, db: Session, product_id: int, skip: int = 10, limit: int = 10):
        return db.query(self.model).filter(self.model.product_id == product_id).offset(skip).limit(limit).all()


comment_crud = CommentCRUD(Comment)
