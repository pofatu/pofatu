from clld.web.datatables.base import Col, LinkCol, LinkToMapCol, DataTable
from clld.web.datatables.language import Languages
from clld.web.util.helpers import link
from clld.db.util import get_distinct_values

from pofatu.models import Artefact, RockSource


class RefCol(Col):
    __kw__ = dict(bSearchable=False)

    def order(self):
        return Artefact.source_pk

    def format(self, item):
        if item.source:
            return link(self.dt.req, item.source)
        return ''


class Artefacts(Languages):
    def col_defs(self):
        return [
            Col(self, 'name', model_col=Artefact.name),
            Col(self, 'type', model_col=Artefact.type, choices=get_distinct_values(Artefact.type)),
            Col(self, 'site_name', model_col=Artefact.site_name),
            Col(self, 'site_context', model_col=Artefact.site_context, choices=get_distinct_values(Artefact.site_context)),
            RefCol(self, 'reference'),
            LinkToMapCol(self, '#'),
        ]


class RockSources(DataTable):
    def col_defs(self):
        return [
            Col(self, 'tectonic_setting', model_col=RockSource.tectonic_setting),
            Col(self, 'location', model_col=RockSource.location),
            Col(self, 'sample_name', model_col=RockSource.name),
            Col(self, 'type', model_col=RockSource.type, choices=get_distinct_values(RockSource.type)),
            # TODO: References!
            LinkToMapCol(self, '#'),
        ]


def includeme(config):
    config.register_datatable('languages', Artefacts)
    config.register_datatable('rocksources', RockSources)
