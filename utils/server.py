# run=uvicorn server:app --host 0.0.0.0
from fastapi import FastAPI, HTTPException
from os import system
import json

app = FastAPI()
PYTHON = "python3"

try:
    with open("secrets.json", "r") as f:
        config_json = json.load(f)
        USER = config_json["USER"]
        REPO = config_json["REPO"]
        GH_PASSWORD = config_json["GH_PASSWORD"]
        CICD_HASH = config_json["CICDHASH"]
except:
    print("error while reading secrets.json")
    exit(0)


@app.get("/cicd/{hash}")
def pull(hash: str):
    if hash != CICD_HASH:
        raise HTTPException(status_code=404, detail="bad")
    system(f"{PYTHON} cicd.py &")
    return "ok"
