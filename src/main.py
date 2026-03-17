
import time
import serial

import keyboard
import JSON_generator

import io_utils
import config
import models




def find_number(curr_time):
    current_number = 0
    for event in events_for_main:
        if curr_time >= event.event_time:
            current_number = event.event_number
        else:
            break
    return current_number
        

def key_handling(event):
    if finished or start_time is None:
        return

    key = event.name
    curr_time = time.perf_counter() - start_time
    current_event_number = find_number(curr_time)
    current_event = events_for_main[current_event_number]

    if current_event.checked:
        return

    if key == config.key1:
        write_event('1', curr_time, current_event_number)
    elif key == config.key2:
        write_event('2', curr_time, current_event_number)
    elif key == config.key3:
        write_event('3', curr_time, current_event_number)
    elif key == config.key4:
        write_event('4', curr_time, current_event_number)
    else:
        print("Wrong key")
        return

    current_event.checked = True
    print(f"The response has been accepted {current_event_number}")
    


def write_event(response, response_time, event_number):
    event_time = events_for_main[event_number].event_time # event_number
    event_content = events_for_main[event_number].event_content # event_content
    response_data.append(models.Response(event_number, event_content, event_time, response, response_time))




def main():
    global current_time, start_time, finished


    message = io_utils.JSON_dump(config.JSON_FILE)
    ser = serial.Serial(config.PORT, config.BAUDRATE, timeout=1)
    time.sleep(2)
    ser.write(message.encode("utf-8"))
    time.sleep(2)
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8", errors="replace").strip()
            if line == "START":
                print("Start", end='\n')
                start_time = time.perf_counter()
                finished = False
                break


    keyboard.on_press(key_handling)

       
    
    try:
        current_time = time.perf_counter()
        while current_time - start_time < experiment_duration:
            current_time = time.perf_counter()
            time.sleep(0.01)
    finally:
        keyboard.unhook_all()
        finished = True
        print('Finish')
        ser.close()
        for i in response_data:
            print(i, end='\n')
    return


events_for_main = io_utils.pickle_dump(config.PKL_FILE)
experiment_duration = events_for_main.pop() 
print(events_for_main)
response_data = []


if __name__ == "__main__":
    main()

keyboard.wait("esc")


