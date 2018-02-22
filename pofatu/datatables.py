from clld.web.datatables.base import Col, LinkCol, LinkToMapCol
from clld.web.datatables.unit import Units
from clld.db.models.common import Language
from clld.db.util import get_distinct_values

from pofatu.models import Sample


class Samples(Units):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'type', model_col=Sample.type, choices=get_distinct_values(Sample.type)),
            Col(self, 'rock_type', model_col=Sample.rock_type, choices=get_distinct_values(Sample.rock_type)),
            LinkCol(
                self, 'language', model_col=Language.name, get_obj=lambda i: i.language),
            LinkToMapCol(self, '#'),
        ]


def includeme(config):
    config.register_datatable('units', Samples)
