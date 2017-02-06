# Pandagen

import logging
import slugify

from .. import pandagen


class Slug(pandagen.Plugin):
    """
    Slugify any item property into another.
    """

    def __init__(self, key='title', into='slug', overwrite=False):
        self.key = key
        self.into = into
        self.overwrite = overwrite

    def _execute(self, pg):
        for k, v in pg.data.items():
            if self.into not in v or self.overwrite:
                v[self.into] = slugify.slugify(v[self.key])
                logging.debug('Computed slug `%s` for %s', v[self.into], k)
