# main.py - entry point for the application
# responsible for initializing core systems and managing app modes
# uses cmu_graphics for rendering and input handling
from cmu_graphics import *
from systems.commandRegistry import CommandRegistry
from systems.fileSystem import FileSystem
from systems.pathUtils import PathUtils
from systems.userAuth import UserAuth
from core.appModes import ModeManager
from systems.windowManager import WindowManager
from ui.clientRender import ClientRender
from ui.terminal.terminal import Terminal, NanoEditor
from ui.fileExplorer import FileExplorer
from ui.desktop.desktop import Desktop
from ui.loginPage.loginPage import LoginPage

def onAppStart(app):
    # initialize core systems
    app.fs = FileSystem()
    app.auth = UserAuth()
    app.windowManager = WindowManager(app)
    app.clientRender = ClientRender(app)
    app.modeManager = ModeManager(app)
    app.cmdRegistry = CommandRegistry(app)
    app.pathUtils = PathUtils()
    app.tick = 0
    app.mouseX = 0
    app.mouseY = 0

    # store class references for  instantiation
    app.Terminal = Terminal
    app.NanoEditor = NanoEditor
    app.FileExplorer = FileExplorer
    app.PathUtils = PathUtils

    # initialize mode manager
    app.modeManager = ModeManager(app)

    app.terminal = Terminal(app)
    app.desktop = Desktop(app)
    app.loginPage = LoginPage(app)

    # set terminal reference in command registry so commands have access to currPath, fs, etc
    app.cmdRegistry.term = app.terminal

    # start at login screen 
    app.modeManager.setMode('login')

def redrawAll(app):
    # render current mode
    app.modeManager.redraw(app)


def onKeyPress(app, key, modifiers): 
    app.modeManager.keyPress(app, key, modifiers)


def onMousePress(app, mouseX, mouseY):
    app.modeManager.mousePress(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    app.modeManager.mouseDrag(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.modeManager.currentMode == 'desktop':
        app.desktop.windowManager.mouseRelease()


def onStep(app):
    # increment tick
    app.tick += 1

runApp()
