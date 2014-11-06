# Pandagen

import logging
import os
import shutil

from .. import pandagen


class Clean(pandagen.Plugin):
    """
    Removes the target directory. Useful when used before the static and write
    plugins.
    """

    def __init__(self, target='build'):
        self.target = target

    def _execute(self, pg):
        if not os.path.exists(self.target):
            return

        logging.info('Removing %s...', self.target)
        shutil.rmtree(self.target)
