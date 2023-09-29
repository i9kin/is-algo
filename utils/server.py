from fastapi import FastAPI, HTTPException
from os import system

app = FastAPI()
PYTHON = 'python3'

@app.get("/cicd/{HASH}")
def pull(hash: str):
    if not validate(owner, repo, hash):
        raise HTTPException(status_code=404, detail='(')
    system(f'{PYTHON} cicd.py &')
    return "ok"