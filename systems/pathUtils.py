# systems/pathUtils.py
class PathUtils:
    @staticmethod
    def getParent(path):
        if path == '/':
            return '/'
        temp = path.rstrip('/')
        idx = temp.rfind('/')
        return '/' if idx <= 0 else temp[:idx]

    @staticmethod
    def join(base, child):
        if base == '/':
            return f"/{child}"
        return f"{base}/{child}"
