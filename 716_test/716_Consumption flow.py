#! usr/bin/python3

import pyautogui

screenwidth, screenhight = pyautogui.size()
mouseX, mouseY = pyautogui.position()

pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

w, h = pyautogui.size()
pyautogui.moveTo(w/2, h/2)
pyautogui.moveTo(100, 100, duration=2)
pyautogui.moveTo(None, 500)

pyautogui.moveRel(-40, 500)

pyautogui.click(100, 400, button='right')
pyautogui.click(clicks=2, interval=0.25)