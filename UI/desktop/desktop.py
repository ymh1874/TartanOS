# ui/desktop/desktop.py - Desktop UI component
# displays desktop background, icons, and manages windows
# allows launching applications from desktop icons
from cmu_graphics import *
from UI.desktop.clockDate import ClockDate
class Desktop():
    def __init__(self, app):
        self.app = app
        
        self.bgColor = rgb(80, 90, 100)  # fallback background color
        self.backgroundImage = 'assets/backgrounds/desktopBackground.png'
        self.fileIcon = 'assets/icons/fileIcon.png'
        self.folderIcon = 'assets/icons/folderIcon.png'
        self.terminalIcon = 'assets/icons/terminalIcon.png'
        self.textEditorIcon = 'assets/icons/textEditorIcon.png'
        self.fileExplorerIcon = 'assets/icons/fileExplorerIcon.png'
        self.terminalOpen = False
        self.filesDisplayed = [] #list of files currently shown on desktop
        self.windowManager = app.windowManager
        self.fontSize = 0.034 * app.height
        # dynamic clock/date display
        app.clockDate = ClockDate(app, x=0, y=0, width=app.width, height=app.height)

    def draw(self, app):
        # draw desktop background image
        try:
            drawImage(self.backgroundImage, 0, 0, width=app.width, height=app.height)
        except:
            # fallback to solid color if image not found
            drawRect(0, 0, app.width, app.height, fill=self.bgColor)
        self.drawFiles(app)
        app.windowManager.drawWindows(app, app.mouseX, app.mouseY)
        self.drawClockDate(app)
        app.windowManager.drawMinimizedBar(app)

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
            elif  file[1] == 'executable':
                if file[0] == 'Terminal':
                    drawImage(self.terminalIcon, x, y, width=iconSize, height=iconSize)
                elif file[0] == 'Tartano': 
                    drawImage(self.textEditorIcon, x, y, width=iconSize, height=iconSize)
                elif file[0] == 'File Explorer':
                    drawImage(self.fileExplorerIcon, x, y, width=iconSize, height=iconSize)
            # draw filename
            drawLabel(file[0], x + iconSize / 2, y + iconSize + 15, size=self.fontSize, align='center', fill='black')

            # store displayed file info for click detection
            self.filesDisplayed.append((file, x, y, iconSize, iconSize + 15))

            # update position for next icon
            x += iconSize + padding
            if x + iconSize > app.width:
                x = startX
                y += iconSize + padding + 15

    def drawClockDate(self, app):
        app.clockDate.draw(app)
            
    
    def checkWindowHover(self, mouseX, mouseY):
        # Check if mouse is over any window
        self.mouseOnWindow = False
        for windowName, windowData in app.windowManager.windows.items():
            left, right, top, bottom = app.windowManager.getWindowBounds(windowData, app)
            if left <= mouseX <= right and top <= mouseY <= bottom:
                return True
            
    def onKeyPress(self, app, key, modifiers):
        # route keyboard input to window clients (like Terminal)
        app.windowManager.handleClientKeyPress(app, key, modifiers)
        # also handle desktop-level shortcuts
        app.windowManager.onKeyPress(app, key, modifiers)
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
        # First try window manager (resizing, dragging, button clicks)
        app.windowManager.mousePress(app, mouseX, mouseY)
        
        # Finally check if a desktop icon was clicked
        for fileInfo in self.filesDisplayed:
            file, x, y, w, h = fileInfo
            if (x <= mouseX <= x + w) and (y <= mouseY <= y + h):
                if self.checkWindowHover(mouseX, mouseY):
                    # don't open file if clicking on a window
                    return
                self.windowManager.openWindow(file[0], app)
                print(f"Clicked on {file[0]}")

    def onMouseDrag(self, app, mouseX, mouseY):
        app.windowManager.mouseDragWindow(app, mouseX, mouseY)

    def onMouseRelease(self, app, mouseX, mouseY):
        app.windowManager.stopDragging()
                          
    
