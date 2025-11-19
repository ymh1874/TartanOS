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
        self.pastLines = []
        self.currPath = '/'
        self.fileSys = {
                        "/": {
                            "home": "folder",
                            "bin": "folder",
                            "tmp": "folder"
                        },

                        "/home": {
                            "yousef": "folder",
                            "shared": "folder"
                        },

                        "/home/yousef": {
                            "notes.txt": "file",
                            "projects": "folder"
                        },
                        '/home/yousef/projects': {
                            'binfile.a' : 'file'
                        },
                        '/home/yousef/projects/binfile.a': {
                            'content' : '0101010',
                            'type' : 'binary file'
                        },

                        "/home/yousef/notes.txt": {
                            "type": "text file",
                            "content": "meow"
                        }
                    }

        
        self.currfiles = self.fileSys[self.currPath]

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

        # traverse Behaviour
        self.upTick = 0

        # text editor vars
        self.editorState = False

          

    def __str__(self):
        return f''

    def executeCommand(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        handler = self.commands.get(cmd)

        if handler:
            handler(args)
        else:
            self.textLines.append(f'command not found: {cmd}')

    # Command Handlers

    def cmdLs(self, _):
        self.textLines.append(' '.join(self.currfiles))
        return

    def cmdCat(self, args):

        if not args:
            self.textLines.append('usage: cat <filename>')
            return
        
        filename = args[0].lower()
        if filename.startswith('/'):
                if filename in self.fileSys:
                    if 'content' not in self.fileSys[filename]:
                        self.textLines.append('not a file')
                    data = self.fileSys[filename]['content']
                    for line in data.splitlines():
                        self.textLines.append(line)
                    return
                else:
                    self.textLines.append('file not found')
                    return
                
        filePath = f"{self.currPath.rstrip('/')}/{filename}"
        print(filePath)
        if filePath not in self.fileSys:
            self.textLines.append(f'{filename}: file not found')
            return
        data = self.fileSys[filePath]['content']
        for line in data.splitlines():
            self.textLines.append(line)
            return
            

    def cmdTouch(self, args):
        if not args:
            self.textLines.append('usage: touch <filename>')
            return

        filename = args[0].lower()
        newPath = f'{self.currPath.rstrip('/')}/{filename}'
        if filename in self.currfiles:
            self.textLines.append(f'touch: {filename}: file already exists')
        else:
            self.currfiles[filename] = 'file'
            self.fileSys[newPath] = {'content': 'None', 'type': 'text file'}
            self.textLines.append(f'Created file: {filename}')

    def cmdCd(self, args):

        if not args:
            self.textLines.append('usage: cd <foldername>')
        else:
            folderName = args[0].lower()
            
            if folderName == '/':
                self.currPath = '/'
                self.currfiles = self.fileSys['/']
                return

            elif folderName == '..':
                if self.currPath == '/':
                    self.textLines.append('Already at main directory')
                    return
                else:   
                    self.currPath = self.getParentPath(self.currPath)
                    self.currfiles = self.fileSys[self.currPath]
                    print(self.currPath)
                    print(self.currfiles)
                    return
            elif folderName.startswith('/'):
                if folderName in self.fileSys:
                    self.currPath = folderName
                    self.currfiles = self.fileSys[folderName]
                    print(self.currPath)
                    print(self.currfiles)
                else:
                    self.textLines.append('Invalid Path')
            elif folderName not in self.currfiles:
                self.textLines.append(f'Does not exist')
                return

            elif self.currfiles[folderName] != 'folder':
                self.textLines.append('This is not a folder!')
                return

            else: 
                # rstrip for cases where path is root
                newPath = f'{self.currPath.rstrip('/')}/{folderName}'
                if newPath not in self.fileSys:
                    self.textLines.append('Path does not exist (not created)')
                    return
                self.currfiles = self.fileSys[newPath]
                self.currPath = newPath
                print(self.currPath)
                print(self.currfiles)
                return
            
                
    def getParentPath(self, path):
        if path == '/':
            return '/'

        # remove trailing slash except root
        temp = path.rstrip('/')

        # find last slash
        idx = temp.rfind('/')
        if idx <= 0:
            return '/'  
        return temp[:idx]

    def cmdPwn(self, _):
        self.textLines.append(self.getcurrPath())

    def getcurrPath(self):
        return self.currPath

    def cmdClear(self, _):
        self.textLines = []

    def cmdHelp(self, _):
        self.textLines.append('available commands:')
        for name in sorted(self.commands.keys()):
            self.textLines.append(f'{name}')

    def cmdWhoami(self, _):
        self.textLines.append(f'You are logged in as {self.username}.')

    def cmdVersion(self, _):
        self.textLines.append('TartanOS version 1.0.0')

    def cmdTxt(self, args):
        if not args:
            self.textLines.append('usage: txt <filename>')
            return

        filename = args[0].lower()
        interface = args[1].lower()
        if filename in self.currfiles and interface == '-t':
            self.textEditor(filename)
        elif filename in self.currfiles and interface == '-i':
            self.textLines.append(f'not implemented yet')
        else:
            self.textLines.append(f'txt: {filename}: file not found')

    def textEditor(self, content):
            self.editorState = True
            drawRect(0, 0, app.width, app.height, fill='black')
            drawLabel('Text Editor', app.width / 2, app.height / 2,
                        size=30, fill='white', font='monospace', align='center')


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
    #########################
    # draw func
    ##########################
    def draw(self, app):
        # Terminal body
        if self.editorState:
            self.editorTerminal(self, app)

        else:
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

    def editorTerminal(self, app):
        drawRect(0, 0, app.width, app.height)
        drawLabel('Controls', self.margin, app.height * 0.9, size = self.fontSize, fill = self.textColor)
    
    ###########################################
    ###########################################

    def trimHistory(self):
        overflow = len(self.textLines) - self.maxLines
        if overflow > 0:
            self.textLines = self.textLines[overflow:]

    

    def onKeyPressTerminal(self, app, key, modifiers):
        if key == 'enter':
            command = self.currLine.strip()
            self.pastLines.append(self.currLine)
            print(self.pastLines)
            self.textLines.append(f'{self.prompt}{self.currLine}')
            self.currLine = ''
            self.upTick = len(self.pastLines)

            if command:
                self.executeCommand(command)
            self.trimHistory()
        elif key == 'backspace':
            self.currLine = self.currLine[:-1]
        elif key == 'space':
            self.currLine += ' '
        elif key == 'up':
            if self.upTick > 0:
                self.upTick -= 1
                self.currLine = self.pastLines[self.upTick]
        elif key == 'down':
            if self.upTick < len(self.pastLines) -1:
                self.upTick += 1
                self.currLine = self.pastLines[self.upTick]
        elif len(key) == 1:
            self.currLine += key
