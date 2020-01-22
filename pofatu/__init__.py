from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from pofatu import models
from pofatu.interfaces import IMeasurement, IMethod

from clld.web import app

_ = lambda s: s
_('Language')
_('Languages')
_('Source')
_('Sources')
_('Value')
_('Values')
_('Parameter')
_('Parameters')


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
    config.register_resource('method', models.Method, IMethod, with_index=True)
    config.register_menu(
        ('About', lambda ctx, req: (req.route_url('about'), 'About')),
        ('Contributions', lambda ctx, req: (req.route_url('contributions'), 'Contributions')),
        ('Samples', lambda ctx, req: (req.route_url('values'), 'Samples')),
        ('References', lambda ctx, req: (req.route_url('sources'), 'References')),
    )
    return config.make_wsgi_app()
