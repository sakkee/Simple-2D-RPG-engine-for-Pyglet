from constants import *

class TilesetClass:
    def __init__(self,tileset,gid,columns,tilecount):
        self.tileset = tileset
        self.gid=gid
        self.columns=columns
        self.tilecount=tilecount
        
class TileClass:
    def __init__(self,tileType=TILETYPE_WALK):
        self.tileType=tileType
        
class Coin:
    def __init__(self,sprite,x,y):
        self.sprite=sprite
        self.x=x
        self.y=y
    
class Player:
    def __init__(self,sprite,x=0,y=0,direction=DIR_DOWN, name=None):
        self.x=x
        self.y=y
        self.name=name
        self.facing=FACING[direction]["standing"]
        self.direction=direction
        self.sprite=sprite
        self.moving=False
        
        self.xOffset=0
        self.yOffset=0
        self.moveTick=0
        self.toStop=False
        self.stepChanged=False
        self.nextDir=direction
        
        
