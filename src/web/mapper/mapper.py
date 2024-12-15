from web.model.user_authenticator import UserAuthenticator
from web.model.web_current_game import WebCurrentGame
from web.model.web_playing_field import WebPlayingField

from domain.model.user import User
from domain.model.current_game import CurrentGame, StatusGame
from domain.model.playing_field import PlayingField


class WebMapper:
    def user_to_user_authenticator(user: User):
        result = UserAuthenticator()
        result.id_user = user.id_user
        result. login = user.login
        result.password = user.password
        result.count_games = user.count_games
        result.count_wins = user.count_wins
        result.count_lose = user.count_lose
        return result
        
    def playing_field_to_web_playing_field(playing_field: PlayingField):
        new_field = []
        
        for line in playing_field.field:
            new_line = []
            for cell in line:
                if cell == 1:
                    new_line.append("X")
                elif cell == 2:
                    new_line.append("0")
                else:
                    new_line.append(" ")
            new_field.append(new_line)
        
        return WebPlayingField(new_field)
        
    def current_game_to_web_current_game(current_game: CurrentGame):
        creator = WebMapper.user_to_user_authenticator(current_game.creator)
        field = WebMapper.playing_field_to_web_playing_field(current_game.field)
        type_creator = "not assigned"
        if current_game.type_creator == 1:
            type_creator = "X"
        elif current_game.type_creator == 2:
            type_creator = "O"
        enemy = None if current_game.enemy is None else WebMapper.user_to_user_authenticator(current_game.enemy)
        
        
        result = WebCurrentGame(creator, 
                    new_uuid = current_game.id_game, 
                    new_field = field, 
                    new_type_creator = type_creator, 
                    is_multy = current_game.is_multy, 
                    new_enemy = enemy, 
                    new_status = current_game.status.value,
                    new_data_creator = current_game.data_creator)
            
        return result
    
        
        
        
        
    def web_user_to_user(user_authenticator: UserAuthenticator):
        result = User(
                     new_id_user = user_authenticator.id_user,
                     new_login = user_authenticator.login,
                     new_password = user_authenticator.password, 
                     new_count_games = user_authenticator.count_games,
                     new_count_wins = user_authenticator.count_wins,
                     new_count_lose = user_authenticator.count_lose
                    )
                    
        return result
        
    def web_playing_field_to_playing_field(web_playing_field): 
        new_field = []
        
        for line in web_playing_field.field:
            new_line = []
            for cell in line:
                if cell == "X":
                    new_line.append(1)
                elif cell == "0":
                    new_line.append(2)
                else:
                    new_line.append(0)
            new_field.append(new_line)
        
        return WebPlayingField(new_field)
        
        
    def web_current_game_to_current_game(web_current_game: WebCurrentGame):
        creator = WebMapper.web_user_to_user(web_current_game.creator)
        field = WebMapper.web_playing_field_to_playing_field(web_current_game.field)
        type_creator = 0
        if web_current_game.type_creator == "X":
            type_creator = 1
        elif web_current_game.type_creator == "O":
            type_creator = 2
        enemy = None if web_current_game.enemy is None else WebMapper.web_user_to_user(web_current_game.enemy)
        
        result = CurrentGame(creator, 
                    new_uuid = web_current_game.id_game, 
                    new_field = field, 
                    new_type_creator = type_creator, 
                    is_multy = web_current_game.is_multy, 
                    new_enemy = enemy, 
                    new_status = StatusGame(web_current_game.status),
                    new_data_creator = web_current_game.data_creator)
        
        return result
       
        