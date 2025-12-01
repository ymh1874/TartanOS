# systems/userAuth.py - user authentication system
# manages user credentials and login verification

class UserAuth:
    def __init__(self):
        self.users = {
            'admin': 'root',
            'bob': 'builder',
            'diddy': 'trq'
        }
        
        self.loggedInUser = 'admin'
    def verify(self, username, password):
        if self.users.get(username) == password:
            self.loggedInUser = username
            return True
        return False