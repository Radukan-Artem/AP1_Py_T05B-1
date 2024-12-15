from abc import ABC, abstractmethod
 
class InterfaceService(ABC):
 
    @abstractmethod
    def make_move(self, id_user, id_game, i, j):
        pass
    
    @abstractmethod
    def get_status_game(self, id_game):
        pass