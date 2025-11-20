# core/appModes.py
class ModeManager:
    def __init__(self, app):
        self.app = app
        self.currentMode = None

    def setMode(self, modeName):
        self.currentMode = modeName

    def redraw(self, app):
        if self.currentMode == 'terminal':
            app.terminal.draw(app)

    def keyPress(self, app, key, modifiers):
        if self.currentMode == 'terminal':
            app.terminal.onKeyPress(app, key, modifiers)
