import pytest

from castleiq_events import EventManager
from castleiq_events import Event, EventResult


# TODO rewrite

class TestEvent(Event):
    status_code = 200
    event_name = "TestEvent"
    message = "Hello Test"
    event_result = EventResult.SUCCESS


@pytest.fixture()
def event_manager() -> EventManager:
    em = EventManager()
    em.register_event(Event)
    em.register_event(TestEvent)
    return em


def test_registering_event():
    em = EventManager()
    em.register_event(Event)
    em.register_event(TestEvent)

    with pytest.raises(ValueError):
        em.register_event(Event)


async def test_event_fires(event_manager: EventManager):
    def sub(event: TestEvent):
        raise ValueError("Success")

    event_manager.subscribe_on(TestEvent, sub)
    with pytest.raises(ValueError):
        await event_manager.fire(TestEvent(message="Test"))


async def test_subscribe_on_event(event_manager: EventManager):
    def sub(event: TestEvent):
        assert event.event_name == "TestEvent"
        assert event.message == "Test"

    event_manager.subscribe_on(TestEvent, sub)
    await event_manager.fire(TestEvent(message="Test"))

    with pytest.raises(ValueError):
        event_manager.subscribe_on(TestEvent, sub)



async def test_decorator(event_manager: EventManager):
    @event_manager.on(TestEvent)
    def sub(event: TestEvent):
        assert event.event_name == "TestEvent"
        assert event.message == "Test"

    await event_manager.fire(TestEvent(message="Test"))
