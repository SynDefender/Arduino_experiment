
import time
import serial

import keyboard
import JSON_generator

import io_utils
import config
import models





response_data = []



def find_number(curr_time):
    temp = JSON_generator.Event_for_main(0, [], 0)
    for i in events_for_main:
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
        if key == config.key1:
            write_event('1', curr_time, current_event_number)
        elif key == config.key2:
            write_event('2', curr_time, current_event_number)
        elif key == config.key3:
            write_event('3', curr_time, current_event_number)
        elif key == config.key4:
            write_event('4', curr_time, current_event_number)
        


def write_event(response, response_time, event_number):
    event_time = events_for_main[event_number][2] # event_number
    event_content = events_for_main[event_number][1] # event_content
    response_data.append(models.Response(event_number, event_content, event_time, response, response_time))




def main():
    
    message = io_utils.JSON_dump(config.JSON_FILE)
    ser = serial.Serial(config.PORT, config.BAUDRATE, timeout=1)
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


events_for_main = io_utils.pickle_dump(config.PKL_FILE)
if __name__ == "__main__":
    main()

for i in response_data:
    print(i, end='\n')
