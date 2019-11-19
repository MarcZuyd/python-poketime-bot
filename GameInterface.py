import FileHandler as handler

class GameInterface:

    fh = handler.FileHandler()

    walkButtons = [["left", "right"], ["up", "down"]]
    gameInterface = [
        ["loginMenu", ["Username", "Password", "Login"]],
        ["battleMenu", ["Fight", "Pokemon", "Items", "Run"]],
        ["itemMenu", ["PokeballTab", "GreatBall"]],
        ["chatMenu", ["General", "Battle", "Trade", "Global"]],
        ["gameMenu", ["Toggle", "Return", "Logout", "Exit"]],
        ["emoteMenu", ["Toggle", "Heart", "Sleep", "Thumbsup", "Sjpiener", "Sunglasses"]],
    ]
    pixels = [["avatarPixel"], ["battleMenuPixel"], ["loginPixel"], ["shinyPixel"], ["hpBarPixel"]]


    def __init__(self):
        print("\nP O K E T I M E  M O R E  P O W E R\n")
        print("\nImporting game interface\n"+"_"*28)
        self.setCoordinates(self.gameInterface, "menus")
        print("\nImporting pixels\n"+"_"*28)
        self.setCoordinates(self.pixels, "pixels")


    def setCoordinates(self, interface, folder):
        for i in interface:
            i.append(self.fh.readJson(i[0], "\\coordinates\\{}".format(folder)))


# inter = GameInterface()
# inter.setMenuCoordinates()
# inter.setPixelCoordinates()

