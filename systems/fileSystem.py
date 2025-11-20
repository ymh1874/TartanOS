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
                "shared": "folder"
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
                "type": "binary file"
            },
            "/home/yousef/notes.txt": {
                "type": "text file",
                "content": "meow"
            }
        }

    def get(self, path):
        return self.fs.get(path, None)

    def exists(self, path):
        return path in self.fs

    def isFile(self, path):
        return self.exists(path) and 'content' in self.fs[path]

    def isFolder(self, path):
        return self.exists(path) and isinstance(self.fs[path], dict)
