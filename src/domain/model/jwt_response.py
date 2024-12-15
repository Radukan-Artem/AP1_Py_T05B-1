class JwtResponse():
    def __init__(self, new_accessToken = None, new_refreshToken = None):
        self.accessToken = new_accessToken
        self.refreshToken = new_refreshToken