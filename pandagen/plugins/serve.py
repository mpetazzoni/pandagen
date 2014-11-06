# Pandagen

import BaseHTTPServer
import logging
import os
import SimpleHTTPServer
import threading
import time

from .. import pandagen


class Serve(pandagen.Plugin):
    """
    Serve the built site with SimpleHTTPServer (for development purposes).
    """

    def __init__(self, port=8000, target='build'):
        self.port = port
        self.target = target
        self._httpd = None

    def _execute(self, pg):
        t = threading.Thread(name='pandagen-httpd', target=self._serve)
        t.start()
        try:
            while t.is_alive():
                time.sleep(0.5)
        except:
            if self._httpd:
                logging.debug('Requesting shutdown of HTTP server...')
                self._httpd.shutdown()
                t.join()


    def _serve(self):
        current = os.getcwd()
        os.chdir(self.target)
        try:
            self._httpd = BaseHTTPServer.HTTPServer(
                ('', self.port), SimpleHTTPServer.SimpleHTTPRequestHandler)
            address = self._httpd.socket.getsockname()
            logging.info('Serving at http://%s:%d/', *address)
            self._httpd.serve_forever()
        finally:
            os.chdir(current)
            self._httpd = None
            logging.info('Done serving.')
