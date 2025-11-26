from cmu_graphics import *
from systems.windowManager import WindowManager
class Desktop():
    def __init__(self, app):
        self.app = app
        self.bgColor = rgb(80, 90, 100)  # fallback background color
        self.backgroundImage = 'assets/backgrounds/desktopBackground.png'
        self.fileIcon = 'assets/icons/fileIcon.png'
        self.folderIcon = 'assets/icons/folderIcon.png'
        self.terminalOpen = False
        self.filesDisplayed = [] #list of files currently shown on desktop
        self.windowManager = WindowManager(app)

    def draw(self, app):
        # draw desktop background image
        try:
            drawImage(self.backgroundImage, 0, 0, width=app.width, height=app.height)
        except:
            # fallback to solid color if image not found
            drawRect(0, 0, app.width, app.height, fill=self.bgColor)
        self.drawFiles(app)
        self.windowManager.drawWindows(app, app.mouseX, app.mouseY)

    def drawFiles(self, app):
        # draw desktop icons for files and folders
        iconSize = max(50, int(app.width * 0.07))
        padding = iconSize * 0.3
        startX = padding
        startY = padding + 50  # leave space for title bar

        x = startX
        y = startY

        self.filesDisplayed = []
        for file in app.fs.getDesktopFiles():    
            # draw icon (placeholder rectangle for now)
            if file[1] == 'folder':
                drawImage(self.folderIcon, x, y, width=iconSize, height=iconSize)
            elif file[1] == 'file':
                drawImage(self.fileIcon, x, y, width=iconSize, height=iconSize)
            # draw filename
            drawLabel(file[0], x + iconSize / 2, y + iconSize + 15, size=12, align='center', fill='black')

            # store displayed file info for click detection
            self.filesDisplayed.append((file, x, y, iconSize, iconSize + 15))

            # update position for next icon
            x += iconSize + padding
            if x + iconSize > app.width:
                x = startX
                y += iconSize + padding + 15
            
    
    
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

    def onMousePress(self, app, mouseX, mouseY):
        # check if a desktop icon was clicked
        for fileInfo in self.filesDisplayed:
            file, x, y, w, h = fileInfo
            if (x <= mouseX <= x + w) and (y <= mouseY <= y + h):
                self.windowManager.openWindow(file[0], app)
                print(f"Clicked on {file[0]}")
    
    def mouseDrag(self, app, mouseX, mouseY):
        WindowManager.mouseDragWindow(app, mouseX, mouseY)
                          

    