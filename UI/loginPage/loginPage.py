from cmu_graphics import *

from systems import userAuth

class LoginPage:
    def __init__(self, app):
        self.app = app
        # colors
        self.bgColor = rgb(34, 139, 34)  # forest green fallback
        self.boxColor = rgb(50, 50, 50)  # dark gray
        self.textColor = 'white'
        self.borderColor = 'white'
        self.activeColor = rgb(128, 0, 0)  # maroon 
        self.userAuth = userAuth.UserAuth()
        
        # background image
        self.backgroundImage = 'assets/backgrounds/loginBackground.png'
        self.profilePicPath = 'assets/icons/adminProfilePic.png'
        
        # input box state
        self.usernameBox = {
            'x': 0.05,
            'y': 0.35,
            'width': 0.3,
            'height': 0.1,
            'active': False,
            'text': ''
        }
        
        self.passwordBox = {
            'x': 0.05,
            'y': 0.55,
            'width': 0.3,
            'height': 0.1,
            'active': False,
            'text': ''
        }
        
        # profile picture placeholder
        self.profilePicSize = 80
        
        
        
        # error state for failed login attempts
        self.loggedin = False
        self.errorMessage = ''
        self.errorTimer = 0
        self.errorDuration = 80  # frames to show error message
        
    def draw(self, app):
        # if user is already logged in, skip to desktop
        if self.loggedin:
            app.modeManager.setMode('desktop')
            return
        
        # draw login background image
        try:
            drawImage(self.backgroundImage, 0, 0, width=app.width, height=app.height)
        except:
            # fallback to green color if image not found
            drawRect(0, 0, app.width, app.height, fill=self.bgColor)
        
        # calculate responsive sizes based on screen dimensions
        titleSize = max(28, int(app.width * 0.035))
        labelSize = max(16, int(app.width * 0.022))  # bigger labels
        inputSize = max(14, int(app.width * 0.018))
        borderWidth = max(2, int(app.width * 0.003))
        profileSize = min(app.width, app.height) * 0.4
        buttonSize = max(14, int(app.width * 0.022))
        
        # profile picture placeholder on right side
        profileX = app.width * 0.75
        profileY = app.height * 0.5
        self.drawProfilePicture(profileX, profileY, profileSize)
        
        # title 
        drawLabel('Login', 
                  app.width * 0.05, app.height * 0.22,
                  size=titleSize, fill='white', align='left', bold = True)
        
        # username label 
        drawLabel('Username:', 
                  app.width * self.usernameBox['x'], 
                  app.height * (self.usernameBox['y'] - 0.07),
                  size=labelSize, fill=self.textColor, align='left')
        
        # username input box
        boxX = app.width * self.usernameBox['x']
        boxY = app.height * self.usernameBox['y']
        boxW = app.width * self.usernameBox['width']
        boxH = app.height * self.usernameBox['height']
        
        borderColor = self.activeColor if self.usernameBox['active'] else self.borderColor
        drawRect(boxX, boxY, boxW, boxH, 
                 fill=self.boxColor, border=borderColor, borderWidth=borderWidth)
        
        drawLabel(self.usernameBox['text'], 
                  boxX + app.width * 0.01, boxY + boxH * 0.5,
                  size=inputSize, fill=self.textColor, align='left')
        
        # password label 
        drawLabel('Password:', 
                  app.width * self.passwordBox['x'], 
                  app.height * (self.passwordBox['y'] - 0.07),
                  size=labelSize, fill=self.textColor, align='left')
        
        # password input box
        boxX = app.width * self.passwordBox['x']
        boxY = app.height * self.passwordBox['y']
        boxW = app.width * self.passwordBox['width']
        boxH = app.height * self.passwordBox['height']
        
        borderColor = self.activeColor if self.passwordBox['active'] else self.borderColor
        drawRect(boxX, boxY, boxW, boxH, 
                 fill=self.boxColor, border=borderColor, borderWidth=borderWidth)
        
        # show masked password
        maskedPassword = '*' * len(self.passwordBox['text'])
        drawLabel(maskedPassword, 
                  boxX + app.width * 0.01, boxY + boxH * 0.5,
                  size=inputSize, fill=self.textColor, align='left')
        
        # login button - left side, simple
        loginButtonY = app.height * 0.70
        loginButtonH = app.height * 0.07
        loginButtonW = app.width * 0.2
        loginButtonX = app.width * 0.05  # left side
        
        drawRect(loginButtonX, loginButtonY, loginButtonW, loginButtonH,
                 fill=self.activeColor, border=self.borderColor, borderWidth=borderWidth)
        drawLabel('Login', 
                  loginButtonX + loginButtonW / 2, loginButtonY + loginButtonH / 2,
                  size=buttonSize, fill='white', align='center', bold=True)
        
        # draw error popup if there is one
        if self.errorMessage and self.errorTimer > 0:
            self.drawErrorPopup(app)
            self.errorTimer -= 1
    
    def drawProfilePicture(self, centerX, centerY, size):
        # draw profile picture on right side
            drawImage(self.profilePicPath, app.width * 0.85 , 
                      app.height * 0.5,
                     width=size, height=size, align='center')
        
    
    def drawErrorPopup(self, app):
        # draw error popup message in center of screen
        popupWidth = app.width * 0.5
        popupHeight = app.height * 0.25
        popupX = app.width * 0.25
        popupY = app.height * 0.3
        
        # error popup background (dark red)
        drawRect(popupX, popupY, popupWidth, popupHeight,
                 fill=rgb(139, 35, 35), border=rgb(255, 100, 100), borderWidth=3)
        
        # error title
        titleSize = max(16, int(app.width * 0.02))
        drawLabel('ERROR', popupX + popupWidth * 0.5, popupY + popupHeight * 0.2,
                  size=titleSize, bold=True, fill=rgb(255, 100, 100), align='center')
        
        # error message
        messageSize = max(12, int(app.width * 0.015))
        drawLabel(self.errorMessage, popupX + popupWidth * 0.5, popupY + popupHeight * 0.55,
                  size=messageSize, fill='white', align='center')
    
    def onKeyPress(self, app, key, modifiers=None):
        # if error is showing, any key dismisses it
        if self.errorMessage:
            self.errorMessage = ''
            self.errorTimer = 0
            return
        if modifiers == ['shift'] and key == 'right':
            self.userAuth.loggedInUser = 'bob'
            self.profilePicPath = 'assets/icons/bobProfilePic.png'
            self.usernameBox['text'] = 'bob'
        elif modifiers == ['shift'] and key == 'left':
            self.userAuth.loggedInUser = 'admin'
            self.profilePicPath = 'assets/icons/adminProfilePic.png'
            self.usernameBox['text'] = 'admin'
        elif modifiers == ['shift'] and key == 'down':
            self.userAuth.loggedInUser = 'diddy'
            self.profilePicPath = 'assets/icons/diddyProfilePic.png'
            self.usernameBox['text'] = 'diddy'
        
        # handle ctrl+t to switch to terminal (use terminal's login)
        if modifiers and modifiers == ['control'] and key == 't':
            # reset terminal's login state and switch to terminal
            self.app.terminal.isLoggingIn = True
            self.app.terminal.loginStage = "username"
            self.app.terminal.tempUsername = ""
            self.app.terminal.tempPassword = ""
            self.app.terminal.tempInput = ""
            self.app.terminal.textLines = []
            self.app.terminal.output("Welcome to TartanOS")
            self.app.modeManager.setMode('terminal')
            return
        
        # handle tab key to switch between fields
        if key == 'tab':
            if self.usernameBox['active']:
                # move from username to password
                self.usernameBox['active'] = False
                self.passwordBox['active'] = True
            elif self.passwordBox['active']:
                # move from password back to username
                self.passwordBox['active'] = False
                self.usernameBox['active'] = True
            else:
                # no box active, default to username
                self.usernameBox['active'] = True
                self.passwordBox['active'] = False
            return
        
        # determine which box is active
        if self.usernameBox['active']:
            if key == 'enter':
                # move to password box when enter pressed
                if self.usernameBox['text']:  # only move if username is not empty
                    self.usernameBox['active'] = False
                    self.passwordBox['active'] = True
                else:
                    # if no text, try to login anyway (will show error)
                    self.attemptLogin()
            elif key == 'backspace':
                self.usernameBox['text'] = self.usernameBox['text'][:-1]
            elif len(key) == 1 and (key.isalnum() or key == '_'):
                self.usernameBox['text'] += key
                
        elif self.passwordBox['active']:
            if key == 'enter':
                self.attemptLogin()
            elif key == 'backspace':
                self.passwordBox['text'] = self.passwordBox['text'][:-1]
            elif len(key) == 1:
                self.passwordBox['text'] += key
        else:
            # no box active, default to username
            if not self.usernameBox['active'] and not self.passwordBox['active']:
                self.usernameBox['active'] = True
    
    def onMousePress(self, app, mouseX, mouseY):
        # check username box click
        usernameBoxX = app.width * self.usernameBox['x']
        usernameBoxY = app.height * self.usernameBox['y']
        usernameBoxW = app.width * self.usernameBox['width']
        usernameBoxH = app.height * self.usernameBox['height']
        
        if (usernameBoxX <= mouseX <= usernameBoxX + usernameBoxW and
            usernameBoxY <= mouseY <= usernameBoxY + usernameBoxH):
            self.usernameBox['active'] = True
            self.passwordBox['active'] = False
            return
        
        # check password box click
        passwordBoxX = app.width * self.passwordBox['x']
        passwordBoxY = app.height * self.passwordBox['y']
        passwordBoxW = app.width * self.passwordBox['width']
        passwordBoxH = app.height * self.passwordBox['height']
        
        if (passwordBoxX <= mouseX <= passwordBoxX + passwordBoxW and
            passwordBoxY <= mouseY <= passwordBoxY + passwordBoxH):
            self.passwordBox['active'] = True
            self.usernameBox['active'] = False
            return
        
        # check login button click
        loginButtonX = app.width * 0.05
        loginButtonY = app.height * 0.70
        loginButtonW = app.width * 0.2
        loginButtonH = app.height * 0.07
        
        if (loginButtonX <= mouseX <= loginButtonX + loginButtonW and
            loginButtonY <= mouseY <= loginButtonY + loginButtonH):
            self.attemptLogin()
            return
        
        # deselect boxes if clicking elsewhere
        self.usernameBox['active'] = False
        self.passwordBox['active'] = False
    
    def attemptLogin(self):
        # verify credentials using auth system
        username = self.usernameBox['text']
        password = self.passwordBox['text']
        
        # check if fields are empty
        if not username or not password:
            self.errorMessage = 'Please fill in all fields'
            self.errorTimer = self.errorDuration
            return
        
        if self.app.auth.verify(username, password):
            # login successful - go to desktop
            self.app.terminal.username = username
            self.app.terminal.isLoggingIn = False
            self.loggedin = True
            self.app.modeManager.setMode('desktop')
        else:
            # login failed - show error, clear both fields, reset to username box
            self.errorMessage = 'Invalid username or password'
            self.errorTimer = self.errorDuration
            self.usernameBox['text'] = ''
            self.passwordBox['text'] = ''
            self.usernameBox['active'] = True
            self.passwordBox['active'] = False
