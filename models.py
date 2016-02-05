from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, TEXT, TINYINT, VARCHAR
from sqlalchemy.ext.associationproxy import association_proxy

'''This example shows a few things:
- sqlalchemy's 'declarative mapping' style
- polymorphic inheritance
- what I learned you cannot have a polymorphic child mapping of a polymorphic object.
'''

Base = declarative_base()

from session_manager import session
from session_manager import engine

def save(func):
    '''save decorator'''
    def inner(*args, **kwargs): #1
        session.add(args[0])
        session.commit()
        return func(*args, **kwargs) #2
    return inner

##
## ORGS
##

'''OrgEntity to Images mapping table'''
orgentity_image_map = Table('orgentity_image_map', Base.metadata,
    Column('orgentity_id', Integer, ForeignKey('orgentity.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('image.id'), primary_key=True)
)

'''OrgEntity to Links mapping table'''
orgentity_link_map = Table('orgentity_link_map', Base.metadata,
    Column('orgentity_id', Integer, ForeignKey('orgentity.id'), primary_key=True),
    Column('link_id', Integer, ForeignKey('link.id'), primary_key=True)
)

'''OrgEntity to ShowEntity mapping table'''
orgentity_showentity_map = Table('orgentity_showentity_map', Base.metadata,
    Column('orgentity_id', Integer, ForeignKey('orgentity.id'), primary_key=True),
    Column('showentity_id', Integer, ForeignKey('showentity.id'), primary_key=True)
)


class OrgEntity(Base):
    """
    This is the CORE atom, star table
    """
    __tablename__ = "orgentity"

    id = Column(Integer, primary_key=True)
    guid = Column(VARCHAR(50))
    name = Column(VARCHAR(50))
    slug = Column(VARCHAR(50))
    creation_date = Column(DATETIME())
    last_modified = Column(DATETIME())
    available_from = Column(DATETIME())

    type = Column(String(50)) # key to polymorphic table
    images = relationship("Image", secondary=orgentity_image_map)
    links = relationship("Link", secondary=orgentity_link_map)

    __mapper_args__ = {
        'polymorphic_identity':'orgentity',
        'polymorphic_on':type
    }

    def __init__(self, name):
        """"""
        self.name = name

    @save
    def save(self):
        pass

    def authorize(self):
        pass

    def publish(self):
        pass

    def search(self):
        pass


class Station(OrgEntity):
    __tablename__ = 'orgentity_station'
    id = Column(Integer, ForeignKey('orgentity.id'), primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'orgentity_station',
        'polymorphic_on':type
    }


class Producer(OrgEntity):
    __tablename__ = 'orgentity_producer'
    id = Column(Integer, ForeignKey('orgentity.id'), primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'orgentity_producer',
        'polymorphic_on':type
    }


class Distributor(OrgEntity):
    __tablename__ = 'orgentity_distributor'
    id = Column(Integer, ForeignKey('orgentity.id'), primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'orgentity_distributor',
        'polymorphic_on':type
    }


class Audience(OrgEntity):
    __tablename__ = 'orgentity_audience'
    id = Column(Integer, ForeignKey('orgentity.id'), primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'orgentity_audience',
        'polymorphic_on':type
    }

##
## BASE OBJS
##

class Season(Base):
    __tablename__ = 'season'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ordinal = Column(Integer)

    @save
    def save(self):
        pass


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    @save
    def save(self):
        pass


class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    @save
    def save(self):
        pass


class SeasonAssociation(Base):
    """tightly bound object between series/ep/season"""
    __tablename__ = "series_ep_season"
    series_id = Column(Integer, ForeignKey('series_base.id'), primary_key=True)
    episode_id = Column(Integer, ForeignKey('episode_base.id'), primary_key=True)
    season_id = Column(Integer, ForeignKey('season.id'), primary_key=True)

    episode = relationship("AbstractEpisode", back_populates="series")
    #series = relationship("AbstractSeries", back_populates="episode")
    series = relationship("AbstractSeries")
    season = relationship("Season")

    @save
    def save(self):
        pass

##
## SHOW ENTITY
##

'''Generic children map, aggregates objs of base kind'''
object_aggregate = Table('object_aggregate', Base.metadata,
    Column('parent_id', Integer, ForeignKey('showentity.id'), primary_key=True),
    Column('child_id', Integer, ForeignKey('showentity.id'), primary_key=True)
)

'''Parent Series to OTOs mapping table'''
series_oto_map = Table('series_otos_map', Base.metadata,
    Column('series_parent_id', Integer, ForeignKey('series_parent.id'), primary_key=True),
    Column('episode_oto_id', Integer, ForeignKey('episode_oto.id'), primary_key=True)
)

'''ShowEntity to Images mapping table'''
showentity_image_map = Table('showentity_image_map', Base.metadata,
    Column('showentity_id', Integer, ForeignKey('showentity.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('image.id'), primary_key=True)
)

'''ShowEntity to Links mapping table'''
showentity_link_map = Table('showentity_link_map', Base.metadata,
    Column('showentity_id', Integer, ForeignKey('showentity.id'), primary_key=True),
    Column('link_id', Integer, ForeignKey('link.id'), primary_key=True)
)

'''Series to Subseries (aka Parent to Child Series) mapping table'''
subseries_map = Table('series_parent_child_map', Base.metadata,
    Column('series_parent_id', Integer, ForeignKey('series_parent.id'), primary_key=True),
    Column('series_child_id', Integer, ForeignKey('series_child.id'), primary_key=True)
)


class ShowEntity(Base):
    """
    This is the CORE atom, star table

    SHOULD WE NAME THIS 'SHOW'?!

    """
    __tablename__ = "showentity"

    id = Column(Integer, primary_key=True)
    guid = Column(VARCHAR(50))
    name = Column(VARCHAR(50))
    slug = Column(VARCHAR(50))
    creation_date = Column(DATETIME())
    last_modified = Column(DATETIME())
    available_from = Column(DATETIME())
    children = relationship("ShowEntity", secondary=object_aggregate,
                           primaryjoin=id==object_aggregate.c.parent_id,
                           secondaryjoin=id==object_aggregate.c.child_id,)
    orgs = relationship("OrgEntity", secondary=orgentity_showentity_map)


    type = Column(String(50)) # key to polymorphic table
    images = relationship("Image", secondary=showentity_image_map)
    links = relationship("Link", secondary=showentity_link_map)

    __mapper_args__ = {
        'polymorphic_identity':'showentity',
        'polymorphic_on':type
    }

    def __init__(self, name):
        """"""
        self.name = name

    @save
    def save(self):
        pass

    def authorize(self):
        pass

    def publish(self):
        pass

    def search(self):
        pass


class AbstractSeries(ShowEntity):
    """this is an Abstract Series, never to be instantiated itself. . .

    but does provide season association as a functionality for descendants"""
    __tablename__ = 'series_base'
    id = Column(Integer, ForeignKey('showentity.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    season_associations = relationship("SeasonAssociation")

    tags = relationship("SeriesRelationTag", foreign_keys="[SeriesRelationTag.series_parent_id]")

    children = association_proxy('br1', 'child')
    parents = association_proxy('br2', 'parent')

    __mapper_args__ = {
        'polymorphic_identity':'series_base',
        'polymorphic_on':type
    }


class Series(AbstractSeries):
    __tablename__ = 'series_parent'
    id = Column(Integer, ForeignKey('series_base.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))

    franchise_id = Column(Integer, ForeignKey('franchise.id'))
    franchise = relationship("Franchise", back_populates="serieses", foreign_keys=[franchise_id])

    subseries = relationship("SubSeries", secondary=subseries_map)

    onetimeonlys = relationship("OneTimeOnlyEpisode", secondary=series_oto_map)

    __mapper_args__ = {
        'polymorphic_identity':'series_parent',
        'polymorphic_on':type
    }


class SubSeries(AbstractSeries):
    __tablename__ = 'series_child'
    id = Column(Integer, ForeignKey('series_base.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    parents = relationship("Series", secondary=subseries_map, back_populates="subseries")
    __mapper_args__ = {
        'polymorphic_identity':'series_child',
        'polymorphic_on':type
    }


class AbstractEpisode(ShowEntity):
    __tablename__ = 'episode_base'
    id = Column(Integer, ForeignKey('showentity.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    series = relationship("SeasonAssociation", back_populates="episode")

    __mapper_args__ = {
        'polymorphic_identity':'episode',
        'polymorphic_on':type
    }


class SeriesEpisode(AbstractEpisode):
    __tablename__ = 'episode_series'
    id = Column(Integer, ForeignKey('episode_base.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'episode_series',
        'polymorphic_on':type
    }


class OneTimeOnlyEpisode(AbstractEpisode):
    __tablename__ = 'episode_oto'
    id = Column(Integer, ForeignKey('episode_base.id'), primary_key=True)
    name = Column(String(50))
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'episode_oto',
        'polymorphic_on':type
    }


class Franchise(ShowEntity):
    __tablename__ = 'franchise'
    id = Column(Integer, ForeignKey('showentity.id'), primary_key=True)
    type = Column(String(50))

    serieses = relationship("Series", order_by=Series.id, back_populates="franchise", foreign_keys="[Series.franchise_id]")

    __mapper_args__ = {
        'polymorphic_identity':'franchise',
        'polymorphic_on':type
    }


class SeriesRelationTag(Base):
    """tightly bound object between series/ep/season"""
    __tablename__ = "series_relation_tag"
    id = Column(Integer, primary_key=True)
    series_parent_id = Column(Integer, ForeignKey('series_base.id'),)
    series_child_id = Column(Integer, ForeignKey('series_base.id'), )
    tag = Column(String(50))
    parent = relationship("AbstractSeries",
                          primaryjoin=series_parent_id==AbstractSeries.id,
                          backref='br1'
                          )
    child = relationship("AbstractSeries",
                          primaryjoin=series_child_id==AbstractSeries.id,
                          backref='br2'
                          )

    @save
    def save(self):
        pass



Base.metadata.create_all(engine)
