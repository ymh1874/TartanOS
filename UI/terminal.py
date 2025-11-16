from cmu_graphics import *


class terminal():
    def __init__(self, app):
        self.textColor = 'white'
        self.backgroundColor = 'black'
        self.username = app.loginPage.username
        self.prompt = '> '
        self.maxLines = 200
        self.fontSize = max(20, int(app.width * 0.018))
        self.lineSpacing = self.fontSize * 1.3
        self.margin = app.width * 0.02
        self.textLines = [f'Welcome to TartanOS {app.loginPage.username}!']
        self.currLine = ''
        self.files = {
            'desktop':
                {'folder1' : 
                    {'secret.txt': None, 
                    'folder3' : 
                         {'good': None}},
                'readme.txt': 'This is a sample readme file.\nFeel free to edit it!',
                'notes.txt': 'These are some sample notes.\nRemember to check them later.'
                }
        }
        app.path = []
        self.currfiles = self.files

        self.commands = {
            'ls': self.cmdLs,
            'cat': self.cmdCat,
            'clear': self.cmdClear,
            'help': self.cmdHelp,
            'whoami': self.cmdWhoami,
            'version': self.cmdVersion,
            'txt': self.cmdTxt, 
            'style': self.cmdStyle,
            'touch': self.cmdTouch,
            'gui': self.cmdGui,
            'cd': self.cmdCd,
            'pwn': self.cmdPwn
        }

    def draw(self, app):
        # Terminal body
        drawRect(0, 0, app.width, app.height, fill=self.backgroundColor)

        availableLines = int((app.height - (self.margin * 2)) // self.lineSpacing)
        history = self.textLines[-availableLines:]

        for i, line in enumerate(history):
            y = self.margin + i * self.lineSpacing
            drawLabel(line, self.margin, y, size=self.fontSize, fill=self.textColor,
                      font='monospace', align='left')

        currentY = self.margin + len(history) * self.lineSpacing
        drawLabel(f'{self.prompt}{self.currLine}', self.margin, currentY,
                  size=self.fontSize, fill=self.textColor, font='monospace', align='left')
        self.drawCursor()

    def drawCursor(self):
        # location indicator for terminal
        if app.tick %  72 > 36:
            cursorX = self.margin + len(self.prompt + self.currLine) * (self.fontSize * 0.6)
            cursorY = len(self.textLines) * self.lineSpacing
            drawRect(cursorX, cursorY, 10, self.fontSize, fill=self.textColor)


    def onKeyPressTerminal(self, app, key, modifiers):
        if key == 'enter':
            command = self.currLine.strip()
            self.textLines.append(f'{self.prompt}{self.currLine}')
            self.currLine = ''

            if command:
                self.executeCommand(command)
            self.trimHistory()
        elif key == 'backspace':
            self.currLine = self.currLine[:-1]
        elif key == 'space':
            self.currLine += ' '
        elif len(key) == 1:
            self.currLine += key

    def executeCommand(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        handler = self.commands.get(cmd)

        if handler:
            handler(args)
        else:
            self.textLines.append(f'command not found: {cmd}')

    def cmdLs(self, _):
        if self.path == []:
            self.textLines.append('Main Directory')
            return
        self.textLines.append('  '.join(sorted(self.currfiles.keys())))

    def cmdCat(self, args):
        if not args:
            self.textLines.append('usage: cat <filename>')
            return
        
        filename = args[0].lower()
        content = self.files.get(filename)

        if content:
            for line in content.splitlines():
                self.textLines.append(line)
        else:
            self.textLines.append(f'cat: {filename}: file not found')
    def cmdTouch(self, args):
        if not args:
            self.textLines.append('usage: touch <filename>')
            return

        filename = args[0].lower()
        if filename in self.currfiles:
            self.textLines.append(f'touch: {filename}: file already exists')
        else:
            self.currfiles[filename] = 'null'
            self.textLines.append(f'Created file: {filename}')
    def cmdCd(self, args):

        if not args:
            self.textLines.append('usage: cd <foldername>')

        else:
            print(app.path)
            foldername = args[0].lower()
            if foldername == '`':
                self.currfiles = self.files
                app.path = []
            elif foldername == '..':
                if app.path == []:
                    self.textLines.append('Already at main directory')
                    return
                self.currfiles = self.getParentPath(self.currfiles)
                app.path.pop()
            elif foldername not in self.currfiles:
                self.textLines.append(f'Folder does not exist')
            elif self.currfiles[foldername] == None:
                self.textLines.append('This is not a folder!')
            else: 
                self.currfiles = self.currfiles[foldername]
                app.path.append(foldername)
            
                
    def getParentPath(self, currentPath):
        # get parent directory
        parentPath = ''
        for i in range(len(app.path)):
            if app.path[i] == currentPath:
                 parentPath = app.path[i - 1]
        return parentPath
    
    def getcurrPath(self):
        return '/'.join(app.path) if app.path else 'desktop'
    
    def cmdPwn(self, _):
        self.textLines.append(self.getcurrPath())


    def cmdClear(self, _):
        self.textLines = []

    def cmdHelp(self, _):
        self.textLines.append('available commands:')
        for name in sorted(self.commands.keys()):
            self.textLines.append(f'  {name}')

    def cmdWhoami(self, _):
        self.textLines.append(f'You are logged in as {self.username}.')

    def cmdVersion(self, _):
        self.textLines.append('TartanOS version 1.0.0')

    def cmdTxt(self, args):
        if not args:
            self.textLines.append('usage: txt <filename>')
            return

        filename = args[0].lower()
        if filename in self.files:
            self.textLines.append(f'Opening {filename} in text editor... (not implemented)')
            #self.textEditor(self.files[filename])
        else:
            self.textLines.append(f'txt: {filename}: file not found')
    def cmdStyle(self, args):
        if not args:
            self.textLines.append('usage: style <colorname>')
            return

        color = args[0].lower()
        validColors = ['white', 'green', 'lightgreen', 'red', 'blue', 'yellow', 'cyan', 'magenta']

        if color in validColors:
            self.textColor = color
            self.textLines.append(f'Text color changed to {color}.')
        else:
            self.textLines.append(f'color: {color}: invalid color. Valid colors are: {", ".join(validColors)}')
            
    def cmdGui(self, _):
        app.screen = 'desktop'

    def textEditor(self, content):
          drawRect(0, 0, app.width, app.height, fill='black')
          drawLabel('Text Editor', app.width / 2, app.height / 2,
                    size=30, fill='white', font='monospace', align='center')

    def trimHistory(self):
        overflow = len(self.textLines) - self.maxLines
        if overflow > 0:
            self.textLines = self.textLines[overflow:]
