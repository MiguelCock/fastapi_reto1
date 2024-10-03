import json
from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str
    correo: str


class Event(BaseModel):
    name: str
    users: list[User] = []


event_list = []


EVENTS_FILE = "events.json"


def load_events():
    global event_list
    try:
        with open(EVENTS_FILE, "r") as file:
            events_data = json.load(file)
            event_list = [Event(**event) for event in events_data]
    except FileNotFoundError:
        event_list = []


def save_events():
    with open(EVENTS_FILE, "w") as file:
        json.dump([event.dict() for event in event_list], file, indent=4)


app = FastAPI()

load_events()


@app.post("/create_event")
async def create_user(event: Event):
    event_list.append(event)
    save_events()
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
            save_events()
            return {"message": "user register succesfully"}
    return {"message": "user could not register"}
