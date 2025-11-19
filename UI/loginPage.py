from cmu_graphics import*
class LoginPage:
    users = {'admin': '67112'}  # Example user database
    def __init__(self):
        self.box1Highlighted = False
        self.box2Highlighted = False
        self.background = 'assets/loginBackground.png'
        self.username = 'yousef'
        self.password = 'Password'
        self.loginPressed = False
        
        
    def addUser(self, username, password):
        LoginPage.users[username] = password

    def draw(self, app):
        
        drawImage(self.background, 0, 0, width=app.width, height=app.height)
        # first box
        drawRect(app.width*0.123047, app.height*0.344727,
             app.width*0.282552, app.height*0.067383,
            fill=rgb(110, 0, 18), border='black', borderWidth=2, opacity=80)
        if self.box1Highlighted:
            self.highlightBox(1, app)
        drawLabel(self.username, app.width*0.14, app.height*0.38, size=app.width*0.02, bold=True, fill='white', align = 'left')
        
        # second box
        drawRect(app.width*0.123698, app.height*0.450195,
                app.width*0.279948, app.height*0.067383,
                fill=rgb(110, 0, 18), border='black', borderWidth=2, opacity=80)
        drawLabel(self.password, app.width*0.14, app.height*0.485, size= app.width*0.02, bold=True, fill='white', align = 'left')
        if self.box2Highlighted:
            self.highlightBox(2, app)
        # login button
        if self.username == 'Username' or self.password == 'Password':
            drawRect(app.width*0.122396, app.height*0.641602,
                    app.width*0.287109, app.height*0.084961,
                    fill=rgb(110, 0, 18), border='black', borderWidth=2, opacity=80)  

    def highlightBox(self, boxNumber, app):

        if boxNumber == 1:
            drawRect(app.width*0.123047, app.height*0.344727,
             app.width*0.282552, app.height*0.067383,
            fill=None, border='white', borderWidth=4, opacity=100)

        elif boxNumber == 2:
            drawRect(app.width*0.123698, app.height*0.450195,
                app.width*0.279948, app.height*0.067383,
                fill=None, border='white', borderWidth=4, opacity=100)

    def loginKeyPress(self,app, key):
        if key == 'enter' and self.username != 'Username' and self.password != 'Password' :
            username = self.username
            password = self.password
            self.addUser(username, password)
            app.screen = 'terminal'
            
        if self.box1Highlighted:
            if key == 'backspace':
                self.username = self.username[:-1]
            elif  key.isalpha() and len(key) == 1:
                if self.username == 'Username':
                    self.username = ''
                if len(self.username) < 15:
                    self.username += key
        elif self.box2Highlighted:
            if key == 'backspace':
                self.password = self.password[:-1]
            if self.password == 'Password':
                self.password = ''
            elif  len(key) == 1:
                if len(self.password) < 15:
                    self.password += key

    def loginMousePress(self, app, mouseX, mouseY):
        if (app.width*0.123047 <= mouseX <= app.width*0.405599 and
            app.height*0.344727 <= mouseY <= app.height*0.41211):
            self.box1Highlighted = True  
            self.box2Highlighted = False

        elif (app.width*0.123698 <= mouseX <= app.width*0.403646 and
              app.height*0.450195 <= mouseY <= app.height*0.517578):
            self.box2Highlighted = True
            self.box1Highlighted = False

        
        
        
                    
        
        # LOGIN BUTTON
        elif (app.width*0.122396 <= mouseX <= app.width*0.287109 and
              app.height*0.641602 <= mouseY <= app.height*0.084961):
            self.loginPressed = True
            

    def checkUser(self, username, password):
        return LoginPage.users.get(username) == password


