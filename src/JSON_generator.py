from random import shuffle
from copy import deepcopy
from pathlib import Path
import json
import pickle
import models
import config




rgb_lamp = {"seq":{"color":"", "ons":[], "dur":[]}}
white_lamp = {"seq":{"ons":[], "dur":[]}}
struct = {"command":"PlaySeq","parameters":{"Leye":{"Lvf":{},"Rvf":{}},"Reye":{"Lvf":{},"Rvf":{}},"Lfix":{},"Rfix":{},"trig":{}}}

LLvf_dict = deepcopy(rgb_lamp)
LRvf_dict = deepcopy(rgb_lamp)
RLvf_dict = deepcopy(rgb_lamp)
RRvf_dict = deepcopy(rgb_lamp)
Lfix_dict = deepcopy(white_lamp)
Rfix_dict = deepcopy(white_lamp)
trig_dict = deepcopy(white_lamp)



lamp_dict = ["LLvf", "LRvf", "RLvf", "RRvf", "Lfix", "Rfix", "trig"]
curr_lamp_dict = lamp_dict[:]


N = 22
DUR = 250
PAUSE = 500
start_onset = 1000
CONSTANT_WHITE = False
TRIGGER_DUR = 100

if CONSTANT_WHITE:
    case_1 = ["R", "G", "R", "G"]
    case_2 = ["R", "G", 0, 0]
    case_3 = [0, 0, "R", "G"]
    case_4 = ["R", "G", "R", "G"]

else:
    case_1 = ["G", "G", "0", "0", 1, 0, 1]
    case_2 = ["0", "0", "G", "G", 0, 1, 1]
    case_3 = ["0", "0", "0", "0", 1, 1, 1]
    case_4 = ["0", "0", "0", "0", 0, 0, 1]



cases_in_list = [case_1, case_2, case_3, case_4]
cases_in_list = cases_in_list[:2]
events_number = len(cases_in_list)
events_for_JSON = []
events_for_main = []



for event in cases_in_list:
    for _ in range(N // events_number):
        events_for_JSON.append(event)

shuffle(events_for_JSON)


micro_events_number = sum(sum(map(lambda a: 1 if a != 0 and a != '0' else 0, x)) for x in events_for_JSON)

pause = PAUSE
duration = DUR

for number, event in enumerate(events_for_JSON):
    #print(event, end='\n')
    for j in range(4):
        if event[j]!=0 and event[j]!='0':
            curr_dict = curr_lamp_dict[j] + '_dict'
            eval(curr_dict)["seq"]["color"] += event[j]
            eval(curr_dict)["seq"]["ons"].append(start_onset)
            eval(curr_dict)["seq"]["dur"].append(duration)
    if CONSTANT_WHITE == False:
        for j in range(4, 7):
            if event[j]!=0 and event[j]!='0':
                curr_dict = curr_lamp_dict[j] + '_dict'
                eval(curr_dict)["seq"]["ons"].append(start_onset)
                eval(curr_dict)["seq"]["dur"].append(duration) #if curr_lamp_dict[j]!='trig' else TRIGGER_DUR)


    events_for_main.append(models.Event_for_main(number, event, start_onset))
    #pause += 2
    #duration += 1
    start_onset += pause



for j in curr_lamp_dict:
    match j:
        case "LLvf":
            struct["parameters"]["Leye"]["Lvf"] = LLvf_dict
        case "LRvf":
            struct["parameters"]["Leye"]["Rvf"] = LRvf_dict
        case "RLvf":
            struct["parameters"]["Reye"]["Lvf"] = RLvf_dict
        case "RRvf":
            struct["parameters"]["Reye"]["Rvf"] = RRvf_dict
        case "Lfix":
            struct["parameters"]["Lfix"] = Lfix_dict
        case "Rfix":
            struct["parameters"]["Rfix"] = Rfix_dict
        case "trig":
            struct["parameters"]["trig"] = trig_dict

if CONSTANT_WHITE:
    struct["parameters"]["Lfix"] = {"seq":{"ons":[1], "dur":[start_onset]}}
    struct["parameters"]["Rfix"] = {"seq":{"ons":[1], "dur":[start_onset]}}

start_onset += PAUSE
experiment_duration = start_onset

print(f'The amount of events for Arduino is {micro_events_number}')


events_for_main.append(experiment_duration)
with open(config.JSON_FILE, "w") as f:
    json.dump(struct, f)

with open(config.PKL_FILE, 'wb') as f:
    pickle.dump(events_for_main, f)


'''for i in events_for_main:
    print(i, end='\n')

print(events_for_main[1].checked)
'''