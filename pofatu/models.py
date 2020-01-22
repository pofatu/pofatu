from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    Boolean,
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import joinedload, relationship

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Language, Source, Value, Contribution, UnitParameter, HasSourceMixin, IdNameDescriptionMixin,
)
from pofatu.interfaces import IAnalysis, IMeasurement, IMethod, ISite


@implementer(interfaces.ILanguage)
class Location(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    region = Column(Unicode)
    subregion = Column(Unicode)
    location = Column(Unicode)


@implementer(ISite)
class Site(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.IValue)
class Sample(CustomModelMixin, Value):
    """
    A Sample has
    - a location - via valueset
    - a contribution - via valueset
    - a domainelement: namely, Sample category
    - multiple Analyses
    """
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    latitude = Column(
        Float(),
        CheckConstraint('-90 <= latitude and latitude <= 90'),
        doc='geographical latitude in WGS84')
    longitude = Column(
        Float(),
        CheckConstraint('-180 <= longitude and longitude <= 180 '),
        doc='geographical longitude in WGS84')
    elevation = Column(Unicode)
    location_comment = Column(Unicode)

    site_pk = Column(Integer, ForeignKey('site.pk'), nullable=False)
    site = relationship(Site, innerjoin=True, backref='samples')

    site_context = Column(Unicode)
    site_comment = Column(Unicode)
    site_stratigraphic_position = Column(Unicode)

    def iter_grouped_sources(self):
        for type_ in ['data', 'artefact', 'site']:
            res = [ref.source for ref in self.references if ref.description == type_]
            if res:
                yield type_, res


class SampleReference(Base, HasSourceMixin):
    __table_args__ = (UniqueConstraint('sample_pk', 'source_pk', 'description'),)

    sample_pk = Column(Integer, ForeignKey('sample.pk'), nullable=False)
    sample = relationship(Sample, innerjoin=True, backref="references")


@implementer(interfaces.IUnitParameter)
class Param(CustomModelMixin, UnitParameter):
    pk = Column(Integer, ForeignKey('unitparameter.pk'), primary_key=True)
    min = Column(Float)
    max = Column(Float)
    mean = Column(Float)
    median = Column(Float)
    count_values = Column(Integer)


@implementer(IMethod)
class Method(Base, IdNameDescriptionMixin):
    code = Column(Unicode)
    parameter = Column(Unicode)
    reference_sample = Column(Unicode)
    technique = Column(Unicode)
    instrument = Column(Unicode)
    laboratory = Column(Unicode)
    analyst = Column(Unicode)
    date = Column(Unicode)
    comment = Column(Unicode)


@implementer(IAnalysis)
class Analysis(Base, IdNameDescriptionMixin):
    sample_pk = Column(Integer, ForeignKey('sample.pk'))
    sample = relationship(Sample, backref="analyses")


@implementer(IMeasurement)
class Measurement(Base, IdNameDescriptionMixin):
    __table_args__ = (UniqueConstraint('analysis_pk', 'unitparameter_pk'),)

    value = Column(Float)
    less = Column(Boolean)
    precision = Column(Float)
    sigma = Column(Integer)

    analysis_pk = Column(Integer, ForeignKey('analysis.pk'), nullable=False)
    analysis = relationship(Analysis, innerjoin=True, backref="measurements")

    method_pk = Column(Integer, ForeignKey('method.pk'))
    method = relationship(Method)

    unitparameter_pk = Column(Integer, ForeignKey('unitparameter.pk'), nullable=False)
    unitparameter = relationship(UnitParameter, innerjoin=True, backref="values")


    def as_string(self):
        res = '{0}{1}'.format('\u2264' if self.less else '', self.value)
        if self.precision:
            res += '±{0}'.format(self.precision)
        if self.sigma:
            res += '{0}σ'.format(self.sigma)
        return res
