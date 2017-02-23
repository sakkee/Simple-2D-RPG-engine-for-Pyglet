import pyglet.window.key

DEFAULTMAP='examplemap.json'
IMAGEFOLDER='images/'
SOUNDFOLDER='sounds/'

TILETYPE_WALK=0
TILETYPE_BLOCK=1
TILETYPE_COIN=2

TILEWIDTH=32

DEFAULTCHARSPRITE=0
DEFAULTCHARSHIRT=1
SPRITECOLUMNS=10

DIR_DOWN=0
DIR_RIGHT=1
DIR_UP=2
DIR_LEFT=3

FACING = {
    DIR_DOWN: {"standing":0, "step_first":1, "step_second":2},
    DIR_RIGHT: {"standing":3, "step_first": 4, "step_second": 3},
    DIR_UP: {"standing":5, "step_first":6, "step_second": 7},
    DIR_LEFT: {"standing":8, "step_first":9, "step_second": 8}
}

START_DIRECTION=DIR_DOWN
START_X=4
START_Y=5

MOVETIME=640 #millisekunneissa

MOVE_DOWN=pyglet.window.key.S
MOVE_LEFT=pyglet.window.key.A
MOVE_RIGHT=pyglet.window.key.D
MOVE_UP=pyglet.window.key.W
OPEN_ESC_WINDOW=pyglet.window.key.ESCAPE

MOVEBINDINGS = {
    MOVE_DOWN : DIR_DOWN,
    MOVE_LEFT : DIR_LEFT,
    MOVE_UP : DIR_UP,
    MOVE_RIGHT : DIR_RIGHT
}

NPC_WALK_DELAY=5000 #millisekuntteja

ESCWINDOW_OPENED=1
MENUWINDOW_OPENED=2
STATSWINDOW_OPENED=3

GAMESTATE_INGAME=0
GAMESTATE_MENU=1

SOUNDEFFECTNAMES = {
    "coin_pick":"coin_pick.mp3"
}
MUSICNAMES = {
    "title_screen":"menumusic.mp3",
    "ingame":"forest.mp3"
}