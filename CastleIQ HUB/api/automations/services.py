from fastapi import FastAPI, Depends, HTTPException

from core.services import ModelService
from .models import Automation, AutomationPydantic
from config import conf
from .events import *


class AutomationsService(ModelService):
    model = Automation
    pydantic_model_in = AutomationPydantic

    def __init__(self):
        super().__init__()

    async def all(self) -> AllAutomations:
        automations = await self.api_get_all()
        automations_event = AllAutomations(automations=automations)
        return automations_event

    async def create(self, create_automation: CreateAutomation) -> AutomationCreated:
        automation_db = await self.api_create_object(create_automation.automation)
        created_event = AutomationCreated(automation=automation_db)
        return created_event
