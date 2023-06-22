from castleiq_events import ResponseEvent, EventResult, RequestEvent
from .models import Automation, AutomationPydantic


class AllAutomations(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "AllAutomations"
    message = ""
    automations: list[AutomationPydantic]


class CreateAutomation(RequestEvent):
    event_name = "CreateAutomation"
    automation: AutomationPydantic


class AutomationCreated(ResponseEvent):
    status_code = 201
    event_result = EventResult.SUCCESS
    event_name = "AutomationCreated"
    automation: AutomationPydantic
    message = "Створено автоматизацію"
