import uuid

class User:
    def __init__(self, new_uuid = None, new_login = "noname", new_password = "password", new_count_games = 0, new_count_wins = 0, new_count_lose = 0):
        if new_uuid is None:
            self.id_user = uuid.uuid4()
        else:
            self.id_user = new_uuid
            
        self.login = new_login
        self.password = new_password
        self.count_games = new_count_games
        self.count_wins = new_count_wins
        self.count_lose = new_count_lose
        