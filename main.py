# main.py - TartanOS
from cmu_graphics import *
from systems.fileSystem import FileSystem
from systems.userAuth import UserAuth
from core.appModes import ModeManager
from ui.terminal.terminal import Terminal
from ui.desktop.desktop import Desktop
from ui.loginPage.loginPage import LoginPage

def onAppStart(app):
    # initialize core systems
    app.fs = FileSystem()
    app.auth = UserAuth()
    app.tick = 0
    app.mouseX = 0
    app.mouseY = 0

    # initialize mode manager
    app.modeManager = ModeManager(app)

    app.terminal = Terminal(app)
    app.desktop = Desktop(app)
    app.loginPage = LoginPage(app)

    # start at login screen 
    app.modeManager.setMode('terminal')


def redrawAll(app):
    # render current mode
    app.modeManager.redraw(app)


def onKeyPress(app, key, modifiers):
    app.modeManager.keyPress(app, key, modifiers)

def onKeyHold(app, key, modifiers):
    app.modeManager.keyHold(app, key, modifiers)


def onMousePress(app, mouseX, mouseY):
    app.modeManager.mousePress(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    app.modeManager.mouseDrag(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    # track mouse position
    app.mouseX = mouseX
    app.mouseY = mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.modeManager.currentMode == 'desktop':
        app.desktop.windowManager.mouseRelease()


def onStep(app):
    # increment tick
    app.tick += 1

runApp()
