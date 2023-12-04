from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings



class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=True)
    sobrenome: str = Column(String(256), nullable=True)
    email: str = Column(String(256), nullable=False, index=True, unique=True)
    senha: str = Column(String(256), nullable=False)
    eh_admin: bool = Column(Boolean, default=False)
    artigos = relationship(
        "ArtigoModel",
        cascade="all,delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )