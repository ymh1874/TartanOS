# main.py 
from cmu_graphics import*
from UI.loginPage import LoginPage
from UI.terminal import terminal
from UI.desktop import desktop

def onAppStart(app):
    app.loginPage = LoginPage()
    app.terminal = terminal(app)
    app.desktop = desktop(app)
    app.screen = 'loginPage'  # Start with the login screen
    

    
def redrawAll(app):
    if app.screen == 'loginPage':
        app.loginPage.draw(app)
    elif app.screen == 'terminal':
        app.terminal.draw(app)
    elif app.screen == 'desktop':
        app.desktop.draw(app)
        
def onMousePress(app, mouseX, mouseY):
    if app.screen == 'loginPage':
        app.loginPage.loginMousePress(mouseX, mouseY, app)
    elif app.screen  == 'terminal':
        pass
         

def onKeyPress(app, key):
    if app.screen == 'loginPage':
        app.loginPage.loginKeyPress(key, app)
    elif app.screen == 'terminal':
        app.terminal.onKeyPressTerminal(key)   

runApp(app.width, app.height)
