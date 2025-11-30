from cmu_graphics import *
class WindowManager:
    def __init__(self, app):
        self.windows = {}
        self.app = app
        # Store ratios instead of absolute positions
        self.xRatio = 0.5  # center of screen
        self.yRatio = 0.5  # center of screen
        self.widthRatio = 0.35  # 35% of screen width
        self.heightRatio = 0.4  # 40% of screen height
        self.align = 'center'
        self.cornerSize = 10
        self.hoveredCorner = None
        self.fontSize = 0.045 * app.height
        self.menuRectSize = 0.05 * app.height
        self.currWindow = None  # currently focused window
        self.mouseOnWindow = False
        self.orderWindow = [] # current windows in order

        # Resizing state
        self.resizingWindow = None
        self.resizingCorner = None  # which corner is being dragged
        self.resizeStartMouseX = 0
        self.resizeStartMouseY = 0
        self.resizeStartWidth = 0
        self.resizeStartHeight = 0
        self.resizeStartCenterX = 0
        self.resizeStartCenterY = 0
        
        # Dragging state
        self.draggingWindow = None
        self.dragOffsetX = 0
        self.dragOffsetY = 0

    
    def openWindow(self, window, app):
        # Store ratios for responsive resizing
        self.windows[window] = {
            'name': window, 
            'xRatio': self.xRatio, 
            'yRatio': self.yRatio,  
            'widthRatio': self.widthRatio, 
            'heightRatio': self.heightRatio, 
            'align': self.align
        }
        if window not in self.orderWindow:
            self.orderWindow.append(window)
        self.currWindow = window  # set as current focused window

    def closeWindow(self, window):
        if window in self.windows:
            del self.windows[window]
            # cleanup client resources if needed
            self.app.clientRender.closeClient(window)
        if window in self.orderWindow:
            self.orderWindow.remove(window)
        if self.currWindow == window:
            self.currWindow = self.orderWindow[-1] if self.orderWindow else None

    def getOpenWindows(self):
        return self.windows 
    
    # Calculate actual dimensions based on app size and ratios
    def getActualDimensions(self, windowData, app):
        x = int(windowData['xRatio'] * app.width)
        y = int(windowData['yRatio'] * app.height)
        w = int(windowData['widthRatio'] * app.width)
        h = int(windowData['heightRatio'] * app.height)
        return x, y, w, h
    
    # Get window bounds (left, right, top, bottom) accounting for center alignment and menu bar
    def getWindowBounds(self, windowData, app):
        x, y, w, h = self.getActualDimensions(windowData, app)
        # With center alignment: center is at (x, y)
        left = x - w // 2
        right = x + w // 2
        top = y - h // 2 - self.menuRectSize // 2  # offset by half menu height
        bottom = y + h // 2
        return left, right, top, bottom
    
    def isMouseInCorner(self, mouseX, mouseY, cornerX, cornerY):
        # Check if mouse is within cornerSize of a corner
        return abs(mouseX - cornerX) <= self.cornerSize and abs(mouseY - cornerY) <= self.cornerSize
    
    def checkCornerHover(self, mouseX, mouseY, app):
        # Check which window corner the mouse is hovering over
        self.hoveredCorner = None
        for windowName, windowData in self.windows.items():
            left, right, top, bottom = self.getWindowBounds(windowData, app)
            corners = {
                'bottom-right': (right, bottom),
                'bottom-left': (left, bottom),
                'top-right': (right, top),
                'top-left': (left, top)
            }
            for corner, (cx, cy) in corners.items():
                if self.isMouseInCorner(mouseX, mouseY, cx, cy):
                    self.hoveredCorner = (windowName, corner)
                    return
    
    def drawWindows(self, app, mouseX=None, mouseY=None):
        # Check for hovered corners
        if mouseX is not None and mouseY is not None:
            self.checkCornerHover(mouseX, mouseY, app)
        
        # Draw all open windows
        for windowName, windowData in self.windows.items():
            x, y, w, h = self.getActualDimensions(windowData, app)
            self.windowClient(windowName, windowData['name'], x, y, w, h)
            
            # Draw corner resize handles
            if mouseX is not None and mouseY is not None:
                left, right, top, bottom = self.getWindowBounds(windowData, app)
                corners = [
                    (right, bottom, 'bottom-right'),
                    (left, bottom, 'bottom-left'),
                    (right, top, 'top-right'),
                    (left, top, 'top-left')
                ]
                
                for x, y, cornerName in corners:
                    # Highlight corner if hovering
                    if self.hoveredCorner and self.hoveredCorner[0] == windowName and self.hoveredCorner[1] == cornerName:
                        drawRect(x, y, self.cornerSize, self.cornerSize, align='center', fill='purple')
                    

    def windowClient(self, windowName, name, x, y, width, height):
        # Draw window with center alignment
        drawRect(x, y, width, height, fill='lightGrey', align='center')
        drawRect(x, y - height // 2, width, self.menuRectSize, fill='darkGrey', align='center')  # title bar
        
        drawRect(x + width // 2 - 10, y - height // 2, self.menuRectSize, self.menuRectSize, fill='red', align='center')  # close button
        drawLabel('X', x + width // 2 - 10, y - height // 2, size=self.fontSize, fill='white', align='center')
        drawRect(x + width // 2 - 30, y - height // 2, self.menuRectSize, self.menuRectSize, fill='green', align='center')  # maximize button
        drawLabel('+', x + width // 2 - 30, y - height // 2, size=self.fontSize, fill='white', align='center')
        drawRect(x + width // 2 - 50, y - height // 2, self.menuRectSize, self.menuRectSize, fill='yellow', align='center')  # minimize button
        drawLabel('-', x + width // 2 - 50, y - height // 2, size=self.fontSize, fill='black', align='center')
        drawLabel(name, x - width // 2 , y - height // 2, size=self.fontSize, fill='black', align='left')

        # render client content through ClientRender
        self.app.clientRender.instantClient(windowName, x, y + self.menuRectSize // 2, width, height - self.menuRectSize, 'center')
            

    def checkDrag(self, mouseX, mouseY, app):
        # Check if clicking in title bar of any window
        for windowName, windowData in self.windows.items():
            left, right, top, bottom = self.getWindowBounds(windowData, app)
            # Check if in title bar (top 10% of window height)
            if left <= mouseX <= right and top <= mouseY <= top + 0.1 * app.height:
                return windowName
        return None
            
    def moveWindow(self, newXRatio, newYRatio, windowName):
        self.windows[windowName]['xRatio'] = newXRatio
        self.windows[windowName]['yRatio'] = newYRatio

    def resizeWindow(self, windowName, newWidthRatio, newHeightRatio, newXRatio=None, newYRatio=None):
        # Check if window still exists before resizing
        if windowName not in self.windows:
            return
        
        # Minimum size constraints
        minWidth = 0.15  # 15% of screen width
        minHeight = 0.15  # 15% of screen height
        
        self.windows[windowName]['widthRatio'] = max(minWidth, newWidthRatio)
        self.windows[windowName]['heightRatio'] = max(minHeight, newHeightRatio)
        
        if newXRatio is not None:
            self.windows[windowName]['xRatio'] = newXRatio
        if newYRatio is not None:
            self.windows[windowName]['yRatio'] = newYRatio
                
    def startDragging(self, mouseX, mouseY, app):
        # Check if clicking on a window's title bar
        windowName = self.checkDrag(mouseX, mouseY, app)
        if windowName:
            self.draggingWindow = windowName
            # Calculate offset from window center to mouse
            windowData = self.windows[windowName]
            centerX = windowData['xRatio'] * app.width
            centerY = windowData['yRatio'] * app.height
            self.dragOffsetX = mouseX - centerX
            self.dragOffsetY = mouseY - centerY
            return True
        return False
    
    def startResizing(self, mouseX, mouseY, app):
        # Check if clicking on a window corner
        for windowName, windowData in self.windows.items():
            left, right, top, bottom = self.getWindowBounds(windowData, app)
            corners = {
                'bottom-right': (right, bottom),
                'bottom-left': (left, bottom),
                'top-right': (right, top),
                'top-left': (left, top)
            }
            for corner, (cx, cy) in corners.items():
                if self.isMouseInCorner(mouseX, mouseY, cx, cy):
                    self.resizingWindow = windowName
                    self.resizingCorner = corner
                    
                    # Store initial state
                    self.resizeStartMouseX = mouseX
                    self.resizeStartMouseY = mouseY
                    
                    x, y, w, h = self.getActualDimensions(windowData, app)
                    self.resizeStartWidth = w
                    self.resizeStartHeight = h
                    self.resizeStartCenterX = x
                    self.resizeStartCenterY = y
                    
                    print(f"Start resizing: {windowName} {corner}")
                    return True
        return False
    
    def pushWindowToFront(self, mouseX, mouseY, app):
        # push the licked window to the front
        for window in list(self.orderWindow):
            if window not in self.windows:
                
                self.orderWindow.remove(window)
                continue
            windowData = self.windows[window]
            left, right, top, bottom = self.getWindowBounds(windowData, app)
            if left <= mouseX <= right and top <= mouseY <= bottom:
                # Reinsert the window to the end of the dict to bring it to front
                if window == self.currWindow:
                    return  # already front
                self.windows[window] = self.windows.pop(window)
                self.orderWindow.remove(window)
                self.orderWindow.append(window)
                self.currWindow = window
                return

    def mousePress(self, app, mouseX, mouseY):
        self.pushWindowToFront(mouseX, mouseY, app)
        # Try resizing first (corners have priority)
        if not self.startResizing(mouseX, mouseY, app):
            # If not resizing, try dragging
            self.startDragging(mouseX, mouseY, app)
        # push window to front
        # Check for clicks on window menu buttons
        for windowName, windowData in self.windows.items():
            left, right, top, bottom = self.getWindowBounds(windowData, app)
            # Check if close button clicked
            if (right - self.menuRectSize <= mouseX <= right) and (top <= mouseY <= top + self.menuRectSize):
                self.closeWindow(windowName)
                return
            # Check if maximize button clicked
            elif (right - 2 * self.menuRectSize <= mouseX <= right - self.menuRectSize) and (top <= mouseY <= top + self.menuRectSize):
                # Maximize to full screen
                self.resizeWindow(windowName, 1.0, 1.0, 0.5, 0.5)
                return
            # Check if minimize button clicked
            elif (right - 3 * self.menuRectSize <= mouseX <= right - 2 * self.menuRectSize) and (top <= mouseY <= top + self.menuRectSize):
                # Minimize (for simplicity, just close the window)
                self.closeWindow(windowName)
                return
        
        # Route mouse press to current active window's client
        if self.currWindow and self.currWindow in self.windows:
            app.clientRender.onMousePress(self.currWindow, app, mouseX, mouseY)

    def mouseDragWindow(self, app, mouseX, mouseY):
        if not self.draggingWindow and not self.resizingWindow:
            return  # Nothing to do
        # Handle window dragging
        if self.draggingWindow and not self.resizingWindow:
            # Check if window still exists
            if self.draggingWindow not in self.windows:
                self.stopDragging()
                return
            # Calculate new center position (mouse position - offset)
            newCenterX = mouseX - self.dragOffsetX
            newCenterY = mouseY - self.dragOffsetY
            
            # Convert to ratios
            newXRatio = newCenterX / app.width
            newYRatio = newCenterY / app.height
            
            # Clamp to keep window on screen
            newXRatio = max(0, min(1, newXRatio))
            newYRatio = max(0, min(1, newYRatio))
            
            self.moveWindow(newXRatio, newYRatio, self.draggingWindow)
        
        # Handle window resizing
        elif self.resizingWindow:
            # Check if window still exists
            if self.resizingWindow not in self.windows:
                self.stopResizing()
                return
            
            # Calculate how much the mouse has moved
            deltaX = mouseX - self.resizeStartMouseX
            deltaY = mouseY - self.resizeStartMouseY
            
            # Calculate new dimensions based on which corner is being dragged
            if self.resizingCorner == 'bottom-right':
                # Grow right and down
                newWidth = self.resizeStartWidth + deltaX
                newHeight = self.resizeStartHeight + deltaY
                # Center moves right and down by half the change
                newCenterX = self.resizeStartCenterX + deltaX / 2
                newCenterY = self.resizeStartCenterY + deltaY / 2
                
            elif self.resizingCorner == 'bottom-left':
                # Grow left and down
                newWidth = self.resizeStartWidth - deltaX
                newHeight = self.resizeStartHeight + deltaY
                # Center moves left (negative) and down
                newCenterX = self.resizeStartCenterX + deltaX / 2
                newCenterY = self.resizeStartCenterY + deltaY / 2
                
            elif self.resizingCorner == 'top-right':
                # Grow right and up
                newWidth = self.resizeStartWidth + deltaX
                newHeight = self.resizeStartHeight - deltaY
                # Center moves right and up (negative)
                newCenterX = self.resizeStartCenterX + deltaX / 2
                newCenterY = self.resizeStartCenterY + deltaY / 2
                
            elif self.resizingCorner == 'top-left':
                # Grow left and up
                newWidth = self.resizeStartWidth - deltaX
                newHeight = self.resizeStartHeight - deltaY
                # Center moves left (negative) and up (negative)
                newCenterX = self.resizeStartCenterX + deltaX / 2
                newCenterY = self.resizeStartCenterY + deltaY / 2
            
            # Convert to ratios
            newWidthRatio = newWidth / app.width
            newHeightRatio = newHeight / app.height
            newXRatio = newCenterX / app.width
            newYRatio = newCenterY / app.height
            
            # Apply the resize
            self.resizeWindow(
                self.resizingWindow, 
                newWidthRatio, 
                newHeightRatio, 
                newXRatio, 
                newYRatio
            )
    
        return False
    def stopDragging(self):
        self.draggingWindow = None
        self.dragOffsetX = 0
        self.dragOffsetY = 0

    def stopResizing(self):
        self.resizingWindow = None
        self.resizingCorner = None
        self.resizeStartMouseX = 0
        self.resizeStartMouseY = 0
        self.resizeStartWidth = 0
        self.resizeStartHeight = 0
        self.resizeStartCenterX = 0
        self.resizeStartCenterY = 0
    
    def closeAllWindows(self):
        self.windows = {}
        self.orderWindow = []
    
    def mouseRelease(self):
        self.stopDragging()
        self.stopResizing()

    def onKeyPress(self, app, key, modifiers):
        if modifiers == ['control'] and key == 'm':  # Ctrl+M to close all windows
            self.closeAllWindows()
    
    def handleClientKeyPress(self, app, key, modifiers):
        # route to clientRender for keyboard input handling
        self.app.clientRender.handleClientKeyPress(self.currWindow, app, key, modifiers)   
