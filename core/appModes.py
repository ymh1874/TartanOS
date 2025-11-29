# core/appModes.py - manages different app states

class ModeManager:
    def __init__(self, app):
        self.app = app
        self.currentMode = None

    def setMode(self, modeName, **kwargs):
        # set current mode: 'login', 'desktop', 'nano', 'terminal'
        self.currentMode = modeName
        
        # initialize nanoEditor if switching to nano mode
        if modeName == 'nano' and 'filePath' in kwargs:
            from ui.terminal.terminal import NanoEditor
            self.app.terminal.nanoEditor = NanoEditor(kwargs['filePath'], self.app)

    def redraw(self, app, **kwargs):
        # render appropriate UI based on current mode
        if self.currentMode == 'login':
            app.loginPage.draw(app)
        elif self.currentMode == 'desktop':
            app.desktop.draw(app)
        elif self.currentMode == 'terminal':
            app.terminal.draw(app, **kwargs)
        elif self.currentMode == 'nano':
            if app.terminal.nanoEditor:
                app.terminal.nanoEditor.draw(app, **kwargs)

    def keyPress(self, app, key, modifiers):
        #  keyboard input to current mode
        if self.currentMode == 'login':
            app.loginPage.onKeyPress(app, key, modifiers)
        elif self.currentMode == 'desktop':
            # handle ctrl+t toggle for terminal
            app.desktop.onKeyPress(app, key, modifiers)
        elif self.currentMode == 'terminal':
            # allow ctrl+t from terminal to close it and return to desktop
            if modifiers == ['control'] and key == 't':
                app.desktop.terminalOpen = False
                self.setMode('desktop')
            else:
                app.terminal.onKeyPress(app, key, modifiers)
        elif self.currentMode == 'nano':
            if app.terminal.nanoEditor:
                app.terminal.nanoEditor.onKeyPress(app, key, modifiers)

    def keyHold(self, app, key, modifiers):
        # keyboard hold input to current mode
        if self.currentMode == 'terminal':
            app.terminal.onKeyHold(app, key, modifiers)
        elif self.currentMode == 'nano':
            if app.terminal.nanoEditor:
                app.terminal.nanoEditor.onKeyHold(app, key, modifiers)

    def mousePress(self, app, mouseX, mouseY):
        #  mouse input to current mode
        if self.currentMode == 'login':
            app.loginPage.onMousePress(app, mouseX, mouseY)
        elif self.currentMode == 'desktop':
            app.desktop.onMousePress(app, mouseX, mouseY)

    def mouseDrag(self, app, mouseX, mouseY):
        # mouse drag input to current mode
        if self.currentMode == 'desktop':
            app.desktop.windowManager.mouseDragWindow(app, mouseX, mouseY)
