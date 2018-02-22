from base64 import b64encode

from clld.web.maps import Map, Legend, Layer
from clld.web.util.htmllib import HTML

from pofatu.models import ROCKTYPES, Site


def icon_uri(color):
    svg = """\
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     height="20"
     width="20">
    <circle cx="10" cy="10" r="8" style="stroke:#000000; fill:{0}" opacity="0.8"/>
</svg>""".format(color)
    return 'data:image/svg+xml;base64,%s' % b64encode(svg.encode('utf8')).decode()


class SamplesMap(Map):
    def get_options(self):
        res = Map.get_options(self)
        res['max_zoom'] = 15
        res['base_layer'] = 'OpenTopoMap'
        res['info_route'] = 'unit_alt'
        res['icons'] = 'div'
        if isinstance(self.ctx, Site):
            res['sidebar'] = True
        return res

    def get_layers(self):
        """Generate the list of layers.

        :return: list or generator of :py:class:`clld.web.maps.Layer` instances.
        """
        if isinstance(self.ctx, Site):
            yield Layer(
                self.ctx.id,
                '%s' % self.ctx,
                self.req.route_url('units_alt', ext='geojson', _query=dict(site=self.ctx.id)))
        else:
            for layer in Map.get_layers(self):
                yield layer

    def get_legends(self):
        #for legend in Map.get_legends(self):
        #    yield legend

        def make_item(label, color):
            return HTML.span(
                HTML.img(
                    width=16,
                    height=16,
                    src=icon_uri(color)),
                HTML.span(label, style='padding-left:5px'),
                style='padding-left:5px')

        items = [make_item(n, c) for n, c in ROCKTYPES.items()]
        yield Legend(self, 'rock types', items)


def includeme(config):
    config.register_map('language', SamplesMap)
    config.register_map('units', SamplesMap)
