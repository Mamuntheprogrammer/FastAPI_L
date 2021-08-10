from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
	return {'data':{'name ':'Mamun'}}

@app.get('/about')
def about():
	return {'data':{'info':'this is about page '}}