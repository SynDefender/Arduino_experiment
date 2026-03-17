import keyboard

def on_key(event):
    print("Нажата:", event.name)

keyboard.on_press(on_key)

print("Жми клавиши. Для выхода: Esc")
keyboard.wait("esc")