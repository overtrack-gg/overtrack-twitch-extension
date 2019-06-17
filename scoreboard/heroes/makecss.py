import glob


def main():
    for p in glob.glob('*.png'):
        team, hero = p.split('.')[0].split('_')
        print('.team-%s > .player > .hero-%s {\n\tbackground-image: url("./heroes/%s_%s.png");\n}' % (team, hero, team, hero))


if __name__ == '__main__':
    main()
