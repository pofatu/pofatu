import itertools

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
from pofatu.interfaces import IAnalysis, IMeasurement, IMethod


@implementer(interfaces.ILanguage)
class Location(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    region = Column(Unicode)
    subregion = Column(Unicode)
    location = Column(Unicode)


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
    sample_name = Column(Unicode)
    sample_comment = Column(Unicode)
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
    petrography = Column(Unicode)

    site_name = Column(Unicode)
    site_code = Column(Unicode)
    site_context = Column(Unicode)
    site_comment = Column(Unicode)
    site_stratigraphic_position = Column(Unicode)
    site_stratigraphy_comment = Column(Unicode)

    artefact_id = Column(Unicode)
    artefact_name = Column(Unicode)
    artefact_category = Column(Unicode)
    artefact_attributes = Column(Unicode)
    artefact_comment = Column(Unicode)
    artefact_collector = Column(Unicode)
    artefact_collection_type = Column(Unicode)
    artefact_fieldwork_date = Column(Unicode)
    artefact_collection_location = Column(Unicode)
    artefact_collection_comment = Column(Unicode)

    @property
    def source_dict(self):
        res = {}
        for type_, refs in itertools.groupby(
                sorted(self.references, key=lambda r: r.description), lambda r: r.description):
            res[type_] = [r.source for r in refs]
        return res


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
    number_of_replicates = Column(Unicode)
    reference_sample = Column(Unicode)
    instrument = Column(Unicode)
    date = Column(Unicode)
    comment = Column(Unicode)
    detection_limit = Column(Unicode)
    detection_limit_unit = Column(Unicode)
    total_procedural_blank_value = Column(Unicode)
    total_procedural_unit = Column(Unicode)


class MethodReference(Base):
    sample_name = Column(Unicode)
    sample_measured_value = Column(Unicode)
    uncertainty = Column(Unicode)
    uncertainty_unit = Column(Unicode)
    number_of_measurements = Column(Unicode)
    method_pk = Column(Integer, ForeignKey('method.pk'), nullable=False)
    method = relationship(Method, innerjoin=True, backref="references")

    def as_string(self):
        res = self.sample_name
        if self.sample_measured_value:
            if res:
                res += ': '
            res += str(self.sample_measured_value)
        if self.uncertainty:
            res += ' ±'
            res += self.uncertainty
        if self.uncertainty_unit:
            res += ' '
            res += self.uncertainty_unit
        if self.number_of_measurements:
            res += ' (N={0})'.format(self.number_of_measurements)
        return res


class Normalization(Base):
    reference_sample_name = Column(Unicode)
    reference_sample_accepted_value = Column(Unicode)
    citation = Column(Unicode)
    method_pk = Column(Integer, ForeignKey('method.pk'), nullable=False)
    method = relationship(Method, innerjoin=True, backref="normalizations")


@implementer(IAnalysis)
class Analysis(Base, IdNameDescriptionMixin):
    sample_pk = Column(Integer, ForeignKey('sample.pk'))
    sample = relationship(Sample, backref="analyses")

    analyzed_material_1 = Column(Unicode)
    analyzed_material_2 = Column(Unicode)
    sample_preparation = Column(Unicode)
    chemical_treatment = Column(Unicode)
    technique = Column(Unicode)
    laboratory = Column(Unicode)
    analyst = Column(Unicode)

    @property
    def title(self):
        res = 'Analysis'
        if self.analyst:
            res += ' by {0}'.format(self.analyst)
        if self.laboratory:
            res += ' at {0}'.format(self.laboratory)
        return res


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
