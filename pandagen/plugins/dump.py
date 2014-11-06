# Pandagen

import pprint

from .. import pandagen


class Dump(pandagen.Plugin):
    """
    Pretty-prints the metadata and the data of the Pandagen pipeline on stdout.
    """

    def _execute(self, pg):
        pprint.pprint(pg.metadata)
        pprint.pprint(pg.data)
