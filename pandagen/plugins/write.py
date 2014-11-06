# Pandagen

import logging
import os

from .. import pandagen


class Write(pandagen.Plugin):

    def __init__(self, to='build'):
        self.to = to

    def _execute(self, pg):
        for v in pg.data.values():
            path = os.path.join(self.to, v['output'])
            dir = os.path.dirname(path)
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(path, 'w+') as f:
                f.write(v['contents'])
            logging.info('Wrote %s as %s%s.', v['source'], path,
                         ' (`{}`)'.format(v['title'])
                         if 'title' in v else '')
