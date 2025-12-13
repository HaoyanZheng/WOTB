import pyautogui

print("把鼠标移到目标位置，按 Enter 记录；输入 q 回车退出。")
while True:
    cmd = input()
    if cmd.strip().lower() == "q":
        break
    x, y = pyautogui.position()
    print(f"Captured: ({x}, {y})")




