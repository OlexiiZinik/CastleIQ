from typing import Callable, Any, TypeVar

from .events import Event

E = TypeVar("E", bound=Event)
Subscriber = Callable[[E], Any]


class EventWrapper:
    def __init__(self, event_class: type[E]):
        self.event_class: type[E] = event_class
        self.name: str = event_class.__name__
        self.subscribers: list[Subscriber] = []

    def notify_subscribers(self, event: E):
        for subscriber in self.subscribers:
            subscriber(event)

    def subscribe(self, subscriber: Subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
        else:
            raise ValueError(f"{subscriber} already subscribed")


class EventManager:
    def __init__(self):
        self._events: list[EventWrapper] = []

    def register_event(self, event_class: type[E]):
        if not self.find_event_wrapper_by_name(event_class.__name__):
            self._events.append(EventWrapper(event_class))
        else:
            raise ValueError(f"{event_class} already registered")

    def find_event_wrapper_by_name(self, event_name: str) -> EventWrapper | None:
        for e in self._events:
            if e.name == event_name:
                return e
        return None

    def fire(self, event: E):
        ew = self.find_event_wrapper_by_name(event.event_name)
        ew.notify_subscribers(event)

    def subscribe_on(self, event_class: type[E], listener: Subscriber) -> None:
        ew = self.find_event_wrapper_by_name(event_class.__name__)
        ew.subscribe(listener)

    def on(self, event_class: type[E]) -> Callable[[Subscriber], Subscriber]:
        def wrapper(func: Subscriber) -> Subscriber:
            self.subscribe_on(event_class, func)
            return func
        return wrapper
