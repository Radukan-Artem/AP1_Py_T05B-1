from sqlalchemy import create_engine, or_, and_, desc
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datasource.model.user_table import UserTable
from datasource.model.current_game_table import CurrentGameTable
from datasource.model.playing_field_table import PlayingFieldTable

from datasource.model.base import Base

class Repository:
    def __init__(self):
        need_create_tables = False
        if not database_exists('postgresql:///pythonday06'):
            connection = psycopg2.connect(user="postgres", password="postgres")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Создаем курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            sql_create_database = "CREATE DATABASE pythonday06"
            # Создаем базу данных
            cursor.execute(sql_create_database)
            # Закрываем соединение
            cursor.close()
            connection.close()
            need_create_tables = True
            
        self.engine = create_engine('postgresql:///pythonday06')
        if need_create_tables:
            Base.metadata.create_all(self.engine)
        
    def find_user_by_id(self, id_user):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(UserTable).filter(UserTable.id_user == id_user).first()

        session.close()
        return result
    
    def find_user_by_login(self, login_user):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(UserTable).filter(UserTable.login == login_user).first()
        
        session.close()
        return result
        
        
    def add_user(self, new_user: UserTable):
        result = False
        
        if self.find_user_by_login(new_user.login) is None:
            session = Session(bind = self.engine)
            session.add(new_user)
            session.commit()
            result = True
            session.close()
            
        return result

    def load_field_by_id_game(self, id_game):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(PlayingFieldTable).filter(PlayingFieldTable.id_game == id_game).all()
        
        session.close()
        return result



    def get_list_games_for_user(self, id_user):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(CurrentGameTable).filter(or_(
                                                            and_(or_(CurrentGameTable.creator == id_user, CurrentGameTable.enemy == id_user),
                                                            CurrentGameTable.status.in_(["waiting players", "move X", "move O"])
                                                            ),
                                                            and_(CurrentGameTable.is_multy == True, CurrentGameTable.enemy == None, CurrentGameTable.status == "waiting players")
                                                            )
                                                        ).all()
        
        session.close()
        return result
        
    def get_game_info(self, id_game):
        session = Session(bind = self.engine)
        
        result = session.query(CurrentGameTable).filter(CurrentGameTable.id_game == id_game).first()
        
        session.close()
        return result

    def add_game_info(self, game):
        session = Session(bind = self.engine)
        
        session.add(game)
        session.commit()
        session.close()
        
    def add_field_info(self, field): #list(PlayingFieldTable)
        session = Session(bind = self.engine)
        
        for cell in field:
            session.add(cell)
        session.commit()
        session.close()





    def update_game_info(self, game: CurrentGameTable):
        session = Session(bind = self.engine)
        
        elem = session.query(CurrentGameTable).filter(CurrentGameTable.id_game == game.id_game).first()
        elem.creator = game.creator
        elem.type_creator = game.type_creator
        elem.is_multy = game.is_multy
        elem.enemy = game.enemy
        elem.status = game.status
   
        
        session.add(elem)
        session.commit()
        session.close()
        
    def update_field_info(self, field): #list(PlayingFieldTable)
        session = Session(bind = self.engine)
        
        for cell in field:
            elem = session.query(PlayingFieldTable).filter(and_(PlayingFieldTable.id_game == cell.id_game, PlayingFieldTable.i == cell.i, PlayingFieldTable.j == cell.j)).first()
            elem.value = cell.value
            session.add(elem)
        session.commit()
        session.close()

    def update_user_info(self, user: UserTable):
        session = Session(bind = self.engine)
        
        elem = session.query(UserTable).filter(UserTable.id_user == user.id_user).first()
        elem.count_games = user.count_games
        elem.count_wins = user.count_wins
        elem.count_lose = user.count_lose
   
        
        session.add(elem)
        session.commit()
        session.close()
        
        
    def get_history_games_for_user(self, id_user):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(CurrentGameTable).filter(
                                                            and_(or_(CurrentGameTable.creator == id_user, CurrentGameTable.enemy == id_user),
                                                            CurrentGameTable.status.notin_(["waiting players", "move X", "move O"])
                                                            )
                                                        ).all()
        
        session.close()
        return result
        
    def get_list_leaders(self, count_leaders):
        result = None
        
        session = Session(bind = self.engine)
        result = session.query(UserTable).order_by(desc(UserTable.count_wins), UserTable.count_lose).limit(count_leaders).all()
        
        session.close()
        return result