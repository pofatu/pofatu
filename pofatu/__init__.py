from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from pofatu import models
from pofatu.interfaces import ISite, IMeasurement

from clld.web import app


_ = lambda s: s
_('Language')
_('Languages')
_('Source')
_('Sources')
_('RockSource')
_('RockSources')
_('Rocksource')
_('Rocksources')


#
# FIXME:
# - icon shape to distinguish SOURCE and ARTEFACT
# - icon color to distinguish site context?
#

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.register_resource('measurement', models.Measurement, IMeasurement, with_index=True)
    menuitems = config.registry.settings['clld.menuitems_list']
    config.register_menu(
        ('Artefacts', lambda ctx, req: (req.route_url('parameter', id='artefact'), 'Artefacts')),
        ('Sources', lambda ctx, req: (req.route_url('parameter', id='source'), 'Sources')),
        *menuitems)
    return config.make_wsgi_app()
