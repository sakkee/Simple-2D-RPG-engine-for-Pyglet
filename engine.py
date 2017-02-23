import pyglet
from gamelogic import *
from constants import *
from spritemanager import SpriteManager
from screenManager import ScreenManager
from musicManager import MusicManager
import globalvars as g
import time
import UIManager

class Window(pyglet.window.Window):
    def __init__(self, engine):
        super().__init__(vsync=False)
        self.engine=engine
    def on_key_release(self,symbol,modifiers):
        if self.engine.gameState==GAMESTATE_INGAME:
            if symbol in MOVEBINDINGS and MOVEBINDINGS[symbol]==getMyPlayer().nextDir:
                stopMove(getMyPlayer(),MOVEBINDINGS[symbol])
    def on_key_press(self,symbol,modifiers):
        if self.engine.gameState==GAMESTATE_INGAME:
            if symbol in MOVEBINDINGS:
                move(MOVEBINDINGS[symbol],getMyPlayer())
            elif symbol == OPEN_ESC_WINDOW:
                self.engine.uiManager.openEscWindow()
                return True
    def on_draw(self):
        self.clear()
        drawGraphics()
        self.engine.fps_display.draw()
        
class Engine:
    current_millitime = lambda self: int(round(time.time() * 1000))
    fps_display = pyglet.clock.ClockDisplay()
    gameTick=0
    gameState=None
    screenManager=None
    musicManager=None
    uiManager=None
    spriteManager=None
    def update(self, dt):
        self.gameTick = self.current_millitime()
        if self.gameState==GAMESTATE_INGAME:
            checkPlayerMovements()
            calculateMapOffset()
            positionCoins()
    def initGame(self):
        self.window=Window(self)
        self.SCREEN_RESOLUTION = (self.window.width,self.window.height)
        initBatches()
        self.screenManager = ScreenManager()
        self.spriteManager = SpriteManager()
        self.musicManager = MusicManager()
        self.uiManager=UIManager.UIManager()
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        changeGameState(GAMESTATE_MENU)
    
g.gameEngine = Engine()
g.gameEngine.initGame()
pyglet.clock.schedule(g.gameEngine.update)
pyglet.app.run()