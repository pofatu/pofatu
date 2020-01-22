from base64 import b64encode

from clld.web.maps import Map, Legend, Layer
from clld.web.util.htmllib import HTML
from clld.web.adapters.geojson import GeoJson, get_lonlat
from clldutils.svg import icon, data_url


class SampleGeoJson(GeoJson):
    def feature_iterator(self, ctx, req):
        return [ctx]


class SampleMap(Map):

    def get_layers(self):
        yield Layer(
            self.ctx.id,
            self.ctx.name,
            SampleGeoJson(self.ctx).render(self.ctx, self.req, dump=False))

    def get_default_options(self):
        return {
            'base_layer': "Esri.WorldImagery",
            'center': list(reversed(get_lonlat(self.ctx) or [0, 0])),
            'max_zoom': 25,
            'no_popup': True,
            'no_link': True,
            'sidebar': True}



def includeme(config):
    config.register_map('value', SampleMap)
