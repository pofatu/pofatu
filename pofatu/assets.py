from clld.web.assets import environment
from clldutils.path import Path

import pofatu


environment.append_path(
    Path(pofatu.__file__).parent.joinpath('static').as_posix(),
    url='/pofatu:static/')
environment.load_path = list(reversed(environment.load_path))
