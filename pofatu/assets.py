import pathlib

from clld.web.assets import environment

import pofatu


environment.append_path(
    str(pathlib.Path(pofatu.__file__).parent.joinpath('static')), url='/pofatu:static/')
environment.load_path = list(reversed(environment.load_path))
