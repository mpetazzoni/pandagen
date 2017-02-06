# Pandagen

import jinja2
import logging
import os

from .. import pandagen


class Permalinks(pandagen.Plugin):

    def __init__(self, pattern='{{ date.strftime("%Y/%m/%d") }}/{{ slug }}'):
        self.pattern = jinja2.Template(pattern)

    def _execute(self, pg):
        for k, v in pg.data.items():
            try:
                (head, tail) = os.path.split(v['output'])
                v['path'] = os.path.join(head, self.pattern.render(v))
                v['output'] = os.path.join(v['path'], 'index.html')
                logging.debug('Permalink for %s: %s', k, v['output'])
            except:
                logging.warn(
                    'No permalink defined for %s (missing properties?).', k)
