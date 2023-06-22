import inspect
import json
from typing import Callable, Any, TypeVar

from .events import Event, ForwardEvent

E = TypeVar("E", bound=Event)
Subscriber = Callable[[E], Any]


class EventWrapper:
    def __init__(self, event_class: type[E] | None, event_name: str | None = None):
        self.event_class: type[E] | None = event_class
        self.name: str = event_class.__name__ if event_class else event_name
        self.subscribers: list[Subscriber] = []

    async def notify_subscribers(self, event: E) -> list[Any] | None:
        results = []
        if self.event_class:
            event = self.event_class(**(event.dict()))
        else:
            event = event
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

    def register_ingoing_event(self, event_class: type[E] | None, name: str | None = None):
        try:
            self.register_event(event_class, name)
        except ValueError:
            pass

        if not self.find_event_wrapper_by_name(event_class.__name__ if event_class else name, self._registered_events):
            self._registered_events.append(EventWrapper(event_class, name))
        else:
            pass
        return event_class

    def register_event(self, event_class: type[E] | None, name: str | None = None):
        if not self.find_event_wrapper_by_name(event_class.__name__ if event_class else name):
            self._events.append(EventWrapper(event_class, event_name=name))
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

    async def fire(self, event: E | str):
        if type(event) == str:
            event = json.loads(event)
            event_name = event.get("event_name", None)
        else:
            event_name = event.event_name
        ew = self.find_event_wrapper_by_name(event_name)
        if ew is None:
            raise ValueError(f"Event {event} not found")
        return await ew.notify_subscribers(event)

    def subscribe_on(self, event_class: type[E] | None, listener: Subscriber, event_name: str | None = None) -> None:
        ew = self.find_event_wrapper_by_name(event_class.__name__ if event_class else event_name)
        if not ew:
            self.register_event(event_class, event_name)
            return self.subscribe_on(event_class, listener, event_name)
        ew.subscribe(listener)

    def on(self, event_class: type[E] | None, event_name: str | None = None) -> Callable[[Subscriber], Subscriber]:
        def wrapper(func: Subscriber) -> Subscriber:
            self.subscribe_on(event_class, func, event_name)
            return func

        return wrapper

    def get_registered_events(self) -> list[dict[str:str]]:
        events = []
        for ev in self._registered_events:
            events.append({"name": ev.name, "event_schema": ev.event_class.schema()})
        return events

    def forward_event(self, to: int | str, event: E | dict | str, direction="To device"):
        # event_name = "ForwardEvent"
        # direction: Direction
        # device_id: int
        # event: dict
        if type(event) == str:
            event = json.loads(event)
        elif type(event) == dict:
            pass
        else:
            event = dict(event)
        forward = ForwardEvent(direction=direction, device_id=to, event=event)
        self.fire(forward)

    def add_automation(self, event_name, code):
        wrapper = self.find_event_wrapper_by_name(event_name)
        if not wrapper:
            self.register_event(None, event_name)
        wrapper = self.find_event_wrapper_by_name(event_name)
        code = compile(code, "<string>", "exec")
        print(code)

        def automation(event):

            a = exec(code, {
                "event_manager": self,
                "event": event,
                "Event": Event,
                "forward_to_device": self.forward_event
            })
            print(a)

        try:
            wrapper.subscribe(automation)
        except ValueError:
            pass
