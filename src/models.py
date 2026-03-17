from dataclasses import dataclass

@dataclass
class Response:
    event_number: int
    event_content: list 
    event_time: float
    response: str
    response_time: float

@dataclass
class Event_for_main:
    event_number: int
    event_content: list
    event_time: float
    checked: bool=False