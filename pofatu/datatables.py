from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DataTable, IdCol, DetailsRowLinkCol
from clld.web.datatables.value import Values
from clld.web.datatables.contribution import Contributions
from clld.web.datatables.unitparameter import Unitparameters
from clld.web.util.htmllib import HTML
from clld.db.util import get_distinct_values

from clld.db.models import common

from pofatu import models


class ValueCol(Col):
    def format(self, item):
        return item.as_string()


class Measurements(DataTable):
    __constraints__ = [models.Analysis, common.UnitParameter]

    def base_query(self, query):
        if self.analysis:
            query = query.join(models.Measurement.unitparameter)
            return query.filter(models.Measurement.analysis_pk == self.analysis.pk)

        if self.unitparameter:
            query = query.join(models.Measurement.analysis)
            return query.filter(models.Measurement.unitparameter_pk == self.unitparameter.pk)

        return query.outerjoin(models.Measurement.method)

    def col_defs(self):
        if self.analysis:
            res = [
                LinkCol(self, 'parameter', get_object=lambda i: i.unitparameter, model_col=common.UnitParameter.name)
            ]
        elif self.unitparameter:
            res = [
                LinkCol(self, 'sample', get_object=lambda i: i.sample, model_col=common.Value.name)
            ]
        else:
            res = []
        res.append(ValueCol(self, 'value'))
        res.append(DetailsRowLinkCol(self, 'method', button_text='method'))
        return res


class RegionCol(Col):
    def format(self, item):
        return item.valueset.language.region

    def order(self):
        return models.Location.region

    def search(self, qs):
        return models.Location.region == qs


class SubRegionCol(Col):
    def format(self, item):
        return item.valueset.language.subregion

    def order(self):
        return models.Location.subregion

    def search(self, qs):
        return models.Location.subregion.contains(qs)


class Samples(Values):
    def col_defs(self):
        res = [LinkCol(self, 'sample', model_col=common.Value.name)]
        if self.language:
            res.append(LinkCol(self, 'type', get_object=lambda v: v.valueset.parameter))
        if self.parameter:
            res.append(LinkCol(self, 'contribution', get_object=lambda v: v.valueset.contribution))
        if self.contribution:
            res.append(LinkCol(self, 'type', get_object=lambda v: v.valueset.parameter))
        if not self.language:
            res.extend([
                RegionCol(self, 'region', choices=get_distinct_values(models.Location.region)),
                SubRegionCol(self, 'subregion'),
            ])
        return res


class PofatuContributions(Contributions):
    def col_defs(self):
        return [
            IdCol(self, 'id'),
            Col(self, 'name', sTitle='Title'),
            Col(self, 'description', sTitle='Abstract'),
            LinkCol(self, 'source', get_object=lambda i: i.source, bSearchable=False, bSortable=False)
        ]


class Params(Unitparameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'min', model_col=models.Param.min),
            Col(self, 'max', model_col=models.Param.max),
            Col(self, 'mean', model_col=models.Param.mean),
            Col(self, 'median', model_col=models.Param.median),
            Col(self, '# samples', model_col=models.Param.count_values),
        ]



def includeme(config):
    config.register_datatable('contributions', PofatuContributions)
    config.register_datatable('values', Samples)
    config.register_datatable('unitparameters', Params)
    config.register_datatable('measurements', Measurements)
