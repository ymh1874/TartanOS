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

        # login stage - tracks if we're logging in or using terminal
        self.isLoggingIn = True
        self.loginStage = "username"  # "username" or "password"
        self.tempUsername = ""
        self.tempPassword = ""
        self.profilePicPath = 'assets/profilePic.png'  # placeholder profile picture

        # init display
        if self.isLoggingIn:
            self.output("Welcome to TartanOS")

    # Login Handling
    def processLoginEnter(self):
        if self.loginStage == "username":
            self.tempUsername = self.tempInput
            self.tempInput = ""
            self.loginStage = "password"
            self.output(f"Username: {self.tempUsername}")
            
        elif self.loginStage == "password":
            self.tempPassword = self.tempInput
            self.tempInput = ""

            # verify credentials
            if self.app.auth.verify(self.tempUsername, self.tempPassword):
                self.username = self.tempUsername
                self.output("Access Granted")
                self.isLoggingIn = False
                self.loginStage = "username"  # reset for next login
                # switch to desktop mode
                self.app.modeManager.setMode('desktop')
            else:
                self.output("Access Denied - Try again")
                self.loginStage = "username"
                self.tempUsername = ""

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
        # handle login input
        if self.isLoggingIn:
            self.handleLoginInput(key)
            return

        # handle terminal input (ctrl+t from desktop goes to terminal mode after login)
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
        # handle input during login stage
        if key == 'enter':
            self.processLoginEnter()
            return
        elif key == "backspace":
            self.tempInput = self.tempInput[:-1]
        elif len(key) == 1:
            self.tempInput += key

    def draw(self, app):
        # recalculate all dimensions on each draw to handle window resizes
        self.w = app.width
        self.h = app.height
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

        # draw login input if logging in
        if self.isLoggingIn:
            if self.loginStage == "username":
                prompt = f"Username: {self.tempInput}"
            else:
                prompt = f"Password: {'*' * len(self.tempInput)}"
            drawLabel(prompt, self.x + self.margin, y,
                size=self.fontSize, fill=self.textColor, font='monospace', align='left')
            # draw cursor for login
            self.drawCursor(app, y)
        else:
            # draw terminal input line
            currentY = self.y + self.margin + len(history) * self.lineSpacing
            drawLabel(f"{self.prompt}{self.currLine}", self.x + self.margin, currentY,
                size=self.fontSize, fill=self.textColor, font='monospace', align='left')
            # draw cursor at correct y
            self.drawCursor(app, currentY)

        

    def drawCursor(self, app, y):
        # blinking cursor using app.tick as frame counter
        if self.isLoggingIn:
            # login mode cursor
            if self.loginStage == "username":
                textToMeasure = f"Username: {self.tempInput}"
            else:
                textToMeasure = f"Password: {'*' * len(self.tempInput)}"
        else:
            # terminal mode cursor
            textToMeasure = self.prompt + self.currLine

        # show cursor half the time
        if app.tick % 72 > 36:
            cursorX = self.x + self.margin + len(textToMeasure) * (self.fontSize * 0.6)
            # align cursor vertically with the label's Y
            cursorY = y + (self.lineSpacing - self.fontSize) / 2 + self.cursorCalibration
            drawRect(cursorX, cursorY, 10, self.fontSize, fill='white')



