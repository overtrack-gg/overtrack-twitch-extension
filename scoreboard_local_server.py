import json
import mimetypes
import os
from typing import Any, Dict, List, Optional

import typedload
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from threading import Thread

from overtrack.overwatch.collect import Game


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
                with open(path, 'r') as f:
                    return Response(f.read(), content_type=mimetypes.guess_type(path)[0])
        elif request.path == '/scoreboard.json':
            data: Dict[str, Optional[Dict[str, List[Dict[str, Any]]]]]
            if self.game:
                data = {
                    'teams': {
                        'blue': [typedload.dump(p.stats) for p in self.game.teams.blue],
                        'red': [typedload.dump(p.stats) for p in self.game.teams.red],
                    }
                }
            else:
                data = {
                    'teams': None
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
        self.thread.start()
        self.game: Game = None

    def update(self, game: Game):
        self.game: Game = game

    def clear(self):
        self.game: Game = None
