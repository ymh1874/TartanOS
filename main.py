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

    # initialize mode manager
    app.modeManager = ModeManager(app)

    # initialize UI components
    app.terminal = Terminal(app)
    app.desktop = Desktop(app)
    app.loginPage = LoginPage(app)

    # start at login screen (stage 1)
    app.modeManager.setMode('login')


def redrawAll(app):
    # render current mode
    app.modeManager.redraw(app)


def onKeyPress(app, key, modifiers):
    # dispatch keyboard input to current mode
    app.modeManager.keyPress(app, key, modifiers)


def onMousePress(app, mouseX, mouseY):
    # dispatch mouse input to current mode
    app.modeManager.mousePress(app, mouseX, mouseY)


def onStep(app):
    # increment tick for cursor blinking
    app.tick += 1

runApp()
