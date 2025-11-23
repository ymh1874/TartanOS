from cmu_graphics import *

class Desktop():
    def __init__(self, app):
        self.app = app
        self.bgColor = rgb(80, 90, 100)  # fallback background color
        self.backgroundImage = 'assets/backgrounds/desktopBackground.png'
        self.terminalOpen = False
        self.filesDisplayed = [] # not implemented yet

    def draw(self, app):
        # draw desktop background image
        try:
            drawImage(self.backgroundImage, 0, 0, width=app.width, height=app.height)
        except:
            # fallback to solid color if image not found
            drawRect(0, 0, app.width, app.height, fill=self.bgColor)
    
    def drawFiles(self, app):
        # draw desktop icons for files and folders
        iconSize = max(50, int(app.width * 0.07))
        padding = iconSize * 0.3
        startX = padding
        startY = padding + 50  # leave space for title bar

        x = startX
        y = startY

        self.filesDisplayed = []
        pass
        

        
    
    def onKeyPress(self, app, key, modifiers):
        # ctrl+t to toggle terminal mode
        if modifiers == ['control'] and key == 't':
            if self.terminalOpen:
                # close terminal, go back to desktop
                self.terminalOpen = False
                self.app.modeManager.setMode('desktop')
            else:
                # open terminal
                self.terminalOpen = True
                self.app.modeManager.setMode('terminal')

    