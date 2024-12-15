from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from datasource.model.base import Base

class CurrentGameTable(Base):
    __tablename__ = 'current_game'
    id_game = Column(UUID(as_uuid=True), primary_key=True)
    creator = Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    type_creator = Column(Integer, nullable=False)
    is_multy = Column(Boolean, nullable=False)
    enemy = Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=True)
    status = Column(String(100), nullable=False)
    data_creator = Column(DateTime, nullable=False)
   
    
   