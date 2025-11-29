# systems/fileSystem.py

class FileSystem:
    def __init__(self):
        self.fs = {
            "/": {
                "type": "folder",
                "children": ["home", "bin", "tmp"],
                "permissions": "755"
            },
            "/home": {
                "type": "folder",
                "children": ["yousef", "shared", "desktop"],
                "permissions": "755"
            },
            "/home/yousef": {
                "type": "folder",
                "children": ["notes.txt", "projects"],
                "permissions": "755"
            },
            "/home/yousef/notes.txt": {
                "type": "file",
                "content": "meow",
                "permissions": "644"
            },
            "/home/yousef/projects": {
                "type": "folder",
                "children": ["binfile.a"],
                "permissions": "755"
            },
            "/home/yousef/projects/binfile.a": {
                "type": "file",
                "content": "0101010",
                "permissions": "644"
            },
            "/home/shared": {
                "type": "folder",
                "children": [],
                "permissions": "755"
            },
            "/home/desktop": {
                "type": "folder",
                "children": ["welcome.txt", "projects"],
                "permissions": "755"
            },
            "/home/desktop/welcome.txt": {
                "type": "file",
                "content": "Welcome to TartanOS!",
                "permissions": "644"
            },
            "/home/desktop/projects": {
                "type": "folder",
                "children": ["binfile.a"],
                "permissions": "755"
            },
            "/home/desktop/projects/binfile.a": {
                "type": "file",
                "content": "0101010",
                "permissions": "644"
            },
            "/bin": {
                "type": "folder",
                "children": [],
                "permissions": "755"
            },
            "/tmp": {
                "type": "folder",
                "children": [],
                "permissions": "755"
            }
        }

    def get(self, path):
        return self.fs.get(path, None)

    def exists(self, path):
        return path in self.fs

    def isFile(self, path):
        node = self.fs.get(path)
        return node is not None and node.get("type") == "file"

    def isFolder(self, path):
        node = self.fs.get(path)
        return node is not None and node.get("type") == "folder"
    
    def getChildren(self, path):
        # Get list of children for a folder
        node = self.fs.get(path)
        if node and node.get("type") == "folder":
            return node.get("children", [])
        return []
    
    def getDesktopFiles(self):
        # Get files and folders in /home/desktop
        desktopFiles = []
        desktopPath = "/home/desktop"
        children = self.getChildren(desktopPath)
        
        for fileName in children:
            filePath = f"{desktopPath}/{fileName}"
            if self.isFile(filePath):
                desktopFiles.append((fileName, 'file'))
            elif self.isFolder(filePath):
                desktopFiles.append((fileName, 'folder'))
        return desktopFiles
    
    def createFile(self, path, content=""):
        # Create a new file
        node = {"type": "file", "content": content, "permissions": "644"}
        self.fs[path] = node
        self.updateParentChildren(path, add=True)
    
    def createFolder(self, path):
        # Create a new folder
        node = {"type": "folder", "children": [], "permissions": "755"}
        self.fs[path] = node
        self.updateParentChildren(path, add=True)
    
    def deleteFile(self, path):
        # Delete a file
        if path in self.fs:
            del self.fs[path]
            self.updateParentChildren(path, add=False)
    
    def updateParentChildren(self, path, add=True):
        # Update parent folder's children list
        parentPath, fileName = self.splitPath(path)
        if parentPath in self.fs:
            node = self.fs[parentPath]
            if node.get("type") == "folder":
                children = node.get("children", [])
                if add and fileName not in children:
                    children.append(fileName)
                elif not add and fileName in children:
                    children.remove(fileName)
    
    def splitPath(self, path):
        # Split path into parent and filename
        parts = path.rsplit('/', 1)
        if len(parts) == 2:
            return parts[0] if parts[0] else "/", parts[1]
        return "/", parts[0] if parts[0] else ""