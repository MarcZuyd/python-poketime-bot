class ButtonCalibration:
    
    import pyautogui
    import FileHandler as handler
    import MouseInput as mouse

    fh = handler.FileHandler()
    m = mouse.MouseInput()

    def jsonButton(self, buttonName):
        button = {
            "button": buttonName,
            "coordinates": {
                "start": {
                    "x": self.m.selected[0][0], 
                    "y": self.m.selected[0][1]
                },
                "end"  : {
                    "x": self.m.selected[1][0], 
                    "y": self.m.selected[1][1]
                }
            }
        }

        return button


    def jsonPixel(self, pixelName, color):
        pixel = {
            "pixel": pixelName,
            "color": {
                "r": color[0],
                "g": color[1],
                "b": color[2]
            },
            "coordinates": {
                "x": self.m.selected[0][0],
                "y": self.m.selected[0][1]
            }
        }

        return pixel


    def setupMenu(self, menuItems, fileName):
        menuJson = []
        for item in menuItems:
            self.m.selected.clear()
            print("\nSelect {} button".format(item))
            self.m.startCapture()
            while self.m.selected[0] == self.m.selected[1]:
                self.m.selected.clear()
                print("\nSelect {} button".format(item))
                self.m.startCapture()
            menuJson.append(self.jsonButton(item))

        self.fh.writeJson(fileName, "\\coordinates\\pixels", menuJson) 


    def setupPixel(self, name):
        self.m.selected.clear()
        print("\nSelect {}".format(name))
        self.m.startCapture()
        pixelColor = self.pyautogui.pixel(self.m.selected[0][0], self.m.selected[0][1])
        print(pixelColor)
        self.fh.writeJson(name, "\\coordinates\\pixels", self.jsonPixel(name, pixelColor))
