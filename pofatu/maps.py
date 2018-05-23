from base64 import b64encode

from clld.web.maps import Map, Legend, Layer
from clld.web.util.htmllib import HTML
from clld.lib.svg import icon, data_url

from pofatu.models import ROCKSOURCETYPES


class ArtefactsMap(Map):
    def get_options(self):
        res = Map.get_options(self)
        res['max_zoom'] = 15
        res['base_layer'] = 'OpenTopoMap'
        return res


class SourcesMap(Map):
    def get_options(self):
        res = Map.get_options(self)
        res['max_zoom'] = 15
        res['base_layer'] = 'OpenTopoMap'
        res['info_route'] = 'rocksource_alt'
        res['icons'] = 'div'
        return res

    def get_layers(self):
        for name in ROCKSOURCETYPES:
            yield Layer(
                name,
                name,
                self.req.route_url('rocksources_alt', ext='geojson', _query=dict(type=name)))

    #def get_legends(self):
    #    def make_item(label, color):
    #        return HTML.span(
    #            HTML.img(
    #                width=16,
    #                height=16,
    #                src=data_url(icon('s' + color[1:]))),
    #            HTML.span(label, style='padding-left:5px'),
    #            style='padding-left:5px')
    #    items = [make_item(n, c) for n, c in ROCKSOURCETYPES.items()]
    #    yield Legend(self, 'rock types', items)


def includeme(config):
    config.register_map('languages', ArtefactsMap)
    config.register_map('rocksources', SourcesMap)
