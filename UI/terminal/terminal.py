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
        self.index = 0  # cursor position in current line

        # small pixel calibration for caret vertical position (positive moves cursor down)
        self.cursorCalibration = -17

        # terminal state
        self.username = "user"
        self.prompt = "> "
        self.textLines = []
        self.currLine = ""
        # history of entered lines for up/down navigation
        self.pastLines = []
        self.upTick = 0
        self.currPath = "/"
        self.maxLines = 200

        # command system
        self.commands = CommandRegistry(self)
        
        # nano editor instance (initialized lazily when needed)
        self.nanoEditor = None
        # login stage - tracks if we're logging in or using terminal
        self.isLoggingIn = True
        self.loginStage = "username"  # "username" or "password"
        self.tempUsername = ""
        self.tempPassword = ""
        self.tempInput = ""  # current input during login
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
            if self.index > 0:
                self.currLine = self.currLine[:self.index - 1] + self.currLine[self.index:]
                self.index -= 1
        
        elif key == 'space':
            self.currLine = self.currLine[:self.index] + ' ' + self.currLine[self.index:]
            self.index += 1
        elif key == 'up':
            if self.upTick > 0:
                self.upTick -= 1
                self.currLine = self.pastLines[self.upTick]
        elif key == 'down':
            if self.upTick < len(self.pastLines) - 1:
                self.upTick += 1
                self.currLine = self.pastLines[self.upTick]
                
        elif key == 'left':
            self.index = max(0, self.index - 1)
        elif key == 'right':
            self.index = min(len(self.currLine), self.index + 1)
        elif isinstance(key, str) and len(key) == 1:
            self.currLine = self.currLine[:self.index] + key + self.currLine[self.index:]
            self.index += 1

    def onKeyHold(self, app, key, modifiers):
        # handle held keys for continuous input
        if self.isLoggingIn:
            return  # no key hold actions during login

        if key == "backspace":
            if self.currLine:
                self.currLine = self.currLine[:-1]
        elif key == 'delete':
            if self.index < len(self.currLine):
                self.currLine = self.currLine[:self.index] + self.currLine[self.index + 1:]
        elif key == 'left':
            self.index = max(0, self.index - 1)
        elif key == 'right':
            self.index = min(len(self.currLine), self.index + 1)
        elif isinstance(key, str) and len(key) == 1:
            self.currLine = self.currLine[:self.index] + key + self.currLine[self.index:]
            self.index += 1
        elif key == 'up':
            if self.upTick > 0:
                self.upTick -= 1
                self.currLine = self.pastLines[self.upTick]
        elif key == 'down':
            if self.upTick < len(self.pastLines) - 1:
                self.upTick += 1
                self.currLine = self.pastLines[self.upTick]

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
        else:
            # draw terminal input line
            currentY = self.y + self.margin + len(history) * self.lineSpacing
            drawLabel(f"{self.prompt}{self.currLine}", self.x + self.margin, currentY,
                size=self.fontSize, fill=self.textColor, font='monospace', align='left')
            # draw cursor at correct y
            self.drawCursor(app, currentY, self.index)
        

    def drawCursor(self, app, y, index):
        # blinking cursor using app.tick as frame counter
        if self.isLoggingIn:
            # login mode cursor
            if self.loginStage == "username":
                textToMeasure = f"Username: {self.tempInput}"
            else:
                textToMeasure = f"Password: {'*' * len(self.tempInput)}"
        else:  
            # terminal mode cursor
            textToMeasure =  self.prompt + self.currLine[:self.index] 

        # show cursor half the time
        if app.tick % 72 > 36:
            cursorX = self.x + self.margin + len(textToMeasure) * (self.fontSize * 0.6) 
            # align cursor vertically with the label's Y
            cursorY = y + (self.lineSpacing - self.fontSize) / 2 + self.cursorCalibration
            drawRect(cursorX, cursorY, self.fontSize * 0.45, self.fontSize, fill='white')
            try : 
                letter = self.currLine[index]
            except IndexError:
                letter = ' '
            drawLabel(letter, cursorX, 1.05 * cursorY , size=self.fontSize, fill='purple', font='monospace', align='left')



class NanoEditor(Terminal):
    def __init__(self, path, app, **kwargs):
        super().__init__(app)
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.w = kwargs.get('width', app.width)
        self.h = kwargs.get('height', app.height)
        self.indexY = 0  # line index for cursor vertical position
        self.filePath = path
        self.openMode = False  # waiting for file path input
        self.loadFile()

    def loadFile(self, path=None):
        if path is not None:
            self.filePath = path
        if self.fs.exists(self.filePath):
            node = self.fs.get(self.filePath)
            if "content" in node:
                self.textLines = node["content"].splitlines()
            else:
                self.textLines = []
        else:
            self.textLines = []

    def saveFile(self):
        content = "\n".join(self.textLines)
        if self.fs.exists(self.filePath):
            node = self.fs.get(self.filePath)
            node["content"] = content
        else:
            self.fs.fs[self.filePath] = {
                "type": "text file",
                "content": content
            }
    def onKeyHold(self, app, key, modifiers):
        if key == "backspace":
            if self.textLines:
                lastLine = self.textLines[-1]
                if lastLine:
                    self.textLines[-1] = lastLine[:-1]
                else:
                    self.textLines.pop()
        elif key == 'delete':
            if self.textLines:
                lastLine = self.textLines[-1]
                if lastLine:
                    self.textLines[-1] = lastLine[:-1]
                else:
                    self.textLines.pop()
        elif key == 'left':
            self.index = max(0, self.index - 1)
        elif key == 'right':
            self.index = min(len(self.currLine), self.index + 1)
        elif key == 'up':
            if self.upTick > 0:
                self.upTick -= 1
                self.currLine = self.pastLines[self.upTick]
        elif key == 'down':
            if self.upTick < len(self.pastLines) - 1:
                self.upTick += 1
                self.currLine = self.pastLines[self.upTick]
        

    def onKeyPress(self, app, key, modifiers):
        # if in open mode, wait for file path input
        if self.openMode:
            if key == 'enter':
                path = self.currLine.strip()
                if path:
                    self.loadFile(path)
                    self.output(f"Opened {path}")
                self.openMode = False
                self.currLine = ""
            elif key == 'backspace':
                self.currLine = self.currLine[:-1]
            elif isinstance(key, str) and len(key) == 1:
                self.currLine += key
            return
        
        # check for control key combinations FIRST
        if key == "s" and 'control' in modifiers:
            self.saveFile()
            self.textLines = []
            self.output("File saved.")
            return
        elif key == "q" and 'control' in modifiers:
            self.output("Exiting nano editor.")
            self.app.modeManager.setMode('terminal')
            return
        elif key == 'o' and 'control' in modifiers:
            self.openMode = True
            self.textLines = []
            self.currLine = ""
            self.output('Type file path to open: ')
            return
        
        # override to handle text editing keys
        if key == "enter":
            # split current line at cursor position and move rest to new line
            if self.textLines:
                currentLine = self.textLines[self.indexY]
                self.textLines[self.indexY] = currentLine[:self.index]
                self.textLines.insert(self.indexY + 1, currentLine[self.index:])
                self.indexY += 1
                self.index = 0
            else:
                self.textLines.append("")
        elif key == "backspace":
            if self.textLines:
                if self.index > 0:
                    # delete character before cursor in current line
                    self.textLines[self.indexY] = self.textLines[self.indexY][:self.index - 1] + self.textLines[self.indexY][self.index:]
                    self.index -= 1
                elif self.indexY > 0:
                    # merge with previous line
                    prevLine = self.textLines[self.indexY - 1]
                    self.index = len(prevLine)
                    self.textLines[self.indexY - 1] = prevLine + self.textLines[self.indexY]
                    self.textLines.pop(self.indexY)
                    self.indexY -= 1
        elif key == 'delete':
            if self.textLines and self.index < len(self.textLines[self.indexY]):
                # delete character at cursor
                self.textLines[self.indexY] = self.textLines[self.indexY][:self.index] + self.textLines[self.indexY][self.index + 1:]
        elif key == 'space':
            if not self.textLines:
                self.textLines.append("")
            self.textLines[self.indexY] = self.textLines[self.indexY][:self.index] + ' ' + self.textLines[self.indexY][self.index:]
            self.index += 1
        elif isinstance(key, str) and len(key) == 1:
            if not self.textLines:
                self.textLines.append("")
            self.textLines[self.indexY] = self.textLines[self.indexY][:self.index] + key + self.textLines[self.indexY][self.index:]
            self.index += 1
        elif key == "up":
            if self.indexY > 0:
                self.indexY -= 1
                # clamp index to new line's length
                if self.index > len(self.textLines[self.indexY]):
                    self.index = len(self.textLines[self.indexY])
                
        elif key == "down":
            if self.indexY < len(self.textLines) - 1:
                self.indexY += 1
                # clamp index to new line's length
                if self.index > len(self.textLines[self.indexY]):
                    self.index = len(self.textLines[self.indexY])
        elif key == "left":
            self.index = max(0, self.index - 1) 

        elif key == "right":
            if self.textLines and self.index < len(self.textLines[self.indexY]):
                self.index += 1 
    def draw(self, app):
        # recalculate all dimensions on each draw to handle window resizes
        self.w = self.w
        self.h = self.h
        self.fontSize = max(12, int(self.w * 0.018))
        self.lineSpacing = self.fontSize * 1.3
        self.margin = self.w * 0.015

        # draw editor background
        drawRect(self.x, self.y, self.w, self.h, fill=self.backgroundColor)
        
        # draw nano editor interface
        for i, line in enumerate(self.textLines):
            if i * self.lineSpacing + self.margin < self.h - self.margin - self.lineSpacing:
                drawLabel(line, self.x + self.margin, self.y + self.margin + i * self.lineSpacing,
                    size=self.fontSize, fill=self.textColor, font='monospace', align='left')
                
        # draw nano footer
        footerY = self.h - self.margin - self.lineSpacing
        drawRect(self.x, footerY, self.w, self.lineSpacing, fill='grey')
        drawLabel("^O Open  ^S Save  ^Q Quit", self.x + self.margin, footerY + (self.lineSpacing - self.fontSize) / 2,
            size=self.fontSize, fill='red', font='monospace', align='left')
        # draw cursor at index
        if self.textLines:
            self.drawCursor(app)
    def drawCursor(self, app):
        # get the current line being edited
        if self.indexY >= len(self.textLines):
            self.indexY = len(self.textLines) - 1
        
        currentLine = self.textLines[self.indexY]
        
        # clamp index to current line length
        if self.index > len(currentLine):
            self.index = len(currentLine)
        
        # calculate cursor position based on index within current line
        textToMeasure = currentLine[:self.index]
        
        # calculate y position based on line number
        cursorY = self.y + self.margin + self.indexY * self.lineSpacing + (self.lineSpacing - self.fontSize) / 2 + self.cursorCalibration

        # show cursor half the time
        if app.tick % 72 > 36:
            cursorX = self.x + self.margin + len(textToMeasure) * (self.fontSize * 0.6) 
            drawRect(cursorX, cursorY, self.fontSize * 0.45, self.fontSize, fill='white')
            try : 
                letter = currentLine[self.index]
            except IndexError:
                letter = ' '
            drawLabel(letter, cursorX, cursorY + (self.lineSpacing - self.fontSize) / 2 + 2 * self.cursorCalibration, size=self.fontSize, fill='purple', font='monospace', align='left')


