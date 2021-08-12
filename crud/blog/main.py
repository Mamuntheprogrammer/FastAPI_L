from fastapi import FastAPI,Depends,status,Response,HTTPException
from sqlalchemy.sql.expression import false
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


@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(reqest:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=reqest.title,body=reqest.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def blog(db:Session = Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200)
def show(id,response:Response,db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'details':f"id {id } is not found "}

    # another alternative above commented code
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id {id } is not found ")

    return blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response:Response,db:Session = Depends(get_db)):

    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "done"