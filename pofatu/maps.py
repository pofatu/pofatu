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
            'center': list(reversed(get_lonlat(self.ctx) or [0, 0])),
            'max_zoom': 25,
            'no_popup': True,
            'no_link': True,
            'sidebar': True}


class SamplesMap(Map):
    def get_layers(self):
        """Generate the list of layers.

        :return: list or generator of :py:class:`clld.web.maps.Layer` instances.
        """
        route_params = {'ext': 'geojson'}
        yield Layer(
            'locations',
            'Locations',
            self.req.route_url('languages_alt', **route_params))

    def get_default_options(self):
        return {
            'max_zoom': 25,
        }


def includeme(config):
    config.register_map('value', SampleMap)
    config.register_map('values', SamplesMap)
