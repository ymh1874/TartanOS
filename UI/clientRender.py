class ClientRender:
    # later be used to render different application clients
    def __init__(self, app):
        self.app = app

    def fileExplorerClient(self, x, y, width, height, align):
        self.app.windowManager.windowClient("File Explorer", x, y, width, height, align)

    def textEditorClient(self, x, y, width, height, align):
        self.app.windowManager.windowClient("Text Editor", x, y, width, height, align)

    def terminalClient(self, x, y, width, height, align):
        self.app.windowManager.windowClient("Terminal", x, y, width, height, align)

    