from cmu_graphics import *
from datetime import datetime

class ClockDate:
    def __init__(self, app, x, y, width, height):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background = "assets/backgrounds/clockDate.png"
        self.fontSize = min(0.025 * app.height, 0.025 * app.width)

    def draw(self, app):
        # Update sizes dynamically for responsiveness
        self.fontSize = min(0.025 * app.height, 0.025 * app.width)

        # Resize the background image proportionally
        bgWidth = app.width 
        bgHeight = app.height * 0.02

        # top right corner 
        bgX = app.width - bgWidth
        bgY = 0 
        # Draw background
        drawImage(self.background, bgX, bgY, width=bgWidth, height=bgHeight)

        # Calculate text positions inside the background
        timeX = bgX + bgWidth - 15
        timeY = bgY + bgHeight * 0.45
        # date before time
        dateX = timeX - bgWidth * 0.35
        dateY = timeY
        # Draw time
        now = datetime.now()
        timeStr = now.strftime("%I:%M %p").lstrip("0")
        dateStr = now.strftime("%A, %B %d")

        drawLabel(timeStr, timeX, timeY,
                  size=self.fontSize, align='right', fill='white', bold=True)

        drawLabel(dateStr, dateX, dateY,
                  size=self.fontSize * 0.7, align='right', fill='white', bold=False)
