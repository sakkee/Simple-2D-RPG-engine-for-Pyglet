import pyglet.sprite
import pyglet.resource
import globalvars as g
from constants import *
from objects import *
from gamelogic import *
from PIL import Image
import json

class MenuScreen:
    images=[]
    def openMenuScreen(self):
        g.gameEngine.musicManager.playMusic("title_screen")
        bgImage = pyglet.resource.image(IMAGEFOLDER+'menu_background.jpg')
        bgImage.width, bgImage.height=g.gameEngine.SCREEN_RESOLUTION
        self.images.append(pyglet.sprite.Sprite(bgImage,x=0,y=0,batch=g.screenBatch))
        g.gameEngine.uiManager.initStartUI()
    def closeMenuScreen(self):
        for sprite in self.images:
            sprite.delete()
        self.images[:]=[]
        g.gameEngine.uiManager.closeStartUI()
        
class IngameScreen:
    mapbaseImage=None
    mapfringeImage=None
    myPlayer=None
    coinBatch=pyglet.graphics.Batch()
    NPCs=[]
    coins=[]
    mapOffsetX=0
    mapOffsetY=0
    tilesets={}
    Map=[]
    mapWidth=0
    mapHeight=0
    def openIngameScreen(self,mapname):
        self.LoadMap(mapname)
        g.gameEngine.uiManager.initStatsWindow()
    def LoadMap(self,mapname):
        self.mapbaseImage, self.mapfringeImage = loadMap(mapname, self.NPCs,self.coins)
        g.gameEngine.musicManager.playMusic("ingame")
    def UnloadMap(self):
        self.NPCs[:]=[]
        for coin in self.coins:
            coin.sprite.delete()
        self.coins[:]=[]
    def draw(self):
        self.mapbaseImage.blit(self.mapOffsetX,self.mapOffsetY)
        for npc in self.NPCs:
            blitPlayer(npc,myPlayer=False)
        blitPlayer(getMyPlayer(),myPlayer=True)
        self.coinBatch.draw()
        self.mapfringeImage.blit(self.mapOffsetX,self.mapOffsetY)
    def deleteCoin(self,coin):
        self.coins.remove(coin)