from cmu_graphics import *
from core.appModes import ModeManager
from ui.desktop.onScreenKeyboard import OnScreenKeyboard

class desktop():
    def __init__(self, app):
        self.app = app
        # instantiate keyboard with app so it can compute sizes
        self.keyboard = OnScreenKeyboard(app)
        self.backgroundColor = './assets/desktopBackground.png'
        self.terminalIcon = 'assets/terminalIcon.png'
        self.folderIcon = 'assets/folderIcon.png'
        self.rectHighlight = True

       

    def draw(self, app):
        # background
        drawRect(0,0, app.width, app.height, fill = 'green')
        # keyboard
        self.keyboard.keyboardDraw(app)
    
    
    def onKeyPress(self, app, key, modifiers):
        self.keyboard.onKeyPressKeyboard(app, key, modifiers)
        if modifiers == ['control'] and key == 't':
            self.app.modeManager.setMode('terminal')
        elif modifiers == ['control'] and key == 'l':
            app.screen = 'loginPage'
        

    def onMouseDragDesktop(self, app, mouseX, mouseY):
        if not self.rectHighlight:
            return
        # original cursor position
        ogX = mouseX
        ogY = mouseY

        self.rectangleHighlight(mouseX, mouseY, ogX, ogY)

    def rectangleHighlight(self, mouseX, mouseY, ogX, ogY):
        drawRect(ogX, ogY, mouseX, mouseY, fill=None, border='white', borderWidth=4, opacity=100)

    