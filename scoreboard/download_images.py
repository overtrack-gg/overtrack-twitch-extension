import requests
import cv2
import numpy as np

def main():
    s = requests.Session()
    for hero, flip in [
        ('dva',             False),
        ('orisa',           False),
        ('reinhardt',       False),
        ('roadhog',         True),
        ('winston',         False),
        ('wrecking-ball',   False),
        ('zarya',           True),
        ('ashe',            True),
        ('bastion',         False),
        ('doomfist',        True),
        ('genji',           False),
        ('hanzo',           False),
        ('junkrat',         True),
        ('mccree',          False),
        ('mei',             False),
        ('pharah',          False),
        ('reaper',          False),
        ('soldier-76',      False),
        ('sombra',          False),
        ('symmetra',        False),
        ('torbjorn',        False),
        ('tracer',          False),
        ('widowmaker',      False),
        ('ana',             False),
        ('baptiste',        True),
        ('brigitte',        False),
        ('lucio',           False),
        ('mercy',           False),
        ('moira',           False),
        ('zenyatta',        False),
    ]:
        r = s.get(f'https://d1u1mce87gyfbn.cloudfront.net/hero/{hero}/icon-portrait.png')
        r.raise_for_status()
        image = cv2.imdecode(np.frombuffer(r.content, dtype=np.uint8), -1)
        if flip:
            image = image[:, ::-1]
        cv2.imwrite(f'./images/heroes/{hero}.png', image)


if __name__ == '__main__':
    main()