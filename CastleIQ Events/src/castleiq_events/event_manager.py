import inspect
from typing import Callable, Any, TypeVar

from .events import Event

E = TypeVar("E", bound=Event)
Subscriber = Callable[[E], Any]


class EventWrapper:
    def __init__(self, event_class: type[E]):
        self.event_class: type[E] = event_class
        self.name: str = event_class.__name__
        self.subscribers: list[Subscriber] = []

    async def notify_subscribers(self, event: E) -> list[Any] | None:
        results = []
        event = self.event_class(**(event.dict()))
        for subscriber in self.subscribers:
            if inspect.iscoroutinefunction(subscriber):
                results.append(await subscriber(event))
            else:
                results.append(subscriber(event))

        return results if len(results) > 0 else None

    def subscribe(self, subscriber: Subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
        else:
            raise ValueError(f"{subscriber} already subscribed")


class EventManager:
    def __init__(self):
        self._events: list[EventWrapper] = []
        self._registered_events: list[EventWrapper] = []

    def register_ingoing_event(self, event_class: type[E]):
        try:
            self.register_event(event_class)
        except ValueError:
            pass

        if not self.find_event_wrapper_by_name(event_class.__name__, self._registered_events):
            self._registered_events.append(EventWrapper(event_class))
        else:
            pass
        return event_class

    def register_event(self, event_class: type[E]):
        if not self.find_event_wrapper_by_name(event_class.__name__):
            self._events.append(EventWrapper(event_class))
        else:
            raise ValueError(f"{event_class} already registered")
        return event_class

    def find_event_wrapper_by_name(self, event_name: str, where: list = None) -> EventWrapper | None:
        if where is None:
            where = self._events
        for e in where:
            if e.name == event_name:
                return e
        return None

    async def fire(self, event: E):
        ew = self.find_event_wrapper_by_name(event.event_name)
        if ew is None:
            raise ValueError(f"Event {event} not found")
        return await ew.notify_subscribers(event)

    def subscribe_on(self, event_class: type[E], listener: Subscriber) -> None:
        ew = self.find_event_wrapper_by_name(event_class.__name__)
        if not ew:
            self.register_event(event_class)
            return self.subscribe_on(event_class, listener)
        ew.subscribe(listener)

    def on(self, event_class: type[E]) -> Callable[[Subscriber], Subscriber]:
        def wrapper(func: Subscriber) -> Subscriber:
            self.subscribe_on(event_class, func)
            return func

        return wrapper

    def get_registered_events(self) -> list[dict[str:str]]:
        events = []
        for ev in self._registered_events:
            events.append({"name": ev.name, "event_schema": ev.event_class.schema()})
        return events
