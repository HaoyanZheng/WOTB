import keyboard
import time

try:
    print("Holding 'L'... (Ctrl+C to stop)")
    keyboard.press("l")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    keyboard.release("l")
    print("\nReleased 'L'. Exiting...")
