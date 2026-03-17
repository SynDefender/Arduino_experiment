import json
import time
import serial
from pathlib import Path

PORT = "COM5"
BAUDRATE = 9600
JSON_FILE = Path("C:/Users/ddzhalag/Projects/JSON serial/sequence.json")

def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    message = json.dumps(data, separators=(",", ":")) + "\n"

    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)

    ser.write(message.encode("utf-8"))
    print("SENT:")
    print(message)

    time.sleep(2)
    

    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if line:
            print("ARDUINO:", line)

    ser.close()
if __name__ == "__main__":
    main()