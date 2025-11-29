# systems/commandRegistry.py
import sys
class CommandRegistry:
    def __init__(self, terminal):
        self.term = terminal

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
            'gui': self.cmdGui,
            'mkdir': self.cmdMkdir,
            'rm': self.cmdRm,
            'backshot': self.cmdBackshot,
            'tartano': self.cmdNano
        }

    # ===== Commands =====
    def cmdNano(self, args):
        # Open file editor
        if not args:
            self.term.output("usage: tartano <filename>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if not self.term.fs.exists(path):
            self.term.output("file not found")
            return

        if not self.term.fs.isFile(path):
            self.term.output("not a file")
            return

        self.term.output(f"Opening nano editor for {name}...")
        self.term.app.modeManager.setMode('nano', filePath=path)
    def cmdLs(self, args):
        # List files in current directory
        children = self.term.fs.getChildren(self.term.currPath)
        if children:
            self.term.output(' '.join(children))
        else:
            self.term.output("")

    def cmdCat(self, args):
        # Display file contents
        if not args:
            self.term.output("usage: cat <filename>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if not self.term.fs.exists(path):
            self.term.output("file not found")
            return

        if not self.term.fs.isFile(path):
            self.term.output("not a file")
            return

        node = self.term.fs.get(path)
        content = node.get("content", "")
        for line in content.splitlines():
            self.term.output(line)

    def cmdClear(self, args):
        self.term.clear()

    def cmdHelp(self, args):
        for cmd in sorted(self.commands.keys()):
            self.term.output(cmd)

    def cmdWhoami(self, args):
        self.term.output(f"You are logged in as {self.term.username}")

    def cmdVersion(self, args):
        self.term.output("TartanOS v1.0")

    def cmdTouch(self, args):
        # Create a new empty file
        if not args:
            self.term.output("usage: touch <filename>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if self.term.fs.exists(path):
            self.term.output("already exists")
            return

        self.term.fs.createFile(path, "")
        self.term.output(f"created {name}")

    def cmdMkdir(self, args):
        # Create a new folder
        if not args:
            self.term.output("usage: mkdir <foldername>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if self.term.fs.exists(path):
            self.term.output("already exists")
            return

        self.term.fs.createFolder(path)
        self.term.output(f"created folder {name}")

    def cmdRm(self, args):
        # Remove a file or folder
        if not args:
            self.term.output("usage: rm <filename/foldername>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if not self.term.fs.exists(path):
            self.term.output("no such file or folder")
            return

        self.term.fs.deleteFile(path)
        self.term.output(f"removed {name}")

    def cmdCd(self, args):
        # Change directory
        if not args:
            self.term.output("usage: cd <folder>")
            return
        if args[0] == "..":
            if self.term.currPath == "/":
                return
            parentPath = '/'.join(self.term.currPath.split('/')[:-1])
            if parentPath == "":
                parentPath = "/"
            self.term.currPath = parentPath
            return
        target = args[0].lower()
        newPath = self.term.resolvePath(target)

        if not self.term.fs.exists(newPath):
            self.term.output("no such directory")
            return

        if not self.term.fs.isFolder(newPath):
            self.term.output("not a folder")
            return

        self.term.currPath = newPath

    def cmdPwn(self, args):
        self.term.output(self.term.currPath)

    def cmdStyle(self, args):
        if not args:
            self.term.output("usage: style <color>")
            return
        self.term.textColor = args[0]
        self.term.output(f"color changed to {args[0]}")

    def cmdGui(self, args):
        self.term.output("Switching to GUI mode...")
        self.term.app.modeManager.setMode('desktop')

    def cmdBackshot(self, args):
        sys.exit()
