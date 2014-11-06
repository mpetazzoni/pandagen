# Pandagen

import glob
import logging
import re

from .. import pandagen


class Ignore(pandagen.Plugin):
    """
    Remove from each resource the key/value pairs that match the given
    glob-style pattern(s). It can be a single pattern given as a string, or a
    list of patterns.
    """

    def __init__(self, patterns):
        if type(patterns) is not list:
            patterns = [patterns]
        self.patterns = map(lambda p: re.compile(glob.fnmatch.translate(p)),
                            patterns)

    def _execute(self, pg):
        for k in pg.data.keys():
            if filter(None, map(lambda p: p.match(k), self.patterns)):
                logging.info('Ignoring %s (pattern mismatch).', k)
                del pg.data[k]
