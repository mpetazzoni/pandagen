# Pandagen

import datetime
import logging

from .. import pandagen


class Readingtime(pandagen.Plugin):
    """Computes an estimated reading time and seeds it into each resource's
    data."""

    def __init__(self, wpm=200, into='reading_time'):
        self.wpm = wpm
        self.into = into

    def _execute(self, pg):
        for k, v in pg.data.items():
            if 'contents' not in v:
                continue
            words = len(filter(None, v['contents'].split()))
            reading_time = words / (self.wpm / 60.0)
            v[self.into] = datetime.timedelta(seconds=reading_time)
            logging.info('Computed reading time of %s (%d words): %s seconds.',
                         k, words, reading_time)
