from domain.model.playing_field import *
from domain.model.user import *
import uuid
import random
import datetime

class StatusGame(Enum):
    WAITINGPLAYERS = "waiting players"
    MOVEX = "move X"
    MOVEO = "move O"
    WINX = "win X"
    WINO = "win O"
    DRAW = "draw"

class CurrentGame:
    def __init__(self, 
                    new_creator, 
                    new_uuid = None, 
                    new_field = None, 
                    new_type_creator = 0, 
                    is_multy = False, 
                    new_enemy = None, 
                    new_status = StatusGame.WAITINGPLAYERS,
                    new_data_creator = None):
        self.creator = new_creator
        
        
    
        if new_uuid is None:
            self.id_game = uuid.uuid4()
        else:
            self.id_game = new_uuid
        
        if new_field is None:
            self.field = PlayingField()
        else:
            self.field = new_field
        
        self.type_creator = new_type_creator
        self.is_multy = is_multy
        self.enemy = new_enemy
        self.status = new_status
        if is_multy == False and new_type_creator == 0:
            self.type_creator = random.choice([X, O])
            self.status = StatusGame.MOVEX
            
        if new_data_creator is None:
            self.data_creator = datetime.datetime.now()
        else:
            self.data_creator = new_data_creator
            
            
        
    
    def change_turn(self):
        result_move = self.field.get_result_game()
        if result_move == TypeResult.CONTINUE:
            if self.status == StatusGame.MOVEX:
                self.status = StatusGame.MOVEO
            elif self.status == StatusGame.MOVEO:
                self.status = StatusGame.MOVEX
        elif result_move == TypeResult.WINX:
            self.status = StatusGame.WINX
        elif result_move == TypeResult.WINO:
            self.status = StatusGame.WINO
        elif result_move == TypeResult.DRAW:
            self.status = StatusGame.DRAW
    
    def get_next_move(self):
        if self.status == StatusGame.MOVEO:
            self.field.get_next_move(O)
            self.change_turn()
        elif self.status == StatusGame.MOVEX:
            self.field.get_next_move(X)
            self.change_turn()
    
    def check_correct_move(self, next_move): #: CurrentGame
        return self.field.check_correct_move(next_move.field)
        
    def get_result_game(self):
        return self.status.value

    def copy(self):
        new_creator = User(self.creator.id_user, self.creator.login, self.creator.password, self.creator.count_games, self.creator.count_wins, self.creator.count_lose)
        
        new_uuid = self.id_game

        new_field = []
        for line in self.field.field:
            new_line = []
            for elem in line:
                new_line.append(elem)
            new_field.append(new_line)
        field = PlayingField(new_field)
        
        
        new_type_creator = self.type_creator 
        is_multy = self.is_multy
        
        new_enemy = None
        if self.enemy is not None:
            new_enemy = User(self.enemy.id_user, self.enemy.login, self.enemy.password, self.enemy.count_games, self.enemy.count_wins, self.enemy.count_lose)
        
        new_status = self.status
        new_data_creator = self.data_creator
        
        result = CurrentGame(new_creator, new_uuid, new_field, new_type_creator, is_multy, new_enemy, new_status, new_data_creator)
        
        return result

    def set_move(self, i, j):
        if self.status == StatusGame.MOVEO:
            self.field.make_move(i, j, O)
            self.change_turn()
        elif self.status == StatusGame.MOVEX:
            self.field.make_move(i, j, X)
            self.change_turn()

    def add_enemy(self, new_enemy):
        if self.status == StatusGame.WAITINGPLAYERS and self.is_multy:
            self.enemy = new_enemy
            self.enemy.count_games += 1
            self.status = StatusGame.MOVEX
            self.type_creator = random.choice([X, O])
            
    def update_info_players(self, id_user, icon_user):
        user = self.creator if self.creator.id_user == id_user else self.enemy
        enemy = self.creator if self.creator.id_user != id_user else self.enemy
        if self.status == StatusGame.WINX:
            if icon_user == X:
                user.count_wins +=1
                if enemy is not None:
                    enemy.count_lose +=1
            else:
                user.count_lose +=1
                if enemy is not None:
                    enemy.count_wins +=1
        elif self.status == StatusGame.WINO:
            if icon_user == O:
                user.count_wins +=1
                if enemy is not None:
                    enemy.count_lose +=1
            else:
                user.count_lose +=1
                if enemy is not None:
                    enemy.count_wins +=1
            
    def make_move(self, id_user, i, j):
        is_current_move = True
        
        walking_icon = EMPTY
        if self.status == StatusGame.MOVEX:
            walking_icon = X  
        elif self.status == StatusGame.MOVEO:
            walking_icon = O
        
        icon_user = -1
        if self.creator.id_user == id_user:
            icon_user = self.type_creator
        else:
            icon_user = X if self.type_creator == O else O
            
        if self.field.field[i][j] != EMPTY or walking_icon != icon_user:
            is_current_move = False
        
        if is_current_move:
            self.set_move(i, j)
            if self.is_multy == False:
                self.get_next_move()
                
            self.update_info_players(id_user, icon_user)
            
            