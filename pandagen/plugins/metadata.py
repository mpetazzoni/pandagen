# Pandagen

import logging
import yaml

from .. import pandagen


class Metadata(pandagen.Plugin):
    """
    Load YAML metadata from the given set of files into their corresponding
    key.
    """

    def __init__(self, **kwargs):
        self.imports = kwargs

    def _execute(self, pg):
        for k, v in self.imports.items():
            if k in pg.metadata:
                logging.warning('Key %s is already present in metadata!', k)
            with open(v) as f:
                pg.metadata[k] = yaml.load(f)
            logging.info('Loaded metadata from %s into %s.', v, k)
