from screenstateTemplates import MenuScreen, IngameScreen

class ScreenManager:
    menuScreen=None
    ingameScreen=None
    def __init__(self):
        self.menuScreen=MenuScreen()
        self.ingameScreen=IngameScreen()
    def openMenuScreen(self):
        self.menuScreen.openMenuScreen()
    def closeMenuScreen(self):
        self.menuScreen.closeMenuScreen()
    def openIngameScreen(self,mapname):
        self.ingameScreen.openIngameScreen(mapname)
        