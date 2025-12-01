# ui/clientRender.py - manages rendering of different application clients within windows
# supports Terminal, NanoEditor, FileExplorer clients
# creates and maintains client instances per window
class ClientRender:
    # render different application clients within windows
    def __init__(self, app):
        self.app = app
        self.winMngr = self.app.windowManager
        self.windowClients = {}  # store instances of clients for each window

    def terminalClient(self, windowName, x, y, width, height, align):
        # create or retrieve terminal instance for this window
        if windowName not in self.windowClients:
            # convert center-aligned coordinates to top-left for terminal
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            # create terminal instance with window-relative coordinates
            self.windowClients[windowName] = self.app.Terminal(
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
            # convert center-aligned coordinates to top-left for editor
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            # create nano editor instance with window-relative coordinates
            if windowName == "Tartano":
                # create new file
                self.app.fs.createFile("/home/desktop/untitled.txt", "")
                newfilePath = "/home/desktop/untitled.txt"
            else:
                newfilePath = f"/home/desktop/{windowName}"
            self.windowClients[windowName] = self.app.NanoEditor(
                newfilePath,
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

    def fileExplorerClient(self, windowName, path, x, y, width, height, align):
        # render file explorer content
        from cmu_graphics import drawLabel
        # create or retrieve nano editor instance for this window
        if windowName not in self.windowClients:
            # convert center-aligned coordinates to top-left for editor
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            path = path if path is not None else "/home"
            self.windowClients[windowName] = self.app.FileExplorer(
                self.app,
                x=topLeftX,
                y=topLeftY,
                width=width,
                height=height,
                path=path
            )
        
        # get file explorer instance
        explorerClient = self.windowClients[windowName]
        
        # convert center-aligned coordinates to top-left for explorer
        if align == 'center':
            topLeftX = x - width // 2
            topLeftY = y - height // 2
        else:
            topLeftX = x
            topLeftY = y
        
        # update dimensions in case window was resized
        explorerClient.x = topLeftX
        explorerClient.y = topLeftY
        explorerClient.width = width
        explorerClient.height = height
        
        # draw the explorer client
        explorerClient.draw(self.app)
        
    
    def changeDimensions(self, clientName, x, y, width, height, align):
        # update client dimensions on window resize
        if clientName in self.windowClients:
            client = self.windowClients[clientName]
            # convert center-aligned coordinates to top-left
            if align == 'center':
                topLeftX = x - width // 2
                topLeftY = y - height // 2
            else:
                topLeftX = x
                topLeftY = y
            
            client.x = topLeftX
            client.y = topLeftY
            client.w = width
            client.h = height
            
            # recalculate visual properties based on new dimensions
            client.fontSize = max(12, int(client.w * 0.018))
            client.lineSpacing = client.fontSize * 1.3
            client.margin = client.w * 0.02

    def instantClient(self, clientName, x, y, width, height, align):
        # route to appropriate client renderer based on window name
        if clientName == "Terminal":
            self.terminalClient(clientName, x, y, width, height, align)
        elif clientName == "File Explorer": 
            self.fileExplorerClient(clientName, None, x, y, width, height, align)
        elif clientName == "Tartano":
            self.textEditorClient(clientName, x, y, width, height, align)
        elif clientName.endswith('.txt'):
            # text editor for .txt files
            self.textEditorClient(clientName, x, y, width, height, align)
        else:
            # default to file explorer for folders
            path = f"/home/desktop/{clientName}"
            self.fileExplorerClient(clientName, path, x, y, width, height, align)
    
    def handleClientKeyPress(self, clientName, app, key, modifiers):
        # route keyboard input to the appropriate client
        if clientName is not None:
            # Create client on demand if it doesn't exist yet
            if clientName not in self.windowClients:
                # Get window data to retrieve dimensions
                if clientName in app.windowManager.windows:
                    windowData = app.windowManager.windows[clientName]
                    x, y, w, h = app.windowManager.getActualDimensions(windowData, app)
                    # Create the client
                    if clientName == "Terminal":
                        self.terminalClient(clientName, x, y, w, h, windowData['align'])
                    elif clientName.endswith('.txt'):
                        self.textEditorClient(clientName, x, y, w, h, windowData['align'])
                    elif clientName == "File Explorer":
                        self.fileExplorerClient(clientName, x, y, w, h, windowData['align'])
            
            # Handle window snapping with Ctrl+Left and Ctrl+Right
            if modifiers == ['control'] and key == 'left':
                print(f"Snapping {clientName} to left half")
                # Snap to left half: center at 25% of screen, width 50%
                app.windowManager.resizeWindow(
                    clientName,
                    0.5,    # 50% width
                    1.0,    # full height
                    0.25,   # center at 25% x
                    0.5     # center at 50% y
                )
                return
            elif modifiers == ['control'] and key == 'right':
                print(f"Snapping {clientName} to right half")
                # Snap to right half: center at 75% of screen, width 50%
                app.windowManager.resizeWindow(
                    clientName,
                    0.5,    # 50% width
                    1.0,    # full height
                    0.75,   # center at 75% x
                    0.5     # center at 50% y
                )
                return
            elif modifiers == ['control'] and key == 'up':
                print(f"Maximizing {clientName}")
                # Maximize window
                app.windowManager.resizeWindow(
                    clientName,
                    1.0,    # full width
                    1.0,    # full height
                    0.5,    # center at 50% x
                    0.5     # center at 50% y
                )
                return
            elif modifiers == ['control'] and key == 'down':
                print(f"Restoring {clientName} to original size")
                # Restore window to original size (assumed 0.5x0.5 at center)
                app.windowManager.resizeWindow(
                    clientName,
                    0.5,    # 50% width
                    0.5,    # 50% height
                    0.5,    # center at 50% x
                    0.5     # center at 50% y
                )
                return
            
            # Now handle the keypress for the client
            if clientName in self.windowClients:
                if clientName == "Terminal":
                    self.windowClients[clientName].onKeyPress(app, key, modifiers)
                elif clientName == "Tartano":
                    if modifiers == ['control'] and key == 'q':
                        print("Closing Tartano editor")
                        # close the editor window on Ctrl+Q
                        app.windowManager.closeWindow(clientName)
                        self.closeClient(clientName)
                        return
                    self.windowClients[clientName].onKeyPress(app, key, modifiers)
                elif clientName.endswith('.txt'):
                    # text editor receives keyboard input
                    if modifiers == ['control'] and key == 'q':
                        print("Closing Tartano editor")
                        # close the editor window on Ctrl+Q
                        app.windowManager.closeWindow(clientName)
                        self.closeClient(clientName)
                        return
                    self.windowClients[clientName].onKeyPress(app, key, modifiers)
                elif clientName == "File Explorer":
                    self.windowClients[clientName].onKeyPress(app, key, modifiers)
                else:
                    try: self.windowClients[clientName].onKeyPress(app, key, modifiers)
                    except: pass
    def onMousePress(self, clientName, app, mouseX, mouseY):
        # route mouse input to the appropriate client
        if clientName in self.windowClients:
            if clientName == "File Explorer":
                self.windowClients[clientName].onMousePress(app, mouseX, mouseY)  
            elif clientName == "Tartano":
                pass
            elif clientName.endswith('.txt'):
                pass
            elif clientName == "Terminal":
                pass
            else:
                self.windowClients[clientName].onMousePress(app, mouseX, mouseY)             
    def closeClient(self, clientName):
        # cleanup when closing a window
        if clientName in self.windowClients:
            del self.windowClients[clientName]