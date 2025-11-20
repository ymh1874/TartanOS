# ui/terminal/terminal.py
from cmu_graphics import *
from systems.pathUtils import PathUtils
from systems.commandRegistry import CommandRegistry

class Terminal:
    def __init__(self, app):
        # external
        self.app = app
        self.fs = app.fs
        

        # visual
        self.textColor = 'white'
        self.backgroundColor = 'black'
        self.fontSize = max(20, int(app.width * 0.018))
        self.lineSpacing = self.fontSize * 1.3
        self.margin = app.width * 0.02
        # (cursor alignment follows backup implementation)
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
        self.Stage = "username"
        self.tempInput = ""
        self.tempUsername = ""
        self.tempPassword = ""

        # init
        self.output("Welcome to TartanOS Terminal")
        self.output("Login required")

    # ===========================
    # Login Handling
    # ===========================

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
                self.stage = "done"
            else:
                self.output("Access Denied")
                self.stage = "username"

    # ===========================
    # Path Resolution
    # ===========================

    def resolvePath(self, name):
        if name.startswith('/'):
            return name
        return PathUtils.join(self.currPath, name)

    # ===========================
    # Output
    # ===========================

    def output(self, text):
        self.textLines.append(text)
        if len(self.textLines) > self.maxLines:
            self.textLines.pop(0)

    def clear(self):
        self.textLines = []

    # ===========================
    # Input Handling
    # ===========================

    def onKeyPress(self, app, key, modifiers):
        if self.stage != "done":
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

    # ===========================
    # Drawing
    # ===========================

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill=self.backgroundColor)

        # compute how many lines fit and draw history
        availableLines = int((app.height - 2 * self.margin) // self.lineSpacing)
        history = self.textLines[-availableLines:]

        y = self.margin
        for line in history:
            drawLabel(line, self.margin, y, size=self.fontSize, fill=self.textColor,
                font='monospace', align='left')
            y += self.lineSpacing

        # login mode
        if self.loginStage != "done":
            prompt = (
                f"Username: {self.tempInput}" if self.loginStage == "username"
                else f"Password: {'*' * len(self.tempInput)}"
            )
            drawLabel(prompt, self.margin, y, size=self.fontSize,
                    fill=self.textColor, font='monospace', align='left')
            # draw cursor for login input as well
            self.drawCursor(app, y, text=prompt)
            return

        # draw input line at the next available Y
        currentY = self.margin + len(history) * self.lineSpacing
        drawLabel(f"{self.prompt}{self.currLine}", self.margin, currentY,
            size=self.fontSize, fill=self.textColor, font='monospace', align='left')

        # draw cursor at correct y
        self.drawCursor(app, currentY)

        

    def drawCursor(self, app, y, text=None):
        """Blinking cursor. Accepts optional `text` to compute cursor X (used for login prompts)."""
        # determine the text to measure for cursor X
        textToMeasure = text if text is not None else (self.prompt + self.currLine)

        # show cursor half the time using app.tick as a frame counter
        if app.tick % 72 > 36:
            cursorX = self.margin + len(textToMeasure) * (self.fontSize * 0.6)
            # align cursor vertically with the label's Y (centered in the line spacing)
            cursorY = y + (self.lineSpacing - self.fontSize) / 2 + self.cursorCalibration
            drawRect(cursorX, cursorY, 10, self.fontSize, fill='white')



