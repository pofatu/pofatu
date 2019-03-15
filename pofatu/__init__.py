from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from pofatu import models
from pofatu.interfaces import ISite, IMeasurement

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
    return config.make_wsgi_app()
