import config
import io_utils

def find_number(curr_time):
    current_number = 0
    for event in events_for_main:
        if curr_time >= event.event_time:
            current_number = event.event_number
        else:
            break
    return current_number




events_for_main = io_utils.pickle_dump(config.PKL_FILE)
last = events_for_main.pop()
for i in events_for_main:
    print(i, end='\n')
print()
print(last)


print(find_number(3100))