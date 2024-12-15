from datasource.model.user_table import UserTable
from datasource.model.current_game_table import CurrentGameTable
from datasource.model.playing_field_table import PlayingFieldTable

from domain.model.user import User
from domain.model.current_game import CurrentGame, StatusGame
from domain.model.playing_field import PlayingField

from datasource.repository.repository import Repository

class DataMapper:
    def user_to_user_table(user: User):
        result = UserTable(
                     id_user = user.id_user,
                     login = user.login,
                     password = user.password, 
                     count_games = user.count_games,
                     count_wins = user.count_wins,
                     count_lose = user.count_lose
                    )
                    
        return result
        
    def playing_field_to_playing_field_table(playing_field: PlayingField, new_id_game):
        result = []
        
        for this_i in range(3):
            for this_j in range(3):
                cell = PlayingFieldTable(id_game = new_id_game, i = this_i, j = this_j, value = playing_field.field[this_i][this_j])
                result.append(cell)
        
        return result
        
    def current_game_to_current_game_table(current_game: CurrentGame):
        result = CurrentGameTable(id_game = current_game.id_game,
                                       creator = current_game.creator.id_user,
                                       type_creator = current_game.type_creator,
                                       is_multy = current_game.is_multy,
                                       enemy = current_game.enemy.id_user if current_game.enemy is not None else None,
                                       status = current_game.status.value,
                                       data_creator = current_game.data_creator)
                                       
        return result
        
    def current_game_to_game_field_users_tables(current_game: CurrentGame):
        result_game = DataMapper.current_game_to_current_game_table(current_game)
        result_field = DataMapper.playing_field_to_playing_field_table(current_game.field, current_game.id_game)
        result_creator = DataMapper.user_to_user_table(current_game.creator)
        result_enemy = DataMapper.user_to_user_table(current_game.enemy) if current_game.enemy is not None else None
        
        return result_game, result_field, result_creator, result_enemy
        
    
        
        
        
    def user_table_to_user(user_table: UserTable):
        result = User(
                     new_uuid = user_table.id_user,
                     new_login = user_table.login,
                     new_password = user_table.password, 
                     new_count_games = user_table.count_games,
                     new_count_wins = user_table.count_wins,
                     new_count_lose = user_table.count_lose
                    )
                    
        return result
        
    def playing_field_table_to_playing_field(playing_field_table): #list(PlayingFieldTable)
        new_field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for elem in playing_field_table:
            new_field[elem.i][elem.j] = elem.value
            
        return PlayingField(new_field)
        
        
    def current_game_table_to_current_game(current_game_table: CurrentGameTable):
        repository = Repository()
        creator_table = repository.find_user_by_id(current_game_table.creator)
        enemy_table = repository.find_user_by_id(current_game_table.enemy) if current_game_table.enemy is not None else None
        field_tables = repository.load_field_by_id_game(current_game_table.id_game)
        
        creator = DataMapper.user_table_to_user(creator_table)
        enemy = DataMapper.user_table_to_user(enemy_table) if current_game_table.enemy is not None else None
        field = DataMapper.playing_field_table_to_playing_field(field_tables)
        
        result = CurrentGame(creator, 
                                new_uuid = current_game_table.id_game, 
                                new_field = field, 
                                new_type_creator = current_game_table.type_creator, 
                                is_multy = current_game_table.is_multy, 
                                new_enemy = enemy, 
                                new_status = StatusGame(current_game_table.status),
                                new_data_creator = current_game_table.data_creator)

        repository.engine.dispose()
                                
        return result
        