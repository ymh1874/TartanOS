# main.py
from cmu_graphics import *
from systems.fileSystem import FileSystem
from systems.userAuth import UserAuth
from core.appModes import ModeManager
from ui.terminal.terminal import Terminal
from ui.desktop.desktop import desktop

def onAppStart(app):
    app.fs = FileSystem()
    app.auth = UserAuth()
    app.tick = 0

    # Mode manager
    app.modeManager = ModeManager(app)

    # Terminal
    app.terminal = Terminal(app)
    
    # Desktop
    app.desktop = desktop(app)

    #Start in terminal mode
    app.modeManager.setMode('desktop')



def redrawAll(app):
    app.modeManager.redraw(app)

def onKeyPress(app, key, modifiers):
    app.modeManager.keyPress(app, key, modifiers)

def onStep(app):
    app.tick += 1

runApp()
