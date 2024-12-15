from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from datasource.model.base import Base

class PlayingFieldTable(Base):
    __tablename__ = 'playing_field'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_game = Column(UUID(as_uuid=True), ForeignKey('current_game.id_game'), nullable=False)
    i = Column(Integer, nullable=False)
    j = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
