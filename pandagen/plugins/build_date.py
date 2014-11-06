# Pandagen

import datetime
import logging

from .. import pandagen


class BuildDate(pandagen.Plugin):
    """
    Add the UTC build time to the metadata.
    """

    def __init__(self, field='builddate'):
        self.field = field

    def _execute(self, pg):
        pg.metadata[self.field] = datetime.datetime.utcnow()
        logging.info('Set build date to %s.', pg.metadata[self.field])
