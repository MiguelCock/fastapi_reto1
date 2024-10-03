from fastapi import FastAPI
from pydantic import BaseModel


class Event(BaseModel):
    name: str
    users: list = []


class User(BaseModel):
    name: str
    correo: str


event_list = []

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_event")
async def create_user(event: Event):
    event_list.append(event)
    return {"message": "event created succesfully"}


@app.get("/get_events")
async def get_events():
    print(event_list)
    return event_list


@app.post("/subscribe")
async def subscribe(user: User, event_name: str):
    for event in event_list:
        if event.name == event_name:
            event.users.append(user)
            return {"message": "user register succesfully"}
    return {"message": "user could not register"}
