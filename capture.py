import pyautogui
import cv2
import numpy as np

roi =  (160, 50, 95, 30) # (left, top, width, height)

img_pil = pyautogui.screenshot(region=roi)
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

cv2.imshow("ROI Preview", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
