from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(100), nullable=False)
    is_premium_client = Column(Boolean)

    links = relationship("LinkModel", back_populates="client")


class LinkModel(Base):
    __tablename__ = "linkmodel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    original_link = Column(String(250), nullable=False)
    shortened_link = Column(String(100), unique=True, nullable=False)
    creation_date = Column(String(100), nullable=False)
    access_counter = Column(Integer, nullable=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="links")
    