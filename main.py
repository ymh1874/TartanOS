# main.py 
from cmu_graphics import*
from UI.loginPage import LoginPage
from UI.terminal import terminal
from UI.desktop import desktop

def onAppStart(app):
    app.loginPage = LoginPage()
    app.terminal = terminal(app)
    app.desktop = desktop(app)
    app.screen = 'terminal'  # Start with the login screen
    app.tick = 0
    

    
def redrawAll(app):
    if app.screen == 'loginPage':
        app.loginPage.draw(app)
    elif app.screen == 'terminal':
        app.terminal.draw(app)
    elif app.screen == 'desktop':
        app.desktop.draw(app)
        
def onMousePress(app, mouseX, mouseY):
    if app.screen == 'loginPage':
        app.loginPage.loginMousePress(app , mouseX, mouseY)
    elif app.screen  == 'terminal':
        pass
    elif app.screen == 'desktop':
        pass
    
def onMouseDrag(app, mouseX, mouseY):
        if app.screen == 'desktop':
            app.desktop.onMouseDragDesktop(app, mouseX, mouseY)
         

def onKeyPress(app, key, modifiers):
    if app.screen == 'loginPage':
        app.loginPage.loginKeyPress(app, key)
    elif app.screen == 'terminal':
        app.terminal.onKeyPressTerminal(app, key, modifiers)   
    elif app.screen == 'desktop':
        app.desktop.onKeyPressDesktop(app, key, modifiers)

def onStep(app):
    app.tick += 1

runApp(app.width, app.height)
