import json
import pickle
import time
import serial
from pathlib import Path
import keyboard
import JSON_generator
from dataclasses import dataclass

@dataclass
class Response:
    event_number: int
    event_content: list 
    event_time: float
    response: str
    response_time: float


key1 = 'enter'
key2 = '+'
key3 = '-'
key4 = '*'
PORT = "COM5"
BAUDRATE = 9600
JSON_FILE = Path("C:/Users/ddzhalag/Projects/JSON serial/sequence.json")
PKL_FILE = Path('C:/Users/ddzhalag/Projects/JSON serial/events_for_main.pkl')
RESULTS_FILE = Path('C:/Users/ddzhalag/Projects/JSON serial/results.csv')

response_data = []



def find_number(curr_time):
    temp = JSON_generator.Event_for_main(0, [], 0)
    for i in JSON_generator.events_for_main:
        if curr_time >= i.event_time:
            temp = i
        else:
            return temp.event_number
        

def key_handling(event):
    key = event.name
    curr_time = time.perf_counter() - start_time
    current_event_number = find_number(curr_time)
    if events_for_main[current_event_number].checked == False:
        events_for_main[current_event_number].checked = True
        if key == key1:
            write_event('1', curr_time, current_event_number)
        elif key == key2:
            write_event('2', curr_time, current_event_number)
        elif key == key3:
            write_event('3', curr_time, current_event_number)
        elif key == key4:
            write_event('4', curr_time, current_event_number)
        
def pickle_dump(file):
    with open(file, "rb") as f:
        result = pickle.load(f)
    return result

def JSON_dump(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        result = json.dumps(data, separators=(",", ":")) + "\n"
    return result

def write_event(response, response_time, event_number):
    event_time = events_for_main[event_number][2] # event_number
    event_content = events_for_main[event_number][1] # event_content
    response_data.append(Response(event_number, event_content, event_time, response, response_time))




def main():
    
    message = JSON_dump(JSON_FILE)
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    ser.write(message.encode("utf-8"))
    time.sleep(2)
    
    

    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        print(line)
        if line == 'START':
            start_time = time.perf_counter()
            break
        
        global current_time
        current_time = time.perf_counter()
    while current_time - start_time < JSON_generator.experiment_duration:
        
    
        keyboard.on_press(key_handling)
        current_time = time.perf_counter()
        keyboard.wait("esc")


    ser.close()


events_for_main = pickle_dump(PKL_FILE)
if __name__ == "__main__":
    main()

for i in response_data:
    print(i, end='\n')
