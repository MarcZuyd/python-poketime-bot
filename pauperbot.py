import pyautogui
import time
import datetime
import random
import json
import MouseInput as mouse
import FileHandler as handler
import ButtonCalibration as calibration
import GameInterface as interface
from pyautogui import FailSafeException

class PauperBot:

    fh = handler.FileHandler()
    mouse = mouse.MouseInput()
    ui = interface.GameInterface()

    encounters = 0
    totalEncounters = 0
    shinyEncounters = 0
    shinyTime = 0
    sessionStart = 0

    save = ""

    def test(self):
        cursorPosition = pyautogui.position()
        screenSize = pyautogui.size()

        print("Cursor position: {} Screensize: {}".format(cursorPosition, screenSize))


    def typeinChat(self, text):
        pyautogui.typewrite("\n{}\n".format(text), interval=0.09)


    def humanizer(self):
        roll = random.randint(1, 10000)
        if roll <= 100:
            delay = random.randint(5, 180)
            print("\nAFK for {} seconds, BRB!!\n".format(delay))
            time.sleep(delay)
        elif roll == 9999:
            self.typeinChat("I love this game guys!")


    def getGameState(self):
        gameState = False
        while not gameState:
            # print(gameState)
            if self.checkFixedPixel("avatarPixel"):
                gameState = True
                return "hunting"
            elif self.checkFixedPixel("hpBarPixel"):
                gameState = True
                return "encounter"
            elif self.checkFixedPixel("loginPixel"):
                gameState = True
                return "disconnected"
            time.sleep(1)


    def getPixelData(self, pixelName, pixels):
        for pixel in pixels:
            if pixel[0] == pixelName:
                return pixel[1]


    def menuClick(self, button, interface):
        for menu in interface:
            for menuItem in menu[2]:
                if menuItem["button"] == button:
                    startX = menuItem["coordinates"]["start"]["x"]
                    startY = menuItem["coordinates"]["start"]["y"]
                    endX   = menuItem["coordinates"]["end"]["x"]
                    endY   = menuItem["coordinates"]["end"]["y"]
                    randomX = random.randint(startX, endX)
                    randomY = random.randint(startY, endY)
                    # print(randomX, randomY)
                    pyautogui.click(randomX, randomY)
        time.sleep(random.randint(50, 90) / 100)


    def walkSteps(self, button, minStep, maxStep):
        for i in range(random.randint(minStep, maxStep)):
            pyautogui.keyDown(button)
            time.sleep(0.1)
            pyautogui.keyUp(button)


    def walkSeconds(self, button, seconds):
        # print("Button {}\t{} seconds".format(button, seconds))
        pyautogui.keyDown(button)
        time.sleep(seconds)
        pyautogui.keyUp(button)


    def walkRoute(self, route):
        for direction in route:
            print(direction[0])
            if direction[0] == "delay":
                time.sleep(float(direction[1]))
            else:
                self.walkSeconds(direction[0], float(direction[1]))


    def waitForPixel(self, pixelName):
        pixel = False
        while not pixel:
            self.checkIfDisconnected()
            print("Searching for {}".format(pixelName))
            if self.checkFixedPixel(pixelName):
                pixel = True
            time.sleep(0.5)


    def checkFixedPixel(self, pixelName):
        pixelReference = self.getPixelData(pixelName, self.ui.pixels)
        xRef = pixelReference["coordinates"]["x"]
        yRef = pixelReference["coordinates"]["y"]
        rgbRef = (pixelReference["color"]["r"], pixelReference["color"]["g"], pixelReference["color"]["b"]) 
        detectedPixelColor = pyautogui.pixel(xRef, yRef)
        # print("Detected {} color: {} x:{} y:{}".format(pixelName, detectedPixelColor, xRef, yRef))
        pixelMatch = pyautogui.pixelMatchesColor(xRef, yRef, rgbRef, tolerance=20)

        return pixelMatch


    def loadSaveFile(self):
        print("\nLoading save file\n"+"_"*28)
        save = self.fh.readJson("save", "")
        print(" | Encounters:\t{}\n | Shinies:\t{}\n | Runtime:\t{}\n | Last shiny:\t{}"
        .format(save["encounters"], save["shinyEncounters"], datetime.timedelta(seconds=save["runTime"]), save["lastShinyDate"])
        )

        return save


    def saveProgress(self):
        save = {
            "encounters": self.totalEncounters,
            "shinyEncounters": self.shinyEncounters,
            "lastShinyDate": self.shinyTime,
            "runTime": self.save["runTime"] + (time.time() - self.sessionStart)
        }

        self.fh.writeJson("save", "", save)


    def idle(self):
        while True:
            time.sleep(random.random(75, 550))
            self.checkIfDisconnected()


    def autocatch(self):
        encounter = True
        while encounter:
            print("Catching pokemon!")
            time.sleep(1)
            self.menuClick("Items", self.ui.gameInterface)
            time.sleep(1)
            self.menuClick("PokeballTab", self.ui.gameInterface)
            time.sleep(1)
            self.menuClick("GreatBall", self.ui.gameInterface)
            time.sleep(13)

            state = self.getGameState()
            print(state)
            if state != "encounter":
                encounter = False


    def login(self):
        time.sleep(1)
        print("Log in")
        self.menuClick("Login", self.ui.gameInterface)
        time.sleep(1)


    def checkIfDisconnected(self):
        if self.checkFixedPixel("loginPixel"):
            print("\nDisconnected")
            self.login()


    def randomDirection(self):
        direction = random.randint(1, 100)
        if direction > 50:
            return 1
        else:
            return 0


    def hunt(self, direction):
        time.sleep(3)
        self.save = self.loadSaveFile()
        shiny = False
        self.totalEncounters = self.save["encounters"]
        self.sessionStart = time.time()
        print("\nStart the hunt!\n"+"_"*28)
        while shiny == False:
                    
            gameState = self.getGameState()
            if gameState == "hunting":

                button = random.randint(0, 1)
                seconds = random.randint(150, 400) / 1000
                self.walkSeconds(self.ui.walkButtons[direction][self.randomDirection()], seconds)

            elif gameState == "encounter":
                # print("\nEncounter check")
                self.encounters += 1
                self.totalEncounters += 1
                pyautogui.screenshot("Zemmel{}.jpg".format(self.encounters))
                if self.checkFixedPixel("shinyPixel"):
                    print("Shiny gevonden in {} encounters".format(self.encounters))
                    # self.idle()
                    self.autocatch()
                    shiny = True
                else:
                    print("Encounter {}: geen shiny".format(self.encounters))
                    
                    time.sleep(0.5)
                    self.menuClick("Run", self.ui.gameInterface)
                    time.sleep(1.5)
                    self.humanizer()
            
            elif gameState == "disconnected":
                self.login()



if __name__ == "__main__":

    try:
        # cali = calibration.ButtonCalibration()
        # cali.setupPixel("hpBarPixel")
        # time.sleep(100)
        bot = PauperBot()
        bot.hunt(0)
    except FailSafeException:
        print("\nPyAutoGUI fail-safe triggered from mouse moving to a corner of the screen.")
    except KeyboardInterrupt:
        print("\nUser shutdown.")

    print("\nTotal encounters {}  encounters {}".format(bot.totalEncounters, bot.encounters))
    bot.saveProgress()


# fh = handler.FileHandler()
# cali = calibration.ButtonCalibration()
# route = readRoute()
# walkRoute(route)
# time.sleep(2)
# hunt(walkButtons[0])
# cali.setupMenu(["Username", "Password", "Login"], "loginMenu")
# cali.setupMenu(["General", "Battle", "Trade", "Global"], "chatMenu")
# cali.setupMenu(["Toggle", "Return", "Logout", "Exit"], "gameMenu")
# cali.setupMenu(["PokeballTab", "GreatBall"], "itemMenu")
# cali.setupPixel("loginPixel")
# menuClick("Toggle", "emoteMenu")
# time.sleep(0.47)
# menuClick("Thumbsup", "emoteMenu")

# Pixel color: (240, 192, 0) Image: None Shiny: True
# autocatch
# safarizone
# Cursor position: Point(x=36, y=19) Screensize: Size(width=1920, height=1080)