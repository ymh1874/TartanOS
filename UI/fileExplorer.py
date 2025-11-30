from cmu_graphics import *
class FileExplorer:
    def __init__(self, app, windowName=None, path = None,  align='center', **kwargs):
        self.app = app
        self.windowName = windowName
        self.fs = app.fs
        self.currentPath = path if path else "/home"
        self.files = []
        self.items = []
        self.theme = 'dark'
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0) 
        self.width = kwargs.get('width', app.width)
        self.height = kwargs.get('height', app.height)
        self.iconSize = max(50, int(self.width * 0.07))
        self.fileIcon = 'assets/icons/fileIcon.png'
        self.folderIcon = 'assets/icons/folderIcon.png'
        self.terminalIcon = 'assets/icons/terminalIcon.png'
        self.textEditorIcon = 'assets/icons/textEditorIcon.png'
        self.fileExplorerIcon = 'assets/icons/fileExplorerIcon.png'
        self.marginX = 20
        self.marginY = 20
        # navigation history
        if self.currentPath == "/home":
            self.pathHistory = ["/","/home"]
            self.historyIndex = 1
        else:
            self.pathHistory = ["/","/home", self.currentPath]
            self.historyIndex = 2
        # search bar properties
        self.searchText = ""
        self.searchBoxFocused = False
        self.searchBarHeight = 35
        self.searchBoxWidth = 180
        self.searchBoxHeight = 25
        # navigation buttons
        self.backButtonX = self.x + 10
        self.backButtonY = self.y + 12
        self.backButtonSize = 20
        self.forwardButtonX = self.x + 35
        self.forwardButtonY = self.y + 12
        self.forwardButtonSize = 20



    def draw(self, app):
        # draw file explorer UI
        from cmu_graphics import drawRect, drawLabel, drawLine
        drawRect(self.x, self.y, self.width, self.height, fill='lightgray')
        
        # recalculate button positions for resizing
        self.backButtonX = self.x + 10
        self.backButtonY = self.y + 12
        self.forwardButtonX = self.x + 35
        self.forwardButtonY = self.y + 12
        
        # draw back button (left arrow)
        backEnabled = self.historyIndex > 0
        backColor = 'darkblue' if backEnabled else 'lightgray'
        drawRect(self.backButtonX, self.backButtonY, self.backButtonSize, self.backButtonSize, fill=backColor, border='black', borderWidth=1)
        drawLabel('<', self.backButtonX + self.backButtonSize // 2, self.backButtonY + self.backButtonSize // 2, size=12, fill='white', align='center')
        
        # draw forward button (right arrow)
        forwardEnabled = self.historyIndex < len(self.pathHistory) - 1
        forwardColor = 'darkblue' if forwardEnabled else 'lightgray'
        drawRect(self.forwardButtonX, self.forwardButtonY, self.forwardButtonSize, self.forwardButtonSize, fill=forwardColor, border='black', borderWidth=1)
        drawLabel('>', self.forwardButtonX + self.forwardButtonSize // 2, self.forwardButtonY + self.forwardButtonSize // 2, size=12, fill='white', align='center')
        
        drawLabel(f"File Explorer - {self.currentPath}", self.x + 70, self.y + 20, size=16, fill='black', align='left')

        # recalculate search box position for resizing - top right corner
        self.searchBoxX = self.x + self.width - self.searchBoxWidth - 15
        self.searchBoxY = self.y + 12

        # draw search bar at top right
        borderColor = 'blue' if self.searchBoxFocused else 'darkgray'
        drawRect(self.searchBoxX, self.searchBoxY, self.searchBoxWidth, self.searchBoxHeight, fill='white', border=borderColor, borderWidth=2)
        displayText = self.searchText if self.searchText else "Search..."
        textColor = 'black' if self.searchText else 'gray'
        drawLabel(displayText, self.searchBoxX + 8, self.searchBoxY + self.searchBoxHeight // 2, size=10, fill=textColor, align='left')

        # list files and folders in current directory
        startY = self.y + 55
        self.drawFiles(app, self.currentPath, self.x + 20, startY)


    def drawFiles(self, app, currPath, x, y):
        # draw files and folders in the current directory
        # ensure that it doesnt go over borders of window
        startX = x
        currDrawX = x
        currDrawY = y
        self.currentPath = currPath
        self.files = []
        self.folders = []
        self.items = []  # clear items list before getting new items
        self.getCurrItems()
        # sort items alphabetically by name
        self.items = sorted(self.items, key=lambda item: item[0].lower())

        # filter items by search text - keep tuples intact  
        filteredItems = [item for item in self.items if self.searchText.lower() in item[0].lower()]

        # recalculate icon size and spacing based on window width
        self.iconSize = max(50, int(self.width * 0.07))
        maxX = self.x + self.width - 20  # leave margin
        maxY = self.y + self.height - 20  # leave margin at bottom

        for itemName, itemType in filteredItems:
            # check if item would exceed bottom boundary
            if currDrawY + self.iconSize + 30 > maxY:
                break  # don't draw items that exceed window
                
            if itemType == 'file':
                drawImage(self.fileIcon, currDrawX, currDrawY, width=self.iconSize, height=self.iconSize)
                drawLabel(itemName, currDrawX + self.iconSize / 2, currDrawY + self.iconSize + 15, size=12, align='center', fill='black')
                self.files.append((itemName, currDrawX, currDrawY))
            elif itemType == 'folder':
                drawImage(self.folderIcon, currDrawX, currDrawY, width=self.iconSize, height=self.iconSize)
                drawLabel(itemName, currDrawX + self.iconSize / 2, currDrawY + self.iconSize + 15, size=12, align='center', fill='black')
                self.folders.append((itemName, currDrawX, currDrawY))
            elif itemType == 'executable':
                for exe in ['Terminal', 'Tartano', 'File Explorer']:
                    if itemName == exe:
                        if exe == 'Terminal':
                            drawImage(self.terminalIcon, currDrawX, currDrawY, width=self.iconSize, height=self.iconSize)
                        elif exe == 'Tartano':
                            drawImage(self.textEditorIcon, currDrawX, currDrawY, width=self.iconSize, height=self.iconSize)
                        elif exe == 'File Explorer':
                            drawImage(self.fileExplorerIcon, currDrawX, currDrawY, width=self.iconSize, height=self.iconSize)
                drawLabel(itemName, currDrawX + self.iconSize / 2, currDrawY + self.iconSize + 15, size=12, align='center', fill='black')
                self.files.append((itemName, currDrawX, currDrawY))  # store as file so it's clickable
            
            currDrawX += self.iconSize + self.marginX
            if currDrawX + self.iconSize > maxX:
                currDrawX = startX
                currDrawY += self.iconSize + self.marginY + 15
        

        
    def getCurrItems(self):
        for items in self.app.fs.getChildren(self.currentPath):
            full_path = f"{self.currentPath}/{items}"
            if self.app.fs.isFile(full_path):
                self.items.append((items, 'file'))
            elif self.app.fs.isFolder(full_path):
                self.items.append((items, 'folder'))
            elif self.app.fs.isExecutable(full_path):
                self.items.append((items, 'executable'))

    def onMousePress(self, app, mouseX, mouseY):
        # check if back button is clicked
        if (self.backButtonX <= mouseX <= self.backButtonX + self.backButtonSize and
            self.backButtonY <= mouseY <= self.backButtonY + self.backButtonSize):
            if self.historyIndex > 0:
                self.historyIndex -= 1
                self.currentPath = self.pathHistory[self.historyIndex]
            return
        
        # check if forward button is clicked
        if (self.forwardButtonX <= mouseX <= self.forwardButtonX + self.forwardButtonSize and
            self.forwardButtonY <= mouseY <= self.forwardButtonY + self.forwardButtonSize):
            if self.historyIndex < len(self.pathHistory) - 1:
                self.historyIndex += 1
                self.currentPath = self.pathHistory[self.historyIndex]
            return
        
        # check if search box is clicked
        if (self.searchBoxX <= mouseX <= self.searchBoxX + self.searchBoxWidth and
            self.searchBoxY <= mouseY <= self.searchBoxY + self.searchBoxHeight):
            self.searchBoxFocused = True
            return
        else:
            self.searchBoxFocused = False

        # check if a file is clicked
        for fileName, fileX, fileY in self.files:
            if (fileX <= mouseX <= fileX + self.iconSize and
                fileY <= mouseY <= fileY + self.iconSize):
                # open file in nano editor
                if fileName == 'Terminal':
                    app.modeManager.setMode('terminal')
                    return
                elif fileName == 'Tartano':
                    app.modeManager.setMode('nano', filePath=f"{self.currentPath}/{fileName}")
                    return
                elif fileName == 'File Explorer':
                    return  # already in file explorer
                elif self.app.fs.isFile(f"{self.currentPath}/{fileName}"):
                    self.app.modeManager.setMode('nano', filePath=f"{self.currentPath}/{fileName}")
                return

        # check if a folder is clicked
        for folderName, folderX, folderY in self.folders:
            if (folderX <= mouseX <= folderX + self.iconSize and
                folderY <= mouseY <= folderY + self.iconSize):
                # navigate into folder
                newPath = f"{self.currentPath}/{folderName}"
                # add to history (remove any forward history when navigating to new folder)
                self.pathHistory = self.pathHistory[:self.historyIndex + 1]
                self.pathHistory.append(newPath)
                self.historyIndex = len(self.pathHistory) - 1
                self.currentPath = newPath
                return
        

    def onKeyPress(self, app, key, modifiers):
        # handle keyboard input for navigation and search bar
        # handle arrow keys for back/forward navigation
        if key == 'left' and 'shift' in modifiers:
            # Ctrl+Left for back
            if self.historyIndex > 0:
                self.historyIndex -= 1
                self.currentPath = self.pathHistory[self.historyIndex]
            return
        elif key == 'right' and 'shift' in modifiers:
            # Ctrl+Right for forward
            if self.historyIndex < len(self.pathHistory) - 1:
                self.historyIndex += 1
                self.currentPath = self.pathHistory[self.historyIndex]
            return
        
        # search bar input
        if key == 'backspace':
            self.searchText = self.searchText[:-1]
        elif key == 'space':
            self.searchText += ' '
        elif key == 'escape':
            self.searchText = ""
        elif len(key) == 1:
            # accept letters, numbers, and common characters
            if key.isalnum() or key in '-_.()[]':
                self.searchText += key
    
