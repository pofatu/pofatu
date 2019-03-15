from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values
from clld.web.util.helpers import link
from clld.db.util import get_distinct_values

from clld.db.models import common

from pofatu import models


class RefCol(Col):
    __kw__ = dict(bSearchable=False)

    def order(self):
        return Artefact.source_pk

    def format(self, item):
        if item.source:
            return link(self.dt.req, item.source)
        return ''


class Measurements(DataTable):
    __constraints__ = [models.Sample, common.UnitParameter]

    def base_query(self, query):
        if self.sample:
            query = query.join(models.Measurement.unitparameter)
            return query.filter(models.Measurement.sample_pk == self.sample.pk)

        if self.unitparameter:
            query = query.join(models.Measurement.sample)
            return query.filter(models.Measurement.unitparameter_pk == self.unitparameter.pk)

        return query

    def col_defs(self):
        if self.sample:
            res = [
                LinkCol(self, 'parameter', get_object=lambda i: i.unitparameter)
            ]
        elif self.unitparameter:
            res = [
                LinkCol(self, 'sample', get_object=lambda i: i.sample)
            ]
        else:
            res = []
        res.append(Col(self, 'value'))
        return res


def includeme(config):
    config.register_datatable('measurements', Measurements)
