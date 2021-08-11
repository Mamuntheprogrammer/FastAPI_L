from fastapi import FastAPI,Depends
import schemas,models
from database import engine,SessionLocal

from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/blog')
def create(reqest:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=reqest.title,body=reqest.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog