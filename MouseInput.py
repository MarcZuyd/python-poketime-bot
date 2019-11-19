class MouseInput:

    from pynput import mouse

    selected = []


    def isUnique(self):
        if self.selected[0] == self.selected[1]:
            return True
        else:
            return False


    def on_move(self, x, y):
        print("Pointer moved to {0}".format((x, y)))


    def on_click(self, x, y, button, pressed):

        self.selected.append([x, y])
        
        print("{0} : {1}".format(
            "Top-left    " if pressed else "Bottom-right", (x, y))
            )
        if not pressed:
            # Stop listener
            return False


    def on_scroll(self, x, y, dx, dy):
        print("Scrolled {0} at {1}".format(
            "down" if dy < 0 else "up", (x, y))
            )


    def startCapture(self):
        # Collect events until released
        with self.mouse.Listener(
                on_click=self.on_click,
            ) as listener:
            listener.join()

