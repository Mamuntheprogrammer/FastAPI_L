from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from sqlalchemy.sql.expression import false
import schemas,models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
models.Base.metadata.create_all(engine)
app = FastAPI()


@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=List[schemas.ShowBlog])
def blog(db:Session = Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog)
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

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id {id } is not found ")
    
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@app.post('/user')
def create_user(request:schemas.User,db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user