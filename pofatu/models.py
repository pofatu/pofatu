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
from clld.db.models.common import Language, Source, IdNameDescriptionMixin

from pofatu.interfaces import IRockSource

ROCKSOURCETYPES = {
    'POFATU': '#ff0000',
    'GEOROC': '#0000ff',
}


@implementer(IRockSource)
class RockSource(Base, IdNameDescriptionMixin):
    type = Column(Unicode)  # georoc or pofatu
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
class Artefact(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    site_name = Column(Unicode)
    site_context = Column(Unicode)
    type = Column(Unicode)
    tectonic_setting = Column(Unicode)
    location = Column(Unicode)
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(Source)
