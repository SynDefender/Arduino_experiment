import json
import time
import serial
import config



def main():
    with open(config.JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    message = json.dumps(data, separators=(",", ":")) + "\n"

    ser = serial.Serial(config.PORT, config.BAUDRATE, timeout=1)
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

    

    