# systems/fileSystem.py

class FileSystem:
    def __init__(self):
        self.fs = {
            "/": {
                "home": "folder",
                "bin": "folder",
                "tmp": "folder"
            },
            "/home": {
                "yousef": "folder",
                "shared": "folder",
                "desktop": "folder"
    
            },
            "/home/yousef": {
                "notes.txt": "file",
                "projects": "folder"
            },
            "/home/yousef/projects": {
                "binfile.a": "file"
            },
            "/home/yousef/projects/binfile.a": {
                "content": "0101010",
                "type": "binary"
            },
            "/home/yousef/notes.txt": {
                "type": "text file",
                "content": "meow"
            },
            "/home/desktop": {
                "welcome.txt": {
                    "type": "file",
                    "content": "Welcome to TartanOS!"
                },
                "projects": "folder",
            },

            "/home/desktop/welcome.txt": {
                    "type": "file",
                    "content": "Welcome to TartanOS!"
            },
            "/home/desktop/projects": {
                "binfile.a": "file"
            }

        }

    def get(self, path):
        return self.fs.get(path, None)

    def exists(self, path):
        return path in self.fs

    def isFile(self, path):
        return self.exists(path) and 'content' in self.fs[path]

    def isFolder(self, path):
        return self.exists(path) and isinstance(self.fs[path], dict) and 'content' not in self.fs[path]
    
    def getDesktopFiles(self):
        desktopFiles = []
        desktopPath = "/home/desktop"
        desktopDir = self.fs.get(desktopPath, {})
        for fileName in desktopDir:
            filePath = f"{desktopPath}/{fileName}"
            if self.isFile(filePath):
                desktopFiles.append((fileName, 'file'))
            elif self.isFolder(filePath):
                desktopFiles.append((fileName, 'folder'))
        return desktopFiles                    