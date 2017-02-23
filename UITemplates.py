from constants import *
from gamelogic import *
import globalvars as g
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label
from pyglet_gui.containers import VerticalContainer, Spacer
from pyglet_gui.buttons import Button
from pyglet_gui.constants import ANCHOR_TOP

class EscWindow(Manager):
    def __init__(self):
        quitButton = Button(label="Exit Game",on_press=self.quitGame)
        closeButton = Button(label="Return",on_press=self.close)
        Manager.__init__(self,
            Frame(VerticalContainer(content=[quitButton,closeButton])),
            window=g.gameEngine.window,
            batch=g.guiBatch,
            theme=g.theme,
            is_movable=False)
    def close(self,event):
        g.gameEngine.uiManager.closeEscWindow()
    def quitGame(self,event):
        g.gameEngine.uiManager.closeEscWindow()
        changeGameState(GAMESTATE_MENU)
        
class MenuWindow(Manager):
    def __init__(self):
        newgameButton=Button(label="New Game", on_press=self.newGame)
        quitButton=Button(label="Quit Game", on_press=self.quitGame)
        Manager.__init__(self,
            VerticalContainer(content=[newgameButton,Spacer(0,20),quitButton]),
            window=g.gameEngine.window,
            batch=g.guiBatch,
            theme=g.theme,
            is_movable=False)
    def newGame(self,event):
        initNewGame()
    def quitGame(self,event):
        exitGame()
        
class StatsWindow(Manager):
    coinsText=None
    def __init__(self):
        self.coinsText = Label("Coins: 0")
        Manager.__init__(self,
            self.coinsText,
            window=g.gameEngine.window,
            batch=g.guiBatch,
            theme=g.theme,
            is_movable=False,
            anchor=ANCHOR_TOP,
            offset=(0,-25))
    def updateCoinText(self,coinAmount):
        self.coinsText.set_text("Coins: %s" % str(coinAmount))