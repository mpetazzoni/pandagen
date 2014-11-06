# Pandagen

import logging
import os

from .. import pandagen


class LocationRewrite(pandagen.Plugin):
    """
    Rewrite the path of loaded resources (by prefix).
    """

    def __init__(self, prefix, dest):
        self.prefix = prefix
        self.dest = dest

    def _execute(self, pg):
        for v in pg.data.values():
            if v['output'].startswith(self.prefix):
                v['output'] = v['output'].replace(self.prefix, self.dest, 1)


class ExtensionRewrite(pandagen.Plugin):
    """
    Rewrite output extensions.
    """

    def __init__(self, from_ext, to_ext):
        self.from_ext = from_ext
        self.to_ext = to_ext

    def _execute(self, pg):
        for v in pg.data.values():
            s = os.path.splitext(v['output'])
            if s[1] == self.from_ext:
                v['output'] = s[0] + self.to_ext
                logging.info('Changed output extension to %s for %s.',
                             self.to_ext, v['output'])
