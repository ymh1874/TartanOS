# ui/terminal/terminal.py
from cmu_graphics import *
from systems.pathUtils import PathUtils
from systems.commandRegistry import CommandRegistry
from core.appModes import ModeManager
class Terminal:
    def __init__(self, app):
        # external
        self.app = app
        self.fs = app.fs
        

        # terminal bounds (adjust these to resize/reposition the terminal)
        self.x = 0                    # left edge
        self.y = 0                    # top edge
        self.w = app.width            # width (full screen)
        self.h = app.height           # height (full screen)
        
        # visual
        self.textColor = 'white'
        self.backgroundColor = 'black'
        self.fontSize = max(12, int(self.w * 0.018))
        self.lineSpacing = self.fontSize * 1.3
        self.margin = self.w * 0.02

        # small pixel calibration for caret vertical position (positive moves cursor down)
        self.cursorCalibration = -12

        # terminal state
        self.username = "user"
        self.prompt = "> "
        self.textLines = []
        self.currLine = ""
        # history of entered lines for up/down navigation
        self.pastLines = []
        self.upTick = 0
        self.currPath = "/"
        self.currFiles = self.fs.get("/")
        self.maxLines = 200

        # command system
        self.commands = CommandRegistry(self)

        # login
        self.stage = "username"
        self.tempInput = ""
        self.tempUsername = ""
        self.tempPassword = ""

        # init     
        self.output("Login required....")

    # Login Handling
    def processLoginEnter(self):
        if self.stage == "username":
            self.tempUsername = self.tempInput
            self.tempInput = ""
            self.stage = "password"

        elif self.stage == "password":
            self.tempPassword = self.tempInput
            self.tempInput = ""

            if self.app.auth.verify(self.tempUsername, self.tempPassword):
                self.username = self.tempUsername
                self.output("Access Granted")
                self.stage = "desktop"
                self.app.modeManager.setMode('desktop')
                
            else:
                self.output("Access Denied")
                self.stage = "username"

    # Path Resolution   
    def resolvePath(self, name):
        if name.startswith('/'):
            return name
        return PathUtils.join(self.currPath, name)

    # Output
    def output(self, text, args = None):
        self.textLines.append(text)
        if len(self.textLines) > self.maxLines:
            self.textLines.pop(0)

    def clear(self):
        self.textLines = []

    # Input Handling
    def onKeyPress(self, app, key, modifiers):
        if self.stage != "desktop":
            self.handleLoginInput(key)
            return

        if key == "enter":
            cmd = self.currLine.strip()
            # save history and show the entered line
            self.pastLines.append(self.currLine)
            self.upTick = len(self.pastLines)
            self.output(f"{self.prompt}{cmd}")

            # execute command if present
            if cmd:
                name = cmd.split()[0]
                handler = self.commands.commands.get(name)
                if handler:
                    handler(cmd.split()[1:])
                else:
                    self.output(f'command not found: {name}')

            # reset current input
            self.currLine = ""
            return

        elif key == "backspace":
            self.currLine = self.currLine[:-1]
        
        elif key == 'space':
            self.currLine += ' '

        elif key == 'up':
            if self.upTick > 0:
                self.upTick -= 1
                self.currLine = self.pastLines[self.upTick]
        elif key == 'down':
            if self.upTick < len(self.pastLines) - 1:
                self.upTick += 1
                self.currLine = self.pastLines[self.upTick]
        elif len(key) == 1:
            self.currLine += key

    def handleLoginInput(self, key):
        if key == 'enter':
            self.processLoginEnter()
            return
        elif key == "backspace":
            self.tempInput = self.tempInput[:-1]
        elif len(key) == 1:
            self.tempInput += key

    # Drawing
    def draw(self, app):
        if self.stage != 'desktop':
            # recalculate bounds on each draw to handle window resizes
            self.w = app.width
            self.h = app.height
            self.fontSize = max(12, int(self.w * 0.018))
            self.lineSpacing = self.fontSize * 1.3
            self.margin = self.w * 0.015
        else:
            self.x = 0.220 * app.width
            self.y = 0.030 * app.height
            self.w = 0.7 * app.width
            self.h = 0.6 * app.height
            self.fontSize = max(12, int(self.w * 0.018))
            self.lineSpacing = self.fontSize * 1.3
            self.margin = self.w * 0.015

        # draw terminal background using bounds
        drawRect(self.x, self.y, self.w, self.h, fill=self.backgroundColor)

        # compute how many lines fit and draw history
        availableLines = int((self.h - 2 * self.margin) // self.lineSpacing)
        history = self.textLines[-availableLines:]

        y = self.y + self.margin
        for line in history:
            drawLabel(line, self.x + self.margin, y, size=self.fontSize, fill=self.textColor,
                font='monospace', align='left')
            y += self.lineSpacing

        # login mode
        if self.stage != "desktop":
            prompt = (
                f"Username: {self.tempInput}" if self.stage == "username"
                else f"Password: {'*' * len(self.tempInput)}"
            )
            drawLabel(prompt, self.x + self.margin, y, size=self.fontSize,
                    fill=self.textColor, font='monospace', align='left')
            # draw cursor for login input as well
            self.drawCursor(app, y, text=prompt)
            return
        else:
            

            # draw input line at the next available y
            currentY = self.y + self.margin + len(history) * self.lineSpacing
            drawLabel(f"{self.prompt}{self.currLine}", self.x + self.margin, currentY,
                size=self.fontSize, fill=self.textColor, font='monospace', align='left')

            # draw cursor at correct y
            self.drawCursor(app, currentY)

        

    def drawCursor(self, app, y, text=None):
        """Blinking cursor. Accepts optional `text` to compute cursor X (used for login prompts)."""
        # determine the text to measure for cursor X
        textToMeasure = text if text is not None else (self.prompt + self.currLine)

        # show cursor half the time using app.tick as a frame counter
        if app.tick % 72 > 36:
            cursorX = self.x + self.margin + len(textToMeasure) * (self.fontSize * 0.6)
            # align cursor vertically with the label's Y (centered in the line spacing)
            cursorY = y + (self.lineSpacing - self.fontSize) / 2 + self.cursorCalibration
            drawRect(cursorX, cursorY, 10, self.fontSize, fill='white')



