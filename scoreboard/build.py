import sys
import zipfile
import glob
import os
import shutil

if __name__ == '__main__':
    if os.path.exists('./build'):
        for p in os.listdir('./build'):
            pp = './build/' + p
            if os.path.isdir(pp):
                shutil.rmtree(pp)
            else:
                os.remove(pp)
    os.makedirs('./build', exist_ok=True)

    for css in glob.glob('*.css'):
        print(f'Copying {css}')
        shutil.copy(css, os.path.join('./build', os.path.basename(css)))

    print('Copying ./fonts')
    shutil.copytree('./fonts', './build/fonts')

    shutil.copytree('./images', './build/images')

    for ext in '*.js', '*.html':
        for p in glob.glob(ext):
            print(f'Processing and copying {p}')
            enabled = True
            lines_skipped = 0
            with open(p, 'r') as inf, open(os.path.join('./build', os.path.basename(p)), 'w') as outf:
                for line in inf.readlines():
                    if '<!-- BEGIN: !twitch -->' in line or '/* BEGIN: !twitch */' in line:
                        enabled = False
                    if enabled:
                        if 'console.' in line:
                            sys.stdout.flush()
                            sys.stderr.flush()
                            sys.stderr.write(f'ERROR: Found illegal line "{line.strip()}" in {p}')
                            sys.exit(-1)
                        outf.write(line)
                    else:
                        lines_skipped += 1
                    if '<!-- END: !twitch -->' in line or '/* END: !twitch */' in line:
                        enabled = True
            print(f'\tRemoved {lines_skipped} lines')

    print('Zipping to build.zip')
    os.chdir('./build')
    files = os.walk('.')
    zf = zipfile.ZipFile('./build.zip', 'w')
    for dirname, subdirs, files in files:
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    os.chdir('..')


