from typing import Union

from fastapi import FastAPI
import database

app = FastAPI()
database.create()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event('shutdown')
def shutdown_event():
    database.drop()
    print("Database dropped")
