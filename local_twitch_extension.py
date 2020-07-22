import base64
import json
import logging
import mimetypes
import os
import sys
from threading import Thread
from typing import Dict

import jwt
import requests
import time
from werkzeug.serving import make_ssl_devcert, run_simple
from werkzeug.wrappers import Request, Response

from dev_hero_selector import ScoreboardGui

PORT = 8080
TWITCH_ENDPOINT_OAUTH = 'https://id.twitch.tv/oauth2/token'


class ScoreboardTwitchExtensionServer:

    @Request.application
    def application(self, request: Request):
        path = request.path
        if request.path == '/':
            path = '/video_component.html'
        path = os.path.join(os.path.dirname(__file__), 'scoreboard', os.path.normpath(path)[1:])

        if os.path.exists(path):
            with open(path, 'rb') as f:
                return Response(f.read(), content_type=mimetypes.guess_type(path)[0])
        else:
            return Response(status=404)

    def __init__(self):
        self.thread = Thread(target=run_simple, args=('localhost', PORT, self.application), kwargs={'ssl_context': ('./key.crt', './key.key')}, daemon=True)
        self.thread.start()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    if not os.path.exists('./key.pem') or not os.path.exists('./key.crt'):
        logging.info('Creating dev cert')
        make_ssl_devcert('./key', host='localhost')

    server = ScoreboardTwitchExtensionServer()
    time.sleep(1)

    print(f'Please visit https://localhost:{PORT} in your browser and ensure that the page is loading and not presenting a SSL error')
    print('In chrome you can set the flag chrome://flags#allow-insecure-localhost, '
          'for other browsers you may need to install the generated "key.crt" as a trusted root cert, '
          'or launch the browser with a special argument.')
    print('Once you have confirmed this page loads with no error (the page should appear empty with no content), '
          'you should also be able to load it on twitch as a locally-hosted extension (see the readme for more info on setting this up).')
    print()

    if '--live' not in sys.argv:
        if len(sys.argv) != 5:
            print('-' * 32)
            print('You need to provide your twitch API client ID if not running in "live data" mode. '
                  'You can find this on the first page when you create a new extension, '
                  'or regenerate it under "Extension Authorization Settings" on your extension\'s Developer Console')
            exit(0)

        client_id, client_secret, extension_secret_encoded, channel = sys.argv[1:]
        extension_secret = base64.b64decode(extension_secret_encoded)

        token_r = requests.post(
            TWITCH_ENDPOINT_OAUTH,
            params=dict(
                client_id=client_id,
                client_secret=client_secret,
                grant_type='client_credentials',
            )
        )
        token_r.raise_for_status()
        twitch = requests.session()
        twitch.headers.update({
            'Authorization': f'Bearer {token_r.json()["access_token"]}',
            'Client-ID': client_id,
        })

        r = twitch.get('https://api.twitch.tv/helix/users?login=' + channel)
        r.raise_for_status()
        user_id = r.json()['data'][0]['id']

        gui = ScoreboardGui.create()

        def update_extension(data: Dict):
            message = {
                'timestamp': time.time(),
                'teams': data['teams']
            }
            auth = {
                'user_id': str(user_id),
                'exp': int(time.time() + 60),
                'role': 'external',
                'channel_id': str(user_id),
                'pubsub_perms': {
                    'send': [
                        'broadcast'
                    ]
                }
            }
            logging.info(f'Sending twitch broadcast: {message}')
            r = twitch.post(
                f'https://api.twitch.tv/extensions/message/{user_id}',
                json={
                    'content_type': 'application/json',
                    'message': json.dumps(message),
                    'targets': ['broadcast']
                },
                headers={
                    'Authorization': 'Bearer ' + jwt.encode(auth, extension_secret).decode()
                }
            )
            try:
                r.raise_for_status()
            except Exception as e:
                logging.exception(f'Failed to publish update: {r.text}', exc_info=e)
            else:
                logging.debug(f' > {r.status_code}')

        def update_loop():
            while True:
                update_extension(gui.data)
                time.sleep(10)

        Thread(target=update_loop, daemon=True).start()

        last_update = None
        def rate_limited_update(data):
            nonlocal last_update
            if not last_update or time.time() - last_update > 1:
                last_update = time.time()
                update_extension(data)

        gui.callback = rate_limited_update

        gui.run()

    else:
        logging.info(f'Running without player selector GUI - you must provide live data from OverTrack')
        server.thread.join()

    logging.info(f'Shutting down')


if __name__ == '__main__':
    try:
        from overtrack.util.logging_config import config_logger
        config_logger(os.path.basename(__file__).split('.')[0], logging.DEBUG)
    except:
        pass
    main()
