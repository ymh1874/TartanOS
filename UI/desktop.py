from cmu_graphics import *

class desktop():
    def __init__(self, app):
        self.backgroundColor = 'assets/desktopBackground.png'
        self.terminalIcon = 'assets/terminalIcon.png'
        self.folderIcon = 'assets/folderIcon.png'

    def draw(self, app):
        drawImage(self.backgroundColor, 0, 0, width=app.width, height=app.height)
        drawImage(self.terminalIcon, 50, 50, width=64, height=64)
        drawImage(self.folderIcon, 150, 50, width=64, height=64)
    

    def onKeyPressDesktop(self, app, key, modifiers):
        if modifiers == ['control'] and key == 't':
            app.screen = 'terminal'