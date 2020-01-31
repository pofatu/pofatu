from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DataTable, IdCol, DetailsRowLinkCol
from clld.web.datatables.value import Values
from clld.web.datatables.contribution import Contributions
from clld.web.datatables.unitparameter import Unitparameters
from clld.web.datatables.source import Sources
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.db.util import get_distinct_values

from clld.db.models import common

from pofatu import models


class Refs(Sources):
    def col_defs(self):
        res = Sources.col_defs(self)
        res[0].__kw__['button_text'] = 'citation'
        return res


class ValueCol(Col):
    def format(self, item):
        return item.as_string()


class StatsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False, 'sTitle': 'Summary for the measured parameter'}

    def format(self, item):
        return HTML.ul(*[
            HTML.li('Min: {0.min:.2f}'.format(item.unitparameter)),
            HTML.li('Max: {0.max:.2f}'.format(item.unitparameter)),
            HTML.li('Mean: {0.mean:.2f}'.format(item.unitparameter)),
            HTML.li('Median: {0.median:.2f}'.format(item.unitparameter)),
        ], **{'class': 'inline'})


class Measurements(DataTable):
    __constraints__ = [models.Analysis, common.UnitParameter]

    def base_query(self, query):
        if self.analysis:
            query = query.join(models.Measurement.unitparameter)
            return query.filter(models.Measurement.analysis_pk == self.analysis.pk)

        if self.unitparameter:
            query = query.join(models.Measurement.analysis).join(models.Analysis.sample)
            return query.filter(models.Measurement.unitparameter_pk == self.unitparameter.pk)

        return query.outerjoin(models.Measurement.method)

    def col_defs(self):
        if self.analysis:
            res = [
                LinkCol(self, 'parameter', get_object=lambda i: i.unitparameter, model_col=common.UnitParameter.name),
            ]
        elif self.unitparameter:
            res = [
                IdCol(self, 'sample', get_object=lambda i: i.analysis.sample, model_col=common.Value.id)
            ]
        else:
            res = []
        res.append(ValueCol(self, 'value'))
        if self.analysis:
            res.append(StatsCol(self, 'stats'))
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


class SampleIdCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.id}


class CategoryCol(LinkCol):
    def get_attrs(self, item):
        return {'label': item.domainelement.name}


class Samples(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        query = query.join(common.DomainElement)
        if not any({self.language, self.contribution, self.parameter}):
            query = query.join(common.Language)
        return query.distinct()

    def col_defs(self):
        res = [
            SampleIdCol(self, 'sample', model_col=common.Value.id),
            Col(self, 'artefact', model_col=models.Sample.artefact_id),
        ]
        if not self.parameter:
            res.append(CategoryCol(
                self,
                'type',
                choices=get_distinct_values(common.DomainElement.name),
                model_col=common.DomainElement.name))
        if self.parameter:
            res.append(LinkCol(self, 'contribution', get_object=lambda v: v.valueset.contribution))
        if self.contribution:
            pass
        if not self.language:
            res.extend([
                RegionCol(self, 'region', choices=get_distinct_values(models.Location.region)),
                SubRegionCol(self, 'subregion'),
            ])
        return res


class SourcesCol(Col):
    def format(self, item):
        return HTML.ul(*[HTML.li(link(self.dt.req, r.source)) for r in item.references])


class PofatuContributions(Contributions):
    def col_defs(self):
        return [
            IdCol(self, 'id'),
            Col(self, 'name', sTitle='Title'),
            Col(self, 'description', sTitle='Abstract'),
            SourcesCol(self, 'sources', bSearchable=False, bSortable=False)
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
    config.register_datatable('sources', Refs)
