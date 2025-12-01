# systems/commandRegistry.py - command registry system
# manages terminal commands and their execution
# provides implementations for various terminal commands
import sys
class CommandRegistry:
    def __init__(self, app):
        self.app = app
        self.term = None  # will be set after Terminal is created

        self.commands = {
            'ls': self.cmdLs,
            'cat': self.cmdCat,
            'clear': self.cmdClear,
            'help': self.cmdHelp,
            'whoami': self.cmdWhoami,
            'version': self.cmdVersion,
            'touch': self.cmdTouch,
            'cd': self.cmdCd,
            'pwn': self.cmdPwn,
            'style': self.cmdStyle,
            'mkdir': self.cmdMkdir,
            'rm': self.cmdRm,
            'backshot': self.cmdBackshot,
            'tartano': self.cmdNano,
            'mv': self.cmdMv,
            'rename': self.cmdRename,
        }

    # ===== Commands =====
    def cmdNano(self, term, args):
        # Open file editor
        if not args:
            term.output("usage: tartano <filename>")
            return

        name = args[0].lower()
        path = term.resolvePath(name)

        if not self.app.fs.exists(path):
            term.output("file not found")
            return

        if not self.app.fs.isFile(path):
            term.output("not a file")
            return

        term.output(f"Opening nano editor for {name}...")
        self.app.modeManager.setMode('nano', filePath=path)
    def cmdRename(self, term, args):
        # Rename a file or folder
        if len(args) < 2:
            term.output("usage: rename <oldname> <newname>")
            return

        oldName = args[0].lower()
        newName = args[1].lower()
        oldPath = term.resolvePath(oldName)
        newPath = term.resolvePath(newName)

        if not self.app.fs.exists(oldPath):
            term.output("source not found")
            return

        if self.app.fs.exists(newPath):
            term.output("destination already exists")
            return

        self.app.fs.moveFile(oldPath, newPath)
        term.output(f"renamed {oldName} to {newName}")
    def cmdLs(self, term, args):
        # List files in current directory
        children = self.app.fs.getChildren(term.currPath)
        if children:
            term.output(' '.join(children))
        else:
            term.output("<empty>")

    def cmdCat(self, term, args):
        # Display file contents
        if not args:
            term.output("usage: cat <filename>")
            return

        name = args[0].lower()
        path = term.resolvePath(name)

        if not self.app.fs.exists(path):
            term.output("file not found")
            return

        if not self.app.fs.isFile(path):
            term.output("not a file")
            return

        node = self.app.fs.get(path)
        content = node.get("content", "")
        if content == '':
            term.output("<empty>")
        else:
            for line in content.splitlines():
                term.output(line)

    def cmdClear(self, term, args):
        term.clear()

    def cmdHelp(self, term, args):
        for cmd in sorted(self.commands.keys()):
            term.output(cmd)

    def cmdWhoami(self, term, args):
        term.output(f"You are logged in as {term.username}")

    def cmdVersion(self, term, args):
        term.output("TartanOS v6.7")

    def cmdTouch(self, term, args):
        # Create a new empty file
        if not args:
            term.output("usage: touch <filename>")
            return

        name = args[0].lower()
        path = term.resolvePath(name)

        if self.app.fs.exists(path):
            term.output("already exists")
            return

        self.app.fs.createFile(path, "")
        term.output(f"created {name}")
    
    def cmdMv(self, term, args):
        # Move or rename a file or folder
        if len(args) < 2:
            term.output("usage: mv <source> <destination>")
            return

        sourceName = args[0].lower()
        destName = args[1].lower()
        sourcePath = term.resolvePath(sourceName)
        destPath = term.resolvePath(destName)

        if not self.app.fs.exists(sourcePath):
            term.output("source not found")
            return

        if self.app.fs.exists(destPath):
            term.output("destination already exists")
            return

        self.app.fs.moveFile(sourcePath, destPath)
        term.output(f"moved {sourceName} to {destName}")

    def cmdMkdir(self, term, args):
        # Create a new folder
        if not args:
            term.output("usage: mkdir <foldername>")
            return

        name = args[0].lower()
        path = term.resolvePath(name)

        if self.app.fs.exists(path):
            term.output("folder already exists")
            return

        self.app.fs.createFolder(path)
        term.output(f"created folder {name}")

    def cmdRm(self, term, args):
        # Remove a file or folder
        if not args:
            term.output("usage: rm <filename/foldername>")
            return

        name = args[0].lower()
        path = term.resolvePath(name)

        if not self.app.fs.exists(path):
            term.output("no such file or folder")
            return

        self.app.fs.deleteFile(path)
        term.output(f"removed {name}")

    def cmdCd(self, term, args):
        # Change directory
        if not args:
            term.output("usage: cd <folder>")
            return
        if args[0] == "..":
            if term.currPath == "/":
                return
            parentPath = '/'.join(term.currPath.split('/')[:-1])
            if parentPath == "":
                parentPath = "/"
            term.currPath = parentPath
            return
        target = args[0].lower()
        newPath = term.resolvePath(target)

        if not self.app.fs.exists(newPath):
            term.output("no such directory")
            return

        if not self.app.fs.isFolder(newPath):
            term.output("not a folder")
            return

        term.currPath = newPath

    def cmdPwn(self, term, args):
        term.output(term.currPath)

    def cmdStyle(self, term, args):
        if not args:
            term.output("usage: style <color>")
            return
        term.textColor = args[0]
        term.output(f"color changed to {args[0]}")

    def cmdGui(self, term, args):
        # not used anymore
        term.output("Switching to GUI mode...")
        self.app.modeManager.setMode('desktop')

    def cmdBackshot(self, term, args):
        term.output("Bye Bye...")
        sys.exit()
