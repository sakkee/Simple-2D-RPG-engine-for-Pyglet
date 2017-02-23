import globalvars as g
from constants import *
from objects import *
from PIL import Image
import json
import pyglet
import random

def getTileTexture(tilevalue):
    for tilesetName,tileset in g.gameEngine.screenManager.ingameScreen.tilesets.items():
        if tilevalue>=tileset.gid and tilevalue<tileset.gid+tileset.tilecount:
            posX = ((tilevalue-tileset.gid)%tileset.columns)*TILEWIDTH
            posY = ((tilevalue-tileset.gid)//tileset.columns)*TILEWIDTH
            box = (posX, posY, posX + TILEWIDTH, posY + TILEWIDTH)
            return tileset.tileset.crop(box)

def loadMap(mapname, npcs, coins):
    with open(mapname) as data_file:    
        data = json.load(data_file)
        g.gameEngine.screenManager.ingameScreen.mapWidth=data["width"]
        g.gameEngine.screenManager.ingameScreen.mapHeight=data["height"]
        g.gameEngine.screenManager.ingameScreen.tilesets.clear()
        for tileset in data["tilesets"]:
            g.gameEngine.screenManager.ingameScreen.tilesets[tileset["image"]] = TilesetClass(Image.open(tileset["image"]),tileset["firstgid"],tileset["columns"],tileset["tilecount"])
        npcs[:]=[]
        coins[:]=[]
        tmpMapImage = Image.new("RGBA", (getMapWidth()*data["tilewidth"], getMapHeight()*data["tileheight"]))
        tmpMapFringe = Image.new("RGBA", (getMapWidth()*data["tilewidth"], getMapHeight()*data["tileheight"]))
        g.gameEngine.screenManager.ingameScreen.Map[:] = [[TileClass() for i in range(getMapHeight())] for i in range(getMapWidth())]
        for layer in data["layers"]:
            if layer["name"]=="NPCs":
                for npc in layer["objects"]:
                    npcs.append(loadPlayer(npc["properties"]["charsprite"], npc["properties"]["shirtsprite"], npc["properties"]["direction"], npc["x"]//TILEWIDTH, npc["y"]//TILEWIDTH, npc["properties"]["name"]))
            else:
                for i in range(len(layer["data"])):
                    X = i%getMapWidth()
                    Y = i//getMapWidth()
                    if layer["name"]=="Layer 1" or layer["name"]=="Layer 2" and layer["data"][i]!=0:
                        tileTexture = getTileTexture(layer["data"][i])
                        tmpMapImage.paste(tileTexture,(X*TILEWIDTH,Y*TILEWIDTH),tileTexture.convert('RGBA'))
                    elif layer["name"] =='Layer Fringe' and layer["data"][i]!=0:
                        tileTexture = getTileTexture(layer["data"][i])
                        tmpMapFringe.paste(tileTexture,(X*TILEWIDTH,Y*TILEWIDTH),tileTexture.convert('RGBA'))
                    elif layer["name"]=="Blocks":
                        if layer["data"][i]!=0:
                            g.gameEngine.screenManager.ingameScreen.Map[getMapHeight()-Y-1][X].tileType=TILETYPE_BLOCK
                    elif layer["name"]=="Coins":
                        if layer["data"][i]!=0:
                            g.gameEngine.screenManager.ingameScreen.Map[getMapHeight()-Y-1][X].tileType=TILETYPE_COIN
                            coins.append(Coin(pyglet.sprite.Sprite(g.gameEngine.spriteManager.coinAnimation,batch=g.gameEngine.screenManager.ingameScreen.coinBatch),X,Y))
        map = tmpMapImage.transpose(Image.FLIP_TOP_BOTTOM)
        raw_data = map.tobytes()
        fringeMap = tmpMapFringe.transpose(Image.FLIP_TOP_BOTTOM)
        raw_fringedata = fringeMap.tobytes()
        return pyglet.image.ImageData(getMapWidth()*data["tilewidth"],getMapHeight()*data["tileheight"],'RGBA',raw_data), pyglet.image.ImageData(getMapWidth()*data["tilewidth"],getMapHeight()*data["tileheight"],'RGBA',raw_fringedata)

def loadPlayer(charsprite, shirtsprite, direction, x, y, name):
    characterImage = Image.new("RGBA", (TILEWIDTH*SPRITECOLUMNS, TILEWIDTH), (0,0,0,0))
    characterSprite = g.gameEngine.spriteManager.getSprite('char',charsprite,SPRITECOLUMNS)
    shirtSprite = g.gameEngine.spriteManager.getSprite('shirt',shirtsprite,SPRITECOLUMNS)
    characterImage.paste(characterSprite,(0,0),characterSprite.convert('RGBA'))
    characterImage.paste(shirtSprite,(0,0),shirtSprite.convert('RGBA'))
    
    char_img_data = characterImage.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    charTmpImg = pyglet.image.ImageData(TILEWIDTH*SPRITECOLUMNS,TILEWIDTH,'RGBA',char_img_data)
    return Player(pyglet.image.ImageGrid(charTmpImg,1,SPRITECOLUMNS), x, y, direction, name)
    
def blitPlayer(player,myPlayer=False):
    if myPlayer:
        x = int((g.gameEngine.SCREEN_RESOLUTION[0]-TILEWIDTH)/2)
        y = int((g.gameEngine.SCREEN_RESOLUTION[1]-TILEWIDTH)/2)
    else:
        x = int((player.x-getMyPlayer().x)*TILEWIDTH+(g.gameEngine.SCREEN_RESOLUTION[0]-TILEWIDTH)/2+player.xOffset-getMyPlayer().xOffset)
        y = int((player.y-getMyPlayer().y)*TILEWIDTH+(g.gameEngine.SCREEN_RESOLUTION[1]-TILEWIDTH)/2+player.yOffset-getMyPlayer().yOffset)
    player.sprite[player.facing].blit(x,y)
    
def calculateMapOffset():
    g.gameEngine.screenManager.ingameScreen.mapOffsetX=int((g.gameEngine.SCREEN_RESOLUTION[0]-TILEWIDTH)/2-getMyPlayer().x*TILEWIDTH - getMyPlayer().xOffset)
    g.gameEngine.screenManager.ingameScreen.mapOffsetY=int((g.gameEngine.SCREEN_RESOLUTION[1]-TILEWIDTH)/2-getMyPlayer().y*TILEWIDTH - getMyPlayer().yOffset)
    
def positionCoins():
    for coin in g.gameEngine.screenManager.ingameScreen.coins:
        x = int((coin.x-getMyPlayer().x)*TILEWIDTH+(g.gameEngine.SCREEN_RESOLUTION[0]-TILEWIDTH)/2-getMyPlayer().xOffset)
        y = int((coin.y-getMyPlayer().y)*TILEWIDTH+(g.gameEngine.SCREEN_RESOLUTION[1]-TILEWIDTH)/2-getMyPlayer().yOffset)
        coin.sprite.set_position(x,y)
def getMyPlayer():
    return g.gameEngine.screenManager.ingameScreen.myPlayer
def getGameState():
    return g.gameEngine.gameState
def drawGraphics():
    if getGameState() == GAMESTATE_MENU:
        g.screenBatch.draw()
    elif getGameState() == GAMESTATE_INGAME:
        g.gameEngine.screenManager.ingameScreen.draw()
    
    if g.guiBatch:
        g.guiBatch.draw()

def checkPositionChange(direction):
    changeX = 0
    changeY = 0
    if direction == DIR_DOWN:
        changeY = -1
    elif direction == DIR_UP:
        changeY = 1
    elif direction == DIR_LEFT:
        changeX = -1
    elif direction == DIR_RIGHT:
        changeX = 1
    return [changeX,changeY]

def checkOffset(player):
    player.yOffset=0
    player.xOffset=0
    if player.moving:
        offset = TILEWIDTH - TILEWIDTH * (g.gameEngine.gameTick-player.moveTick)/MOVETIME
        if offset<=0:
            return
        if player.direction==DIR_UP:
            player.yOffset=-offset
        elif player.direction==DIR_DOWN:
            player.yOffset=+offset
        elif player.direction==DIR_LEFT:
            player.xOffset=+offset
        elif player.direction==DIR_RIGHT:
            player.xOffset=-offset
        
def move(direction,player):
    player.toStop=False
    player.nextDir=direction
    posChange = checkPositionChange(direction)
    
    if player.y+posChange[1]>=getMapHeight() or player.y+posChange[1] < 0 or player.x+posChange[0] >= getMapWidth() or player.x+posChange[0] < 0:
        stopMove(player,direction)
    elif g.gameEngine.screenManager.ingameScreen.Map[player.y+posChange[1]][player.x+posChange[0]].tileType==TILETYPE_BLOCK:
        stopMove(player,direction)
    
    elif not player.moving:
        player.direction=direction
        player.moveTick=g.gameEngine.gameTick
        player.facing=FACING[player.direction]["step_first"]
        player.moving=True
        player.x+=posChange[0]
        player.y+=posChange[1]
        checkOffset(player)
def getMapWidth():
    return g.gameEngine.screenManager.ingameScreen.mapWidth
def getMapHeight():
    return g.gameEngine.screenManager.ingameScreen.mapHeight
def stopMove(player,direction):
    player.toStop=True
    if not player.moving:
        player.direction=direction
        player.facing=FACING[player.direction]["standing"]
def checkPlayerMovement(player,NPC=False):
    if player.moving:
        checkOffset(player)
        if g.gameEngine.gameTick-player.moveTick>=MOVETIME:
            if not NPC:
                onTileEnter()
            player.moving=False
            player.stepChanged=False
            if NPC:
                player.toStop=True
            if player.toStop:
                player.facing=FACING[player.direction]["standing"]
            else:
                move(player.nextDir,player)
        elif not player.stepChanged and g.gameEngine.gameTick-player.moveTick>=MOVETIME/2:
            player.facing = FACING[player.direction]["step_second"]
            player.stepChanged=True
def checkPlayerMovements():
    processNpcMovements()
    checkPlayerMovement(getMyPlayer(),NPC=False)
    for npc in g.gameEngine.screenManager.ingameScreen.NPCs:
        checkPlayerMovement(npc,NPC=True)
        
def processNpcMovements():
    for npc in g.gameEngine.screenManager.ingameScreen.NPCs:
        if g.gameEngine.gameTick-npc.moveTick>=NPC_WALK_DELAY:
            direction = random.choice([DIR_DOWN,DIR_LEFT,DIR_UP,DIR_RIGHT])
            move(direction,npc)
            
def exitGame():
    pyglet.app.exit()

def initBatches():
    g.guiBatch = pyglet.graphics.Batch()
    g.screenBatch = pyglet.graphics.Batch()

def initNewGame():
    g.coins=0
    g.gameEngine.screenManager.ingameScreen.myPlayer = loadPlayer(DEFAULTCHARSPRITE,DEFAULTCHARSHIRT,START_DIRECTION,START_X,START_Y, "My Player")
    changeGameState(GAMESTATE_INGAME)
def unloadGame():
    g.gameEngine.uiManager.closeStatsWindow()
    g.gameEngine.screenManager.ingameScreen.UnloadMap()
    
def changeGameState(gamestate):
    if gamestate==GAMESTATE_MENU:
        g.gameEngine.screenManager.menuScreen.openMenuScreen()
    elif gamestate==GAMESTATE_INGAME:
        g.gameEngine.screenManager.openIngameScreen(DEFAULTMAP)
    if getGameState()==GAMESTATE_MENU:
        g.gameEngine.screenManager.menuScreen.closeMenuScreen()
    elif getGameState()==GAMESTATE_INGAME:
        unloadGame()
    g.gameEngine.gameState=gamestate
        
def getCoinOnPosition(x,y):
    for coin in g.gameEngine.screenManager.ingameScreen.coins:
        if coin.x == x and coin.y == y:
            return coin
    return None
def pickCoin(x,y):
    coin = getCoinOnPosition(getMyPlayer().x,getMyPlayer().y)
    if coin is not None:
        g.coins+=1
        coin.sprite.delete()
        g.gameEngine.screenManager.ingameScreen.deleteCoin(coin)
        g.gameEngine.musicManager.playSoundEffect("coin_pick")
        g.gameEngine.uiManager.statsWindow.updateCoinText(g.coins)
def onTileEnter():
    pickCoin(getMyPlayer().x,getMyPlayer().y)

    