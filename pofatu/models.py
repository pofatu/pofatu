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
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Language, Source, Value, Contribution, UnitParameter, HasSourceMixin, IdNameDescriptionMixin

from pofatu.interfaces import ISite, IMeasurement, IMethod


ROCKSOURCETYPES = {
    'POFATU': '#ff0000',
    'GEOROC': '#0000ff',
}


@implementer(interfaces.IContribution)
class PofatuContribution(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(Source)


@implementer(interfaces.ILanguage)
class Location(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    region = Column(Unicode)
    subregion = Column(Unicode)
    location = Column(Unicode)
    elevation = Column(Unicode)


@implementer(interfaces.IValue)
class Sample(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)

    site_name = Column(Unicode)
    site_context = Column(Unicode)
    type = Column(Unicode)
    tectonic_setting = Column(Unicode)
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(Source)

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


@implementer(IMeasurement)
class Measurement(Base):
    __table_args__ = (UniqueConstraint('sample_pk', 'unitparameter_pk', 'method_pk'),)

    value = Column(Float)
    less = Column(Boolean)
    precision = Column(Float)
    sigma = Column(Integer)
    sample_pk = Column(Integer, ForeignKey('sample.pk'), nullable=False)
    sample = relationship(Sample, innerjoin=True, backref="values")
    unitparameter_pk = Column(Integer, ForeignKey('unitparameter.pk'), nullable=False)
    unitparameter = relationship(UnitParameter, innerjoin=True, backref="values")
    method_pk = Column(Integer, ForeignKey('method.pk'))
    method = relationship(Method, innerjoin=True, backref="measurement_assocs")


    def as_string(self):
        res = '{0}{1}'.format('\u2264' if self.less else '', self.value)
        if self.precision:
            res += '±{0}'.format(self.precision)
        if self.sigma:
            res += '{0}σ'.format(self.sigma)
        return res
