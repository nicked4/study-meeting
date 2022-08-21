import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return 'Hello world!'

@app.get('/query')
async def query(n: int):
    return [ i for i in range(n) ]


if __name__ == '__main__':
    uvicorn.run(
        'fastapi_https:app',
        port=8443,
        ssl_keyfile='./keys/server.key',
        ssl_certfile='./keys/server.crt',
    )
