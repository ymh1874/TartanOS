class ClientRender:
    # render different application clients within windows
    def __init__(self, app):
        self.app = app
        self.windowClients = {}  # store instances of clients for each window

    def terminalClient(self, windowName, x, y, width, height, align):
        # create or retrieve terminal instance for this window
        if windowName not in self.windowClients:
            from ui.terminal.terminal import Terminal
            # convert center-aligned coordinates to top-left for terminal
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            # create terminal instance with window-relative coordinates
            self.windowClients[windowName] = Terminal(
                self.app,
                x=topLeftX,
                y=topLeftY,
                width=width,
                height=height,
            )
        
        # get terminal instance
        terminalClient = self.windowClients[windowName]
        
        # convert center-aligned coordinates to top-left for terminal
        if align == 'center':
            topLeftX = x - width // 2
            topLeftY = y - height // 2
        else:
            topLeftX = x
            topLeftY = y
        
        # update dimensions in case window was resized
        terminalClient.x = topLeftX
        terminalClient.y = topLeftY
        terminalClient.w = width
        terminalClient.h = height
        
        # recalculate visual properties based on new dimensions
        terminalClient.fontSize = max(12, int(terminalClient.w * 0.018))
        terminalClient.lineSpacing = terminalClient.fontSize * 1.3
        terminalClient.margin = terminalClient.w * 0.02
        
        # draw the terminal client
        terminalClient.draw(self.app)

    def textEditorClient(self, windowName, x, y, width, height, align):
        # create or retrieve nano editor instance for this window
        if windowName not in self.windowClients:
            from ui.terminal.terminal import NanoEditor
            # convert center-aligned coordinates to top-left for editor
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            # create nano editor instance with window-relative coordinates
            # extract file path from windowName if it's a .txt file
            filePath = f"/home/desktop/{windowName}"
            self.windowClients[windowName] = NanoEditor(
                filePath,
                self.app,
                x=topLeftX,
                y=topLeftY,
                width=width,
                height=height,
            )
        
        # get nano editor instance
        editorClient = self.windowClients[windowName]
        
        # convert center-aligned coordinates to top-left for editor
        if align == 'center':
            topLeftX = x - width // 2
            topLeftY = y - height // 2
        else:
            topLeftX = x
            topLeftY = y
        
        # update dimensions in case window was resized
        editorClient.x = topLeftX
        editorClient.y = topLeftY
        editorClient.w = width
        editorClient.h = height
        
        # recalculate visual properties based on new dimensions
        editorClient.fontSize = max(12, int(editorClient.w * 0.018))
        editorClient.lineSpacing = editorClient.fontSize * 1.3
        editorClient.margin = editorClient.w * 0.02
        
        # draw the editor client
        editorClient.draw(self.app)

    def fileExplorerClient(self, x, y, width, height, align):
        # render file explorer content
        from cmu_graphics import drawLabel
        drawLabel("File Explorer Client", x, y, size=14, fill='black', align=align)

    


    def instantClient(self, clientName, x, y, width, height, align):
        # route to appropriate client renderer based on window name
        if clientName == "Terminal":
            self.terminalClient(clientName, x, y, width, height, align)
        elif clientName == "File Explorer": 
            self.fileExplorerClient(x, y, width, height, align)
        elif clientName.endswith('.txt'):
            # text editor for .txt files
            self.textEditorClient(clientName, x, y, width, height, align)
    
    def handleClientKeyPress(self, clientName, app, key, modifiers):
        # route keyboard input to the appropriate client
        if clientName == "Terminal" and clientName in self.windowClients:
            self.windowClients[clientName].onKeyPress(app, key, modifiers)
        elif clientName.endswith('.txt') and clientName in self.windowClients:
            # text editor receives keyboard input
            if modifiers == ['control'] and key == 'q':
                # close the editor window on Ctrl+Q
                app.windowManager.closeWindow(clientName)
                self.closeClient(clientName)
            self.windowClients[clientName].onKeyPress(app, key, modifiers)
    
    def closeClient(self, clientName):
        # cleanup when closing a window
        if clientName in self.windowClients:
            del self.windowClients[clientName]