from web.model.web_playing_field import WebPlayingField
import uuid
import random
import datetime

class WebCurrentGame:
    def __init__(self, new_creator, 
                    new_uuid = None, 
                    new_field = None, 
                    new_type_creator = "not assigned", 
                    is_multy = False, 
                    new_enemy = None, 
                    new_status = "waiting players",
                    new_data_creator = None):
        self.creator = new_creator            
                    
        if new_uuid is None:
            self.id_game = uuid.uuid4()
        else:
            self.id_game = new_uuid
        
        if new_field is None:
            self.field = WebPlayingField()
        else:
            self.field = new_field
        
        self.type_creator = new_type_creator
        self.is_multy = is_multy
        self.enemy = new_enemy
        self.status = new_status
        if is_multy == False and new_type_creator == "not assigned":
            self.type_creator = random.choice(["X", "O"])
            self.status = "move X"
            
        if new_data_creator is None:
            self.data_creator = datetime.datetime.now()
        else:
            self.data_creator = new_data_creator    
