# Pandagen

import logging
import os
import shutil

from .. import pandagen


class Static(pandagen.Plugin):
    """
    Copy a directory of static resources into the given destination folder. By
    default, copies static/ under the build/ folder.
    """

    def __init__(self, src='static', dst='build'):
        self.src = os.path.relpath(src)
        self.dst = os.path.relpath(dst)

    def _execute(self, pg):
        if not os.path.exists(self.src) or not os.path.isdir(self.src):
            logging.warn('Static data directory %s does not exist.', self.src)
            return

        if not os.path.exists(self.dst):
            os.makedirs(self.dst)

        logging.info('Copying directory %s into %s...', self.src, self.dst)
        shutil.copytree(self.src, os.path.join(self.dst, self.src))
