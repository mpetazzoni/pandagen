# Pandagen

import BaseHTTPServer
import logging
import SimpleHTTPServer
import threading
import time

from .. import pandagen


class Serve(pandagen.Plugin):
    """
    Serve the built site with SimpleHTTPServer (for development purposes).
    """

    def __init__(self, port=8000, target='build', wait=False):
        self.port = port
        self.target = target
        self.wait = wait
        self._httpd = None

    def _get_address(self):
        """Returns the listening address of the HTTP server, if running."""
        assert self._httpd is not None
        address = self._httpd.socket.getsockname()
        return 'http://{0}:{1}/'.format(*address)

    def _execute(self, pg):
        if self._httpd:
            logging.info('Already serving at %s', self._get_address())
            return

        t = threading.Thread(name='pandagen-httpd', target=self._serve)
        t.daemon = True
        t.start()

        if not self.wait:
            return

        try:
            while t.is_alive():
                time.sleep(0.5)
        except:
            if self._httpd:
                logging.debug('Requesting shutdown of HTTP server...')
                self._httpd.shutdown()
                t.join()

    class PathTranslatingHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        """
        A request handler for the SimpleHTTPServer that translates incoming
        requests to include the serving path into the mapped local file path.
        For example, /index.html will read and return
        <pandagen_target>/index.html.

        <pandagen_target> is set from the serve target passed to the
        constructor of the Serve plugin.
        """

        def translate_path(self, path):
            path = '/{0}{1}'.format(self.server.pandagen_target, path)
            return (SimpleHTTPServer.SimpleHTTPRequestHandler
                    .translate_path(self, path))

    def _serve(self):
        try:
            self._httpd = BaseHTTPServer.HTTPServer(
                ('', self.port), Serve.PathTranslatingHandler)
            self._httpd.pandagen_target = self.target
            logging.info('Serving %s at %s', self.target, self._get_address())
            self._httpd.serve_forever()
        finally:
            self._httpd = None
            logging.info('Done serving.')
