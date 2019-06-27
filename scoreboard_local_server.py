import json
import mimetypes
import os

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from threading import Thread

from dev_hero_selector import ScoreboardGui


class ScoreboardHTTPServer:

    @Request.application
    def application(self, request: Request):
        path = request.path
        if request.path == '/':
            path = '/video_component.html'
        path = os.path.join(os.path.dirname(__file__), 'scoreboard', os.path.normpath(path)[1:])

        if os.path.exists(path):
            if 'html' in path or 'js' in path:
                lines = []
                enabled = True
                with open(path, 'r') as f:
                    for line in f.readlines():
                        if '<!-- BEGIN: twitch -->' in line:
                            enabled = False
                        if enabled:
                            lines.append(line)
                        if '<!-- END: twitch -->' in line:
                            enabled = True
                return Response(''.join(lines), content_type=mimetypes.guess_type(path)[0])
            else:
                with open(path, 'rb') as f:
                    return Response(f.read(), content_type=mimetypes.guess_type(path)[0])
        elif request.path == '/scoreboard.json':
            data = self.gui.data
            return Response(
                json.dumps(data),
                content_type='application/json',
                headers={
                    'Access-Control-Allow-Origin': '*'
                }
            )
        else:
            return Response(status=404)

    def __init__(self, address='localhost', port=8000):
        self.thread = Thread(target=run_simple, args=(address, port, self.application), daemon=True)
        self.thread.start()

        self.gui = ScoreboardGui.create()
        self.gui.run()


if __name__ == '__main__':
    ScoreboardHTTPServer()
