from flask_login import UserMixin
 
class UserAuthenticator(UserMixin):
    id_user = None
    login = ""
    password = ""
    count_games = 0
    count_wins = 0
    count_lose = 0

    def get_id(self):
        return self.id_user