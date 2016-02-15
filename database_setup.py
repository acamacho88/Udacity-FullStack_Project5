from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    id = Column(Integer, primary_key=True)

class Artist(Base):
    __tablename__ = 'artist'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class Album(Base):
    __tablename__ = 'album'


    name = Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    year = Column(String(4))
    numtracks = Column(String(2))
    cover = Column(String(250))
    artist_id = Column(Integer,ForeignKey('artist.id'))
    artist = relationship(Artist)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'year'         : self.year,
           'numtracks'         : self.numtracks,
           'cover'          : self.cover,
       }



engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
 

Base.metadata.create_all(engine)
