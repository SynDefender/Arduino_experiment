import json
import pickle
import time
import serial
import keyboard
from pathlib import Path
from dataclasses import dataclass, field

import JSON_generator


@dataclass
class Response:
    event_number: int
    event_content: list
    event_time: float
    response: str
    response_time: float


@dataclass
class ExperimentState:
    start_time: float | None = None
    response_data: list[Response] = field(default_factory=list)


key1 = "enter"
key2 = "+"
key3 = "-"
key4 = "*"

PORT = "COM5"
BAUDRATE = 9600
JSON_FILE = Path("C:/Users/ddzhalag/Projects/JSON serial/sequence.json")
PKL_FILE = Path("C:/Users/ddzhalag/Projects/JSON serial/events_for_main.pkl")


def load_pickle(file: Path):
    with open(file, "rb") as f:
        return pickle.load(f)


def load_json_as_line(file: Path) -> str:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, separators=(",", ":")) + "\n"


def find_event_number(curr_time: float, events_for_main) -> int:
    current_number = 0

    for event in events_for_main:
        if curr_time >= event.event_time:
            current_number = event.event_number
        else:
            break

    return current_number


def write_event(state: ExperimentState, response: str, response_time: float, event_number: int, events_for_main):
    event = events_for_main[event_number]
    state.response_data.append(
        Response(
            event_number=event.event_number,
            event_content=event.event_content,
            event_time=event.event_time,
            response=response,
            response_time=response_time,
        )
    )


def make_key_handler(state: ExperimentState, events_for_main):
    def key_handling(event):
        if state.start_time is None:
            return

        key = event.name
        curr_time = time.perf_counter() - state.start_time
        current_event_number = find_event_number(curr_time, events_for_main)
        current_event = events_for_main[current_event_number]

        if current_event.checked:
            return

        if key == key1:
            current_event.checked = True
            write_event(state, "1", curr_time, current_event_number, events_for_main)
        elif key == key2:
            current_event.checked = True
            write_event(state, "2", curr_time, current_event_number, events_for_main)
        elif key == key3:
            current_event.checked = True
            write_event(state, "3", curr_time, current_event_number, events_for_main)
        elif key == key4:
            current_event.checked = True
            write_event(state, "4", curr_time, current_event_number, events_for_main)

    return key_handling


def main():
    events_for_main = load_pickle(PKL_FILE)
    state = ExperimentState()

    message = load_json_as_line(JSON_FILE)
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    ser.write(message.encode("utf-8"))

    while True:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if not line:
            continue

        print(line)

        if line == "START":
            state.start_time = time.perf_counter()
            break

    handler = make_key_handler(state, events_for_main)
    keyboard.on_press(handler)

    try:
        while time.perf_counter() - state.start_time < JSON_generator.experiment_duration:
            if keyboard.is_pressed("esc"):
                break
            time.sleep(0.001)
    finally:
        keyboard.unhook_all()
        ser.close()

    for item in state.response_data:
        print(item)


        


if __name__ == "__main__":
    main()