import time
from pynput.mouse import Controller, Button

mouse = Controller()
while True:
    mouse.click(Button.left, 1)
    time.sleep(60)  # Clicks every 60 seconds