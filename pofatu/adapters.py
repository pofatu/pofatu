from sqlalchemy.orm import joinedload

from clld import interfaces
from clld.web.adapters.geojson import GeoJson
from clld.db.meta import DBSession
from clld.db.models.common import Unit, Language

from pofatu.models import ROCKTYPES


class GeoJsonSamples(GeoJson):
    def feature_iterator(self, ctx, req):
        q = DBSession.query(Unit).options(joinedload(Unit.language))
        if 'site' in req.params:
            site = Language.get(req.params['site'])
            q = q.filter(Unit.language_pk == site.pk)
        return q

    def feature_properties(self, ctx, req, feature):
        res = GeoJson.feature_properties(self, ctx, req, feature)
        res['type'] = feature.type
        res['color'] = ROCKTYPES.get(feature.rock_type, '#cccccc')
        return res


def includeme(config):
    config.register_adapter(
        GeoJsonSamples, interfaces.IUnit, interfaces.IIndex, name=GeoJson.mimetype)
