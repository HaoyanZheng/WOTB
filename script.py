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
roi_start = (1574, 983, 40, 20)

# speed section in game
roi_speed = (690, 1050, 30, 20)

# first word when destroyed
roi_destroyed = (815, 1000, 98, 30)

# end_game screen
roi_end = (160, 50, 95, 30)

# distance
roi_distance = (1020, 560, 40, 10)

# energy tank list
roi_wait_start = (850, 420, 200, 100)


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

# 建议：减少 PyAutoGUI 自带延迟，让节奏更自然
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True  # 鼠标甩到左上角可中断（安全）

# 你已有的 hold_key
def hold_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def key_down(k: str):
    pyautogui.keyDown(k)

def key_up(k: str):
    pyautogui.keyUp(k)

def hold_keys(keys, duration: float):
    """同时按下多个键（例如 ['w','a']）持续 duration 秒"""
    for k in keys:
        key_down(k)
    try:
        time.sleep(duration)
    finally:
        # 反向抬起更稳一点
        for k in reversed(keys):
            key_up(k)

def tap_key(key: str, min_d=0.03, max_d=0.10):
    """短按一下（人类常见的“点按”）"""
    hold_key(key, random.uniform(min_d, max_d))

def human_duration(short=0.06, long=0.45):
    """
    右偏分布：大多数很短，偶尔稍长，更像人手微调节奏
    """
    x = random.lognormvariate(mu=-1.2, sigma=0.55)
    return max(short, min(long, x))

def forward_with_jitter(
    total_min=3, total_max=5,      # longer forward segments
    tick_min=0.06, tick_max=0.18,       # tighter cadence
    jitter_prob=0.35,                   # fewer lateral corrections
    left_bias=0.50,
    micro_pause_prob=0.00,              # IMPORTANT: never release W
):
    total = random.uniform(total_min, total_max)
    end_t = time.time() + total

    key_down('w')
    try:
        while time.time() < end_t:
            time.sleep(random.uniform(tick_min, tick_max))

            if random.random() > jitter_prob:
                continue

            side = 'a' if random.random() < left_bias else 'd'

            # IMPORTANT: keep lateral very short so net forward stays strong
            key_down(side)
            time.sleep(random.uniform(0.04, 0.16))   # was up to ~0.35
            key_up(side)

    finally:
        key_up('w')
        key_up('a')
        key_up('d')


def back_step():
    """短后退（避免卡住/像人在调整）"""
    hold_key('s', random.uniform(0.08, 0.45))

def strafe_only():
    """纯横移（不配W）偶尔发生，像人在躲/找角度"""
    hold_key(random.choice(['a', 'd']), random.uniform(0.10, 0.55))

def pause_idle():
    """短暂停（像人发呆/观察）"""
    time.sleep(random.uniform(0.08, 0.60))

def random_motion_human():
    """
    一次“动作片段”：用权重控制行为分布
    你可以根据实际体验调整权重。
    """
    actions = [
        ("forward_jitter", 0.90),
        ("wa",             0.05),
        ("wd",             0.05),
        ("pause",          0.00),  # or 0.01 if you really want it
        ("back",           0.00),  # or 0.01
        ("strafe",         0.00),  # or 0.01
    ]

    names, weights = zip(*actions)
    act = random.choices(names, weights, k=1)[0]

    if act == "forward_jitter":
        forward_with_jitter()
    elif act == "wa":
        hold_keys(['w', 'a'], random.uniform(1, 2))
    elif act == "wd":
        hold_keys(['w', 'd'], random.uniform(1, 2))
    elif act == "pause":
        pause_idle()
    elif act == "back":
        back_step()
    else:
        strafe_only()

def motion_loop(run_seconds=None):
    """
    持续执行 motion。
    - run_seconds=None 表示一直跑
    - 提示：PyAutoGUI FAILSAFE 开着，鼠标甩到左上角可强制中断
    """
    start = time.time()
    try:
        while True:
            if run_seconds is not None and (time.time() - start) >= run_seconds:
                break
            random_motion_human()
    finally:
        # 无论如何都抬起这些常用键，防止卡键
        for k in ['w', 'a', 's', 'd']:
            try:
                key_up(k)
            except Exception:
                pass


def random_shooting():
    # Define the probability of shooting
    shoot_probability = 0.5
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
        random_motion_human()
        random_buff()
        random_shooting()

def enter_battle():
    if 'tan' in get_start().lower() or 'TAN' in get_start():
        print('Battle Start!')
        # first vehicle
        pyautogui.click(179, 1020)
        time.sleep(0.2)
        pyautogui.click(979, 127)

        # second vehicle
        time.sleep(0.2)
        pyautogui.click(354, 1020)
        time.sleep(0.2)
        pyautogui.click(979, 127)

        # third vehicle
        time.sleep(0.2)
        pyautogui.click(500, 1020)
        time.sleep(0.2)
        pyautogui.click(979, 127)

    elif 'fu' in get_destroyed().lower():
        print('Back to Home!')
        pyautogui.press('esc')
        time.sleep(1)
        pyautogui.click(983, 490)
        time.sleep(1)
        pyautogui.click(1104, 651)
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