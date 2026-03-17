import json
import pickle

def pickle_dump(file):
    with open(file, "rb") as f:
        result = pickle.load(f)
    return result

def JSON_dump(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        result = json.dumps(data, separators=(",", ":")) + "\n"
    return result


def csv_load():
    pass

