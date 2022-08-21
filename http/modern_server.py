# uvicorn modern_server:app --reload
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str


@app.get('/')
async def root():
    return 'Hello world!'

@app.get('/healthz')
async def health():
    return 'OK'

@app.get('/query')
async def query(n: int):
    return [ i for i in range(n) ]

@app.post('/')
async def root(body: User):
    user = body.dict()
    return f'Hello {user["name"]}! Your id is {user["id"]}.'
