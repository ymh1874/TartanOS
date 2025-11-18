from cmu_graphics import *

class desktop():
    def __init__(self, app):
        self.backgroundColor = 'assets/desktopBackground.png'
        self.terminalIcon = 'assets/terminalIcon.png'
        self.folderIcon = 'assets/folderIcon.png'
        self.rectHighlight = True

    def draw(self, app):
        drawImage(self.backgroundColor, 0, 0, width=app.width, height=app.height)
        drawImage(self.terminalIcon, 50, 50, width=64, height=64)
        drawImage(self.folderIcon, 150, 50, width=64, height=64)
    

    def onKeyPressDesktop(self, app, key, modifiers):
        if modifiers == ['control'] and key == 't':
            app.screen = 'terminal'
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

    