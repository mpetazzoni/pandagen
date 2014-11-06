# Pandagen

import logging
import slugify

from .. import pandagen


class Slug(pandagen.Plugin):
    """
    Slugify any item property into another.
    """

    def __init__(self, key='title', into='slug'):
        self.key = key
        self.into = into

    def _execute(self, pg):
        for v in pg.data.values():
            v[self.into] = slugify.slugify(unicode(v[self.key]))
