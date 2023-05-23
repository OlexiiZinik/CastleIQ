import pytest

from core.events.event_manager import EventManager
from core.events.events import Event, EventResult


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


def test_event_fires(event_manager: EventManager):
    def sub(event: TestEvent):
        raise ValueError("Succes")

    event_manager.subscribe_on(TestEvent, sub)
    with pytest.raises(ValueError):
        event_manager.fire(TestEvent(message="Test"))


def test_subscribe_on_event(event_manager: EventManager):
    def sub(event: TestEvent):
        assert event.event_name == "TestEvent"
        assert event.message == "Test"

    event_manager.subscribe_on(TestEvent, sub)
    event_manager.fire(TestEvent(message="Test"))

    with pytest.raises(ValueError):
        event_manager.subscribe_on(TestEvent, sub)


def test_decorator(event_manager: EventManager):
    @event_manager.on(TestEvent)
    def sub(event: TestEvent):
        assert event.event_name == "TestEvent"
        assert event.message == "Test"

    event_manager.fire(TestEvent(message="Test"))


