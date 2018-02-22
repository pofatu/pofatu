from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Unit, Language, UnitParameter, UnitValue


ROCKTYPES = {
    'ALKALI BASALT': '#bbccee',
    'BASALT': '#44aa99',
    'BASANITE': '#332288',
    'HAWAIITE': '#117733',
    'LOW SILICA BASANITE': '#999933',
    'MUGEARITE': '#ddcc77',
    'PHONO-TEPHRITE': '#cc6677',
    'PICRITE': '#882255',
    'PICRO-BASALTE': '#aa4499',
    'TEPHRITE ': '#ffffff',
}


@implementer(interfaces.IUnit)
class Sample(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)
    type = Column(Unicode)
    site_context = Column(Unicode)
    site_comment = Column(Unicode)
    rock_type = Column(Unicode)
    tectonic_setting = Column(Unicode)
    location = Column(Unicode)
    latitude = Column(
        Float(),
        CheckConstraint('-90 <= latitude and latitude <= 90'),
        doc='geographical latitude in WGS84')
    longitude = Column(
        Float(),
        CheckConstraint('-180 <= longitude and longitude <= 180 '),
        doc='geographical longitude in WGS84')


@implementer(interfaces.ILanguage)
class Site(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    samples = relationship(Sample)
