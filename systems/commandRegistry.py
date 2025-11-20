# systems/commandRegistry.py

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
            'gui': self.cmdGui
        }

    # ========== Commands ==========

    def cmdLs(self, args):
        self.term.output(' '.join(self.term.currFiles))

    def cmdCat(self, args):
        if not args:
            self.term.output("usage: cat <filename>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if not self.term.fs.exists(path):
            self.term.output("file not found")
            return

        node = self.term.fs.get(path)
        if "content" not in node:
            self.term.output("not a file")
            return

        for line in node["content"].splitlines():
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
        if not args:
            self.term.output("usage: touch <filename>")
            return

        name = args[0].lower()
        path = self.term.resolvePath(name)

        if path in self.term.fs.fs:
            self.term.output("already exists")
            return

        self.term.fs.fs[path] = {"content": ""}
        self.term.currFiles[name] = "file"
        self.term.output(f"created {name}")

    def cmdCd(self, args):
        if not args:
            self.term.output("usage: cd <folder>")
            return

        target = args[0].lower()
        newPath = self.term.resolvePath(target)

        if not self.term.fs.exists(newPath):
            self.term.output("no such directory")
            return

        if not isinstance(self.term.fs.get(newPath), dict):
            self.term.output("not a folder")
            return

        self.term.currPath = newPath
        self.term.currFiles = self.term.fs.get(newPath)

    def cmdPwn(self, args):
        self.term.output(self.term.currPath)

    def cmdStyle(self, args):
        if not args:
            self.term.output("usage: style <color>")
            return
        self.term.textColor = args[0]
        self.term.output(f"color changed to {args[0]}")

    def cmdGui(self, args):
        self.term.switchToGUI()
