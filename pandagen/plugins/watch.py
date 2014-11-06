# Pandagen

import logging
import time
import watchdog.events
import watchdog.observers

from .. import pandagen


class Watch(pandagen.Plugin, watchdog.events.FileSystemEventHandler):

    def __init__(self, location='src'):
        self.location = location
        self.observer = self._get_observer()
        self.pg = None

    def _get_observer(self):
        observer = watchdog.observers.Observer()
        observer.schedule(self, self.location, recursive=True)
        return observer

    def on_any_event(self, event):
        if not self.pg:
            # Not yet executed/initialized; shouldn't happen
            return

        logging.info('Change detected. Rebuilding...')
        self.observer.stop()
        self.observer = self._get_observer()
        self.pg.execute()

    def _execute(self, pg):
        logging.warn('Watch plugin does not work yet; skipping...')
        return

        self.pg = pg
        if self.observer.is_alive():
            logging.info('Watch already active.')
            return

        logging.info('Starting watch of %s...', self.location)
        self.observer.start()
        try:
            while self.observer.should_keep_running():
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.observer.stop()
        logging.info('Done watching.')
