from fastapi import FastAPI
from castleiq_events import EventManager


event_manager = EventManager()
driver = FastAPI()
