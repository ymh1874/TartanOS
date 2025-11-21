from cmu_graphics import *


class OnScreenKeyboard:
    def __init__(self, app):
        # store app and compute keyboard bounds relative to the window
        self.app = app
        self.boardX =  0.45 * app.width
        self.boardY = 0.623 * app.height
        self.boardW = 0.485 * app.width
        self.boardH = 0.19 * app.height
        # first-row keys (commas required!)
        self.keyRow1 = ['ESC', '1', '2', '3', '4', '5', '6', '7',
                        '8', '9', '0', '-', '=', 'BACK']
        self.row1 = 0
    def keyboardDraw(self, app):
        self.boardX =  0.45 * app.width
        self.boardY = 0.63 * app.height
        self.boardW = 0.485 * app.width
        self.boardH = 0.19 * app.height
        self.row1 = (self.boardW - self.boardX) // 15
        drawRect(self.boardX, self.boardY, app.width, app.height, fill = 'red')
        for i in range(len(self.keyRow1)):

            drawRect(self.boardX + (i * self.row1), self.boardY, 20, 20, fill = None, border = 'black')
            drawLabel(self.keyRow1[i],self.boardX + (i * self.row1) // 2 + 10, self.boardY // 2 + 10, size = 20, fill = 'purple' )


    def onKeyPressKeyboard(self, app, key, modifiers):
        app.terminal.onKeyPress(app, key, modifiers)
