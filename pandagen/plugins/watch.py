# Pandagen

import fnmatch
import logging
import os.path
import time
import watchdog.events
import watchdog.observers

from .. import pandagen


class Watch(pandagen.Plugin, watchdog.events.FileSystemEventHandler):
    """
    Watch for files changes and re-execute the pipeline if a change is
    detected. A list of excluded glob patterns can be specified via the exclude
    paramater to the constructor. Make sure you exclude your build directory
    (and anything underneath it); if you use Jinja2 templates, also exclude
    anything under the .cache folder.
    """

    def __init__(self, location='.',
                 exclude=['.', '.cache/*', 'build', 'build/*', '*.swp']):
        self.location = location
        self.exclude = [os.path.normpath(p) for p in exclude]
        self.observer = self._get_observer()
        self.pg = None

    def _get_observer(self):
        observer = watchdog.observers.Observer()
        observer.schedule(self, self.location, recursive=True)
        return observer

    def on_any_event(self, event):
        assert self.pg is not None

        for t in [watchdog.events.DirCreatedEvent,
                  watchdog.events.DirModifiedEvent]:
            if isinstance(event, t):
                return

        for exclude in self.exclude:
            if fnmatch.fnmatch(os.path.normpath(event.src_path), exclude):
                return

        logging.info('Change detected in %s. Rebuilding...', event.src_path)
        self.pg.execute()

    def _execute(self, pg):
        self.pg = pg
        if self.observer.is_alive():
            logging.info('Watch already active.')
            return

        logging.info('Starting watch of %s (excluding %s)...',
                     self.location, ', '.join(self.exclude))
        self.observer.start()
        try:
            while self.observer.should_keep_running():
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        logging.info('Done watching.')
