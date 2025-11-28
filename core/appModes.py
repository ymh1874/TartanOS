# core/appModes.py - manages different app states

class ModeManager:
    def __init__(self, app):
        self.app = app
        self.currentMode = None

    def setMode(self, modeName):
        # set current mode: 'login', 'desktop', or 'terminal'
        self.currentMode = modeName

    def redraw(self, app):
        # render appropriate UI based on current mode
        if self.currentMode == 'login':
            app.loginPage.draw(app)
        elif self.currentMode == 'desktop':
            app.desktop.draw(app)
        elif self.currentMode == 'terminal':
            app.terminal.draw(app)

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
