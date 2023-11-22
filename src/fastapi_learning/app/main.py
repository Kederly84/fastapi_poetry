from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


@app.get('/hotels')
def get_hotels():
    res = {"hotels": "Some hotel"}
    return res


def main():
    run(
        'src.fastapi_learning.app.main:app',
        port=8000,
        host='127.0.0.1',
        reload=True
    )
