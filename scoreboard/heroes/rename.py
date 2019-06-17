import glob
import shutil
import os


def main():
    for p in glob.glob('*/*.png'):
        if 'blue' in p:
            back = -25
        else:
            back = -24
        t, h = p.split(os.path.sep)
        h = h[len('heroes'):]
        print(t, h)
        shutil.move(p, t + '_' + h)


if __name__ == '__main__':
    main()
