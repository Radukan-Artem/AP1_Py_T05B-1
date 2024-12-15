from datasource.repository.repository import Repository
from domain.model.current_game import CurrentGame
from domain.service.interface_service import InterfaceService
from datasource.mapper.mapper import DataMapper
import random

class Service(InterfaceService):
    def __init__(self, repository: Repository):
        self.repository = repository

    def create_game(self, id_user, is_multy):
        user_table = self.repository.find_user_by_id(id_user)
        user = DataMapper.user_table_to_user(user_table)
        game = CurrentGame(user, is_multy = is_multy)
        user.count_games += 1

        if game.type_creator == 2:
            game.get_next_move()
        
        game_table, field_tables, creator_table, enemy_table = DataMapper.current_game_to_game_field_users_tables(game)
        self.repository.add_game_info(game_table)
        self.repository.add_field_info(field_tables)
        self.repository.update_user_info(creator_table)
        
        return game.id_game
        
    def get_game(self, game_id):
        game_info = self.repository.get_game_info(game_id)
        result = DataMapper.current_game_table_to_current_game(game_info)
        return result

    def get_status_game(self, id_game):
        this_game = self.get_game(id_game)
        return this_game.get_result_game()    

    def make_move(self, id_user, id_game, i, j):   
        game = self.get_game(id_game)
        game.make_move(id_user, i, j)
        
        game_table, field_tables, creator_table, enemy_table = DataMapper.current_game_to_game_field_users_tables(game)
        self.repository.update_game_info(game_table)
        self.repository.update_field_info(field_tables)
        self.repository.update_user_info(creator_table)
        if enemy_table is not None:
            self.repository.update_user_info(enemy_table)
        
        
        
        
        
        
    def get_list_id_games_for_user(self, id_user):
        result = []
        list_games = self.repository.get_list_games_for_user(id_user)
        
        for game in list_games:
            result.append({"creator": game.creator, "id_game": game.id_game})
        
        return result
        
    def join_to_game(self, id_user, id_game):
        result = False
        
        game = self.repository.get_game_info(id_game)
        
        if game is not None:
            if game.creator == id_user or (game.enemy is not None and game.enemy == id_user):
                result = True
            elif game.enemy is None:
                result = True
                game.enemy = id_user
                game.type_creator = random.choice([1, 2])
                game.status = "move X"
                self.repository.update_game_info(game)
                user = self.repository.find_user_by_id(id_user)
                user.count_games += 1
                self.repository.update_user_info(user)
            
        return result

    def get_user_info(self, user_id):
        user_table = self.repository.find_user_by_id(user_id)
        user = DataMapper.user_table_to_user(user_table) if user_table is not None else None
        return user
        
        
    def get_history_games_for_user(self, id_user):
        result = []
        list_games = self.repository.get_history_games_for_user(id_user)
        
        for game in list_games:
            icon_user = "uninitialized"
            type_creator = 0
            if game.creator == id_user:
                type_creator = game.type_creator
            else:
                type_creator = 1 if game.type_creator == 2 else 2
            
               
            if type_creator == 1:
                icon_user = "X"
            elif type_creator == 2:
                icon_user = "O"
        
            result.append({"id_game": game.id_game, "icon_user": icon_user, "status_game": game.status})
        
        return result
        
    def get_list_leaders(self, count_leaders):
        result = []
        list_leaders = self.repository.get_list_leaders(count_leaders)
        
        for leader in list_leaders:
        
            result.append({"id_user": leader.id_user, "login": leader.login, "count_wins": leader.count_wins, "count_lose_draw": leader.count_games - leader.count_wins})
        
        return result