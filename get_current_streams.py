import base64
import os
from pprint import pprint

import requests

USER_ID = os.environ['TWITCH_USER_ID']
TWITCH_EXTENSION_ID = os.environ['TWITCH_EXTENSION_ID']
SECRET = base64.b64decode(os.environ['TWITCH_EXTENSION_SECRET'])

twitch = requests.Session()
twitch.headers.update({'Client-ID': TWITCH_EXTENSION_ID})


def main():
    r = twitch.get(
        f'https://api.twitch.tv/extensions/{TWITCH_EXTENSION_ID}/live_activated_channels'
    )
    r.raise_for_status()
    pprint(r.json())


if __name__ == '__main__':
    main()
