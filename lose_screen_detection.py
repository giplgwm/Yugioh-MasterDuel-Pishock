import cv2
import pyautogui
import numpy as np


def at_lose_screen(thresh: float):
    lose_screen_comparison_img_path = 'img/yugioh_master_duel/lose.png'
    current_screen = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(current_screen), cv2.COLOR_RGB2BGR)
    lose_screen_template = cv2.imread(lose_screen_comparison_img_path)
    result = cv2.matchTemplate(screenshot, lose_screen_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= thresh)
    if len(list(zip(*loc[::-1]))) > 0:
        return True
    else:
        return False
