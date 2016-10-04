# Pandagen

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
        for v in pg.data.values():
            if self.into not in v or self.overwrite:
                v[self.into] = slugify.slugify(unicode(v[self.key]))
