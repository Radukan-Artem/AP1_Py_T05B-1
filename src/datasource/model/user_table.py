from sqlalchemy import Integer, String, Column
from sqlalchemy.dialects.postgresql import UUID, BYTEA

from datasource.model.base import Base

class UserTable(Base):
    __tablename__ = 'user'
    id_user = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String(100), nullable=False)
    password = Column(BYTEA(), nullable=False)
    count_games = Column(Integer, nullable=False)
    count_wins = Column(Integer, nullable=False)
    count_lose = Column(Integer, nullable=False)
