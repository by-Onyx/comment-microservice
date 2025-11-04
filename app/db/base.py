from app.db.database import Base, engine
from app.db.models.comment import Comment

Base.metadata.create_all(bind=engine)