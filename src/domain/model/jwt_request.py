import base64

class JwtRequest():
    def __init__(self, new_login = "noname", new_password = "password"):
        self.login = new_login
        self.password = base64.b64encode(new_password.encode())