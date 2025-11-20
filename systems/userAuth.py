# systems/userAuth.py

class UserAuth:
    def __init__(self):
        self.users = {
            'yousef': '112',
            'admin': 'root'
        }

    def verify(self, username, password):
        return self.users.get(username) == password
