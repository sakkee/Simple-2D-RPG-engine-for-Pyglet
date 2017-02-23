from constants import *
from gamelogic import *
import globalvars as g

from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame
from pyglet_gui.containers import VerticalContainer
import pyglet_gui.theme
import pyglet.graphics
import UITemplates

class UIManager():
    states = []
    escWindow=None
    menuWindow=None
    statsWindow=None
    def __init__(self):
        g.theme =  pyglet_gui.theme.ThemeFromPath('theme')
    
    def initStartUI(self):
        if MENUWINDOW_OPENED not in self.states:
            self.states.append(MENUWINDOW_OPENED)
            self.menuWindow=UITemplates.MenuWindow()
    def closeStartUI(self):
        if MENUWINDOW_OPENED in self.states:
            self.states.remove(MENUWINDOW_OPENED)
            self.menuWindow.delete()
    def initStatsWindow(self):
        if STATSWINDOW_OPENED not in self.states:
            self.states.append(STATSWINDOW_OPENED)
            self.statsWindow = UITemplates.StatsWindow()
    def closeStatsWindow(self):
        if STATSWINDOW_OPENED in self.states:
            self.states.remove(STATSWINDOW_OPENED)
            self.statsWindow.delete()
    def openEscWindow(self):
        if ESCWINDOW_OPENED in self.states:
            self.closeEscWindow()
            return
        self.states.append(ESCWINDOW_OPENED)
        self.escWindow=UITemplates.EscWindow()
    def closeEscWindow(self):
        if ESCWINDOW_OPENED not in self.states:
            return
        self.states.remove(ESCWINDOW_OPENED)
        self.escWindow.delete()