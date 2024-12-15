from enum import Enum

class TypeResult(Enum):
    CONTINUE = "continue"
    WINX = "win X"
    WINO = "win O"
    DRAW = "draw"
    
EMPTY = 0
X = 1
O = 2

class PlayingField:
    def __init__(self, new_field = None):
        if new_field is None:
            self.field = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
        else:
            self.field = new_field
        
    def check_win_in_line(self):
        result = TypeResult.CONTINUE
        
        for line in self.field:
            if line[0] == line[1] and line[0] == line[2]:
                if line[0] == X:
                    result = TypeResult.WINX
                elif line[0] == O:
                    result = TypeResult.WINO
        
        return result
    
    def check_win_in_column(self):
        result = TypeResult.CONTINUE
        
        for index_column in range(len(self.field)):
            if self.field[0][index_column] == self.field[1][index_column] and self.field[0][index_column] == self.field[2][index_column]:
                if self.field[0][index_column] == X:
                    result = TypeResult.WINX
                elif self.field[0][index_column] == O:
                    result = TypeResult.WINO
        
        return result
        
    def check_win_in_diagonal(self):
        result = TypeResult.CONTINUE
        
        if self.field[0][0] == self.field[1][1] and self.field[0][0] == self.field[2][2]:
            if self.field[0][0] == X:
                result = TypeResult.WINX
            elif self.field[0][0] == O:
                result = TypeResult.WINO
        elif self.field[2][0] == self.field[1][1] and self.field[2][0] == self.field[0][2]:
            if self.field[2][0] == X:
                result = TypeResult.WINX
            elif self.field[2][0] == O:
                result = TypeResult.WINO
        
        return result
        
    def check_draw(self):
        result = TypeResult.CONTINUE
        
        count_empty_cells = 0
        
        for line in self.field:
            for cell in line:
                if cell == EMPTY:
                    count_empty_cells += 1
        
        if count_empty_cells == 0:
            result = TypeResult.DRAW
        
        return result
        
    def get_result_game(self):
        result = TypeResult.CONTINUE
        
        result = self.check_win_in_line()
        if result == TypeResult.CONTINUE:
            result = self.check_win_in_column()
        if result == TypeResult.CONTINUE:
            result = self.check_win_in_diagonal()
        
        if result == TypeResult.CONTINUE:
            result = self.check_draw()
            
        return result
    
    
    
    
    
    def make_move(self, i, j, value):
        self.field[i][j] = value

    def undo_move(self, i, j):
        self.field[i][j] = EMPTY

    def minimax(self, depth, maximizing_player, player):
        result_game = self.get_result_game()
        if (result_game == TypeResult.WINX and player == X) or (result_game == TypeResult.WINO and player == O):
            return 10
        if (result_game == TypeResult.WINX and player == O) or (result_game == TypeResult.WINO and player == X):
            return -10
        if result_game == TypeResult.DRAW:
            return 0
        
        opponent = X
        if player == X:
            opponent = O
        
        if maximizing_player:
            max_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.field[i][j] == EMPTY:
                        self.make_move(i, j, player)
                        score = self.minimax(depth + 1, False, player)
                        self.undo_move(i, j)
                        max_score = max(max_score, score)
            return max_score

        else:
            min_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.field[i][j] == EMPTY:
                        self.make_move(i, j, opponent)
                        score = self.minimax(depth + 1, True, player)
                        self.undo_move(i, j)
                        min_score = min(min_score, score)
            return min_score

    def find_best_move(self, player):
        best_score = float('-inf')
        best_i, best_j = None, None
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == EMPTY:
                    self.make_move(i, j, player)
                    score = self.minimax(0, False, player)
                    self.undo_move(i, j)
                    if score > best_score:
                        best_score = score
                        best_i = i
                        best_j = j
        return best_i, best_j
    
    def get_next_move(self, value):
        best_i, best_j = self.find_best_move(value)
        self.make_move(best_i, best_j, value)
        
        
        
    def check_correct_move(self, next_move): #: PlayingField
        result = True
        count_changes = 0
        
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == EMPTY and self.field[i][j] != next_move.field[i][j]:
                    count_changes += 1
                elif self.field[i][j] != EMPTY and self.field[i][j] != next_move.field[i][j]:
                    result = False
        
        if count_changes != 1:
            result = False
          
        return result