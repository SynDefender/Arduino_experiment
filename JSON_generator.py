from random import shuffle
from copy import deepcopy
from pathlib import Path
import json
import pickle
from dataclasses import dataclass

@dataclass
class Event_for_main:
    event_number:int
    event_contain:list
    event_time:float
    checked:bool=False


rgb_lamp = {"seq":{"color":"", "ons":[], "dur":[]}}
white_lamp = {"seq":{"ons":[], "dur":[]}}

LLvf_dict = deepcopy(rgb_lamp)
LRvf_dict = deepcopy(rgb_lamp)
RLvf_dict = deepcopy(rgb_lamp)
RRvf_dict = deepcopy(rgb_lamp)

struct = {"command":"PlaySeq","parameters":{"Leye":{"Lvf":{},"Rvf":{}},"Reye":{"Lvf":{},"Rvf":{}},"Lfix":{},"Rfix":{},"trig":{}}}
lamp_dict = ["LLvf", "LRvf", "RLvf", "RRvf", "Lfix", "Rfix", "trig"]
curr_lamp_dict =  ["LLvf", "LRvf", "RLvf", "RRvf"]


N = 12
DUR = 250
PAUSE = 1500
JSON_FILE = Path("C:/Users/ddzhalag/Projects/JSON serial/sequence.json")
PKL_FILE = Path('C:/Users/ddzhalag/Projects/JSON serial/events_for_main.pkl')
start_onset = 1000


case_1 = ["R", 0, 0, "G"]
case_2 = ["G", 0, 0, "R"]
case_3 = [0, "R", "G", 0]
case_4 = [0, "G", "R", 0]

cases_in_list = [case_1, case_2, case_3, case_4]
events_for_JSON = []
events_for_main = []


for event in cases_in_list:
    for _ in range(N // 4):
        events_for_JSON.append(event)

shuffle(events_for_JSON)



for number, event in enumerate(events_for_JSON):
    #print(event, end='\n')
    for j in range(4):
        if event[j]!=0:
            curr_dict = curr_lamp_dict[j] + '_dict'
            eval(curr_dict)["seq"]["color"] += event[j]
            eval(curr_dict)["seq"]["ons"].append(start_onset)
            eval(curr_dict)["seq"]["dur"].append(DUR)

    events_for_main.append(Event_for_main(number, event, start_onset))
    start_onset += PAUSE



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


start_onset += PAUSE
experiment_duration = start_onset

struct["parameters"]["Lfix"] = {"seq":{"ons":[1], "dur":[start_onset]}}
struct["parameters"]["Rfix"] = {"seq":{"ons":[1], "dur":[start_onset]}}

with open(JSON_FILE, "w") as f:
    json.dump(struct, f)

with open(PKL_FILE, 'wb') as f:
    pickle.dump(events_for_main, f)


'''for i in events_for_main:
    print(i, end='\n')

print(events_for_main[1].checked)
'''