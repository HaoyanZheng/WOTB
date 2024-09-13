import pyautogui
import random
import time
import cv2
import pytesseract
import numpy as np
import re
import threading

speed_dropped_time = None
# BATTLE! at home screen
roi_start = (700, 980, 250, 40)

# speed section in game
roi_speed = (690, 1050, 30, 20)

# first word when destroyed
roi_destroyed = (730, 900, 40, 30)

# end_game screen
roi_end = (160, 50, 95, 30)

# distance
roi_distance = (1020, 560, 40, 10)

# energy tank list
roi_wait_start = (850, 420, 200, 100)

# hold key
def hold_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def get_start():
    screenshot_start = pyautogui.screenshot(region=roi_start)
    text_start = pytesseract.image_to_string(screenshot_start)
    return text_start

def get_destroyed():
    screenshot_destroyed = pyautogui.screenshot(region=roi_destroyed)
    text_destroyed = pytesseract.image_to_string(screenshot_destroyed)
    return text_destroyed

def get_end():
    screenshot_end = pyautogui.screenshot(region=roi_end)
    text_end = pytesseract.image_to_string(screenshot_end)
    return text_end

def get_speed():
    screenshot_speed = pyautogui.screenshot(region=roi_speed)
    text_speed = pytesseract.image_to_string(screenshot_speed)
    match_speed = re.search(r'\d+', text_speed)
    if match_speed:
        speed = int(match_speed.group())
    else:
        speed = None
    return speed

def get_distance():
    screenshot_distance = pyautogui.screenshot(region=roi_distance)
    text_distance = pytesseract.image_to_string(screenshot_distance)
    match_distance = re.search(r'\d+', text_distance)
    if match_distance:
        distance = int(match_distance.group())
    else:
        distance = None
    return distance

def wait_start():
    screenshot_wait_start = pyautogui.screenshot(region=roi_wait_start)
    text_wait_start = pytesseract.image_to_string(screenshot_wait_start)
    return text_wait_start

def random_signals():
    # Define the keys and their probabilities
    keys = ['o', 'i', 't', 'u', 'nothing']
    probabilities = [0.04, 0.02, 0.02, 0.02, 0.9]
    # Choose a key based on the probabilities
    chosen_key = random.choices(keys, probabilities, k=1)[0]
    # Press the chosen key if it's not 'nothing'
    if chosen_key != 'nothing':
        print(f"Pressing {chosen_key}")
        pyautogui.press(chosen_key)

def random_buff():
    # Define the keys and their probabilities
    keys = ['4', '7']
    probabilities = [0.1, 0.9]
    # Choose a key based on the probabilities
    chosen_key = random.choices(keys, probabilities, k=1)[0]
    # Press the chosen key if it's not 'nothing'
    if chosen_key != 'nothing':
        print(f"Pressing {chosen_key}")
        pyautogui.press(chosen_key)

def random_motion():
    keys = ['w', 's', 'a', 'd']
    probabilities = [0.5, 0.3, 0.1, 0.1]
    chosen_key = random.choices(keys, probabilities, k=1)[0]
    print(f"No speed, running {chosen_key}")
    if chosen_key == 'w':
        hold_key(chosen_key, random.randint(5, 10))
    elif chosen_key == 's':
        hold_key(chosen_key, random.randint(4, 6))
    elif chosen_key == 'a':
        hold_key(chosen_key, random.randint(1, 5))
    else:
        hold_key(chosen_key, random.randint(1, 5))

def random_shooting():
    # Define the probability of shooting
    shoot_probability = 0.2
    # Generate a random number between 0 and 1
    random_number = random.random()
    # If the random number is less than the shoot probability, click the left mouse button
    if random_number < shoot_probability:
        pyautogui.click(button='left')

def detect_enemy():
    global speed_dropped_time
    speed = get_speed()
    distance = get_distance()
    if speed is not None:
        random_signals()
        random_buff()
        random_shooting()
        print('got speed', speed)
        if speed < 30:
            pyautogui.keyDown('w')
            if speed < 10:
                if speed_dropped_time is None:
                    speed_dropped_time = time.time()
                elif time.time() - speed_dropped_time > 5:
                    speed_dropped_time = None
                    print("Speed has been below 10 for more than 5 seconds!")
                    direction = random.choice(['left', 'right'])
                    if direction == 'left':
                        distance = get_distance()
                        if distance is not None:
                            if distance < 20:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveRel(-random.randint(50, 500), 0)
                                pyautogui.mouseUp(button='left')
                                distance = get_distance()  # Update distance
                            pyautogui.keyDown('a' if direction == 'left' else 'd')
                            time.sleep(2)  # Hold the key for a moment
                            pyautogui.keyUp('a' if direction == 'left' else 'd')
                    else:
                        distance = get_distance()
                        if distance is not None:
                            if distance < 20:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveRel(random.randint(50, 500), 0)
                                pyautogui.mouseUp(button='left')
                                distance = get_distance()  # Update distance
                                pyautogui.keyDown('a' if direction == 'left' else 'd')
                                time.sleep(2)  # Hold the key for a moment
                                pyautogui.keyUp('a' if direction == 'left' else 'd')
            else:
                # The speed is not below 10, so reset the timer
                speed_dropped_time = None
    elif distance is not None:
        random_signals()
        random_buff()
        random_shooting()
        print('got speed', speed)
        if distance < 30:
            pyautogui.keyDown('w')
            if distance < 10:
                if speed_dropped_time is None:
                    speed_dropped_time = time.time()
                elif time.time() - speed_dropped_time > 5:
                    speed_dropped_time = None
                    print("Speed has been below 10 for more than 5 seconds!")
                    direction = random.choice(['left', 'right'])
                    if direction == 'left':
                        distance = get_distance()
                        if distance is not None:
                            if distance < 20:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveRel(-random.randint(50, 500), 0)
                                pyautogui.mouseUp(button='left')
                                distance = get_distance()  # Update distance
                            pyautogui.keyDown('a' if direction == 'left' else 'd')
                            time.sleep(2)  # Hold the key for a moment
                            pyautogui.keyUp('a' if direction == 'left' else 'd')
                    else:
                        distance = get_distance()
                        if distance is not None:
                            if distance < 20:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveRel(random.randint(50, 500), 0)
                                pyautogui.mouseUp(button='left')
                                distance = get_distance()  # Update distance
                                pyautogui.keyDown('a' if direction == 'left' else 'd')
                                time.sleep(2)  # Hold the key for a moment
                                pyautogui.keyUp('a' if direction == 'left' else 'd')
            else:
                # The speed is not below 10, so reset the timer
                speed_dropped_time = None
    else:
        print('both none')
        random_signals()
        random_motion()
        random_buff()
        random_shooting()

def enter_battle():
    if 'tan' in get_start().lower() or 'TAN' in get_start():
        print('Battle Start!')
        # first vehicle
        pyautogui.click(179, 1020)
        pyautogui.click(979, 127)

        # second vehicle
        pyautogui.click(354, 1020)
        pyautogui.click(979, 127)

        # third vehicle
        pyautogui.click(500, 1020)
        pyautogui.click(979, 127)

    elif 'use' in get_destroyed().lower():
        print('Back to Home!')
        pyautogui.press('esc')
        pyautogui.click(973, 490)
        pyautogui.click(x=1078, y=660)
        return
    elif 'ug' in get_end().lower():
        pyautogui.press('esc')
        return
    else:
        print('Taking Over!')
        detect_enemy()

# Continuously monitor and react
count = 0
while True:
    print(count)
    enter_battle()
    count += 1