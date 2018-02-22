from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from pofatu import models

_ = lambda s: s
_('Language')
_('Languages')
_('Unit')
_('Units')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    return config.make_wsgi_app()
