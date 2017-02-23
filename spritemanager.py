from PIL import Image
from constants import *
import pyglet
class SpriteManager:
    def __init__(self):
        self.characterSprite = Image.open(IMAGEFOLDER+'char.png')
        self.shirtSprite = Image.open(IMAGEFOLDER+'shirt.png')
        coinRes = pyglet.resource.image(IMAGEFOLDER+'coin_gold.png')
        coinGrid = pyglet.image.ImageGrid(coinRes, coinRes.height//TILEWIDTH, coinRes.width//TILEWIDTH, TILEWIDTH, TILEWIDTH)
        self.coinAnimation = pyglet.image.Animation.from_image_sequence(coinGrid.get_texture_sequence(), 0.2, True )
    def getSprite(self,spritetype,spritevalue,spritecolumns):
        box = (0,spritevalue*TILEWIDTH,spritecolumns*TILEWIDTH,(spritevalue+1)*TILEWIDTH)
        if spritetype == "char":
            return self.characterSprite.crop(box)
        elif spritetype=='shirt':
            return self.shirtSprite.crop(box)