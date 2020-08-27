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
            path = '/overlay.html'
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
            data['postgame'] = {
                'role': 'tank',
                'result': 'win',
                'map': 'blizzard-world',
                'hero': 'zarya',
                'timestamp': 1591246479.8514,
                'description': '1 rounds',
                'duration': '11.0 min',
                'link': 'https://overtrack.gg/overwatch/games/synap53/2020-06-04-04-54-k4fJn7',
                'stats': [
                    {
                        'key': 'Eliminations',
                        'value': '17'
                    },
                    {
                        'key': 'Hero Damage Done',
                        'value': '6773'
                    },
                    {
                        'key': 'Objective Kills',
                        'value': '6'
                    },
                    {
                        'key': 'Healing Done',
                        'value': '0'
                    },
                    {
                        'key': 'Objective Time',
                        'value': '00:02:06'
                    },
                    {
                        'key': 'Deaths',
                        'value': '9'
                    }
                ]
            }
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
        self.gui = ScoreboardGui.create()
        self.thread.start()

        self.gui.run()


if __name__ == '__main__':
    ScoreboardHTTPServer()
