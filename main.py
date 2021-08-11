from fastapi import FastAPI
from typing import Optional
# for Post method
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
def index():
	return {'data':{'name ':'Mamun'}}


@app.get('/about/unpublished')
def unpublished():
	return {'data':'working'}


@app.get('/about/{id}')
def about(id: int):
	return {'data':id}

# limitng , validate , default value , Optional

@app.get('/blog2')
def blog2(limit:int = 10 ,published:bool = True, sort:Optional[str]=None):
	
	if published:
		return {'data':f"{limit} blog found "}
	else:
		return { limit }


# ------------------------------ Post METHOD --------------------
# Need pydentic base mode 

class Blog(BaseModel):
	title:str
	body:str
	published_at:Optional[bool]


@app.post('/blog')
def create_blog(request:Blog):
	return {f" blog is created and title is {request.title}"}