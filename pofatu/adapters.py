from collections import namedtuple

from clld import interfaces
from clld.web.adapters.geojson import GeoJson
from clld.db.meta import DBSession

from pofatu.interfaces import IRockSource
from pofatu.models import ROCKSOURCETYPES

RockSource = namedtuple('RockSource', 'id name type latitude longitude')


class GeoJsonSources(GeoJson):
    def feature_iterator(self, ctx, req):
        for row in DBSession.execute(
            "select id, name, type, latitude, longitude from rocksource where type = '%s'" % req.params['type']
        ):
            yield RockSource(*row)

    def feature_properties(self, ctx, req, feature):
        return {'color': ROCKSOURCETYPES[feature.type]}


def includeme(config):
    config.register_adapter(
        GeoJsonSources, IRockSource, interfaces.IIndex, name=GeoJson.mimetype)
