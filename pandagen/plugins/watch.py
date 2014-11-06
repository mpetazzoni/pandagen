# Pandagen

import logging
import watchdog.events
import watchdog.observers

from .. import pandagen


class Watch(pandagen.Plugin, watchdog.events.FileSystemEventHandler):

    def __init__(self, location='src'):
        self.location = location
        self.observer = watchdog.observers.Observer()
        self.observer.daemon = False
        self.observer.schedule(self, location, recursive=True)
        self.pg = None

    def on_any_event(self, event):
        if self.pg:
            logging.info('Change detected. Rebuilding...')
            self.pg.execute()

    def _execute(self, pg):
        self.pg = pg
        if self.observer.is_alive():
            logging.info('Watch already active.')
            return

        logging.info('Starting watch of %s...', self.location)
        self.observer.start()
#        try:
#            while True:
#                time.sleep(0.1)
#        except KeyboardInterrupt:
#            self.observer.stop()
#        self.observer.join()
#        logging.info('Done watching.')
