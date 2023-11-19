from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


def main():
    print('Here We Are!!!')
    run('src.fastapi_learning.app.main:app', port=8000, host='127.0.0.1', reload=True)
