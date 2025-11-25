from cmu_graphics import *

class WindowManager:
    def __init__(self, app):
        self.windows = {}
        # Store ratios instead of absolute positions
        self.xRatio = 0.5  # center of screen
        self.yRatio = 0.5  # center of screen
        self.widthRatio = 0.35  # 35% of screen width
        self.heightRatio = 0.4  # 40% of screen height
        self.align = 'center'
        self.cornerSize = 20
        self.hoveredCorner = None

    
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

    def closeWindow(self, window):
        if window in self.windows:
            del self.windows[window]

    def getOpenWindows(self):
        return self.windows
    
    # Calculate actual dimensions based on app size and ratios
    def getActualDimensions(self, windowData, app):
        x = int(windowData['xRatio'] * app.width)
        y = int(windowData['yRatio'] * app.height)
        w = int(windowData['widthRatio'] * app.width)
        h = int(windowData['heightRatio'] * app.height)
        return x, y, w, h
    
    # Get window bounds (left, right, top, bottom) accounting for center alignment
    def getWindowBounds(self, windowData, app):
        x, y, w, h = self.getActualDimensions(windowData, app)
        # With center alignment: center is at (x, y)
        left = x - w // 2
        right = x + w // 2
        top = y - h // 2
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
                
                for cx, cy, cornerName in corners:
                    # Highlight corner if hovering
                    if self.hoveredCorner and self.hoveredCorner[0] == windowName and self.hoveredCorner[1] == cornerName:
                        drawRect(cx, cy, self.cornerSize, self.cornerSize, align='center', fill='purple')
                    else:
                        drawRect(cx, cy, self.cornerSize, self.cornerSize, align='center', fill='grey', opacity=0.5)

    def windowClient(self, windowName, name, x, y, width, height):
        # Draw window with center alignment
        drawRect(x, y, width, height, fill='lightGrey', align='center')
        drawLabel(name, x, y, size=14)

    def mousePress(self, app, mouseX, mouseY):
        # Just recognize corners for now
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
                    print(f"Corner detected: {windowName} {corner}")
                    return

    def mouseDrag(self, app, mouseX, mouseY):
        pass
    
    def mouseRelease(self):
        pass
