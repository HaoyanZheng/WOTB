import pyautogui
import pytesseract

# Take a screenshot of the entire screen
screenshot = pyautogui.screenshot(region=(700, 980, 250, 40))

# Use pytesseract to perform OCR on the screenshot
text = pytesseract.image_to_string(screenshot)

# Print the resulting text
print(text)
