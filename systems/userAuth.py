# systems/userAuth.py

class UserAuth:
    def __init__(self):
        self.users = {
            'yousef': '112',
            'admin': 'root'
        }
        self.loggedInUser = None
    def verify(self, username, password):
        if self.users.get(username) == password:
            self.loggedInUser = username
            return True
        return False