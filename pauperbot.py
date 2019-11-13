import pyautogui
import time
import random


def test():
    cursorPosition = pyautogui.position()
    screenSize = pyautogui.size()

    print("Cursor position: {} Screensize: {}".format(cursorPosition, screenSize))


def checkIfEncounter():
    encounter = False
    buttonGroup = pyautogui.locateOnScreen("buttonGroup.jpg", confidence=0.6)
    if buttonGroup:
        pyautogui.screenshot("knip.jpg", region=buttonGroup)
        encounter = True

    return encounter


def checkIfShiny():
    shiny = False
    s = pyautogui.locateOnScreen("shiny2.jpg", confidence=0.7)
    if s:
        pyautogui.screenshot("shinyCheck.jpg", region=s)
    p = pyautogui.pixel(36, 20)
    shinyPixel = pyautogui.pixelMatchesColor(36, 20, (255, 242, 0))
    if s or shinyPixel:
        shiny = True

    # print("Pixel color: {} Image: {} Shiny: {}".format(p, s, shinyPixel))

    return shiny


def pressRun():
    buttonGroup = pyautogui.locateOnScreen("buttonGroup.jpg", confidence=0.6)
    x = buttonGroup.left + buttonGroup.width - int(buttonGroup.width / 3.3)
    y = buttonGroup.top + int(buttonGroup.height / 1.5)
    randomX = random.randint(x, buttonGroup.left + buttonGroup.width)
    randomY = random.randint(y, buttonGroup.top + buttonGroup.height)
    pyautogui.click(randomX, randomY)
    time.sleep(2)


def walk(button, minStep, maxStep):
    for i in range(random.randint(minStep, maxStep)):
        pyautogui.press(button)
    

def hunt():
    shiny = False
    encounters = 0
    while shiny == False:
        walk("a", 5, 10)
        walk("d", 6, 10)
       
        if checkIfEncounter():
            encounters += 1
            if checkIfShiny():
                print("Shiny gevonden in {} encounters".format(encounters))
                shiny = True
            else:
                print("Encounter {}: geen shiny".format(encounters))
                pyautogui.screenshot("Zemmel{}.jpg".format(encounters))
                pressRun()
       

# Cursor position: Point(x=36, y=19) Screensize: Size(width=1920, height=1080)

time.sleep(3)
hunt()

