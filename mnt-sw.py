#!/usr/bin/env python3
from sys import argv
import subprocess
from pathlib import Path

home = Path.home()

def main():
    if len(argv) == 3:
        if argv[-2] == '-r':
            raw_mode = True
        else:
            raw_mode = False
        source_file_path = argv[-1]
    elif len(argv) == 2:
        source_file_path = argv[-1]
        raw_mode = False
    else:
        print('Invalid arguments')

    mount_path = Path("{}/mnt/{}".format(home,source_file_path))

    tkeystr = None
    for titlekeypath in Path(source_file_path).parent.glob('*.titlekey'):
        with open(titlekeypath, 'rb') as titlekeyfile:
            tkeystr = titlekeyfile.read(16).hex()

    cmd = []
    cmd.append('fuse-nx')
    if tkeystr != None:
        cmd.append('--titlekey={}'.format(tkeystr))
    cmd += ['mount',source_file_path,mount_path]
    if raw_mode == True:
        cmd.append('r')
    cmd += ['-o','allow_root']

    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    print(subprocess.list2cmdline(cmd))

    try:
        proc.communicate()
    except KeyboardInterrupt:
        print(f"Terminating process {proc.pid}")
        proc.terminate()

    while True:
        try:
            mount_path.rmdir()
        except OSError as e:
            if e.args[0] != 16: # Errno 16: Device or resource busy -> FUSE hasn't unmounted yet
                break
if __name__ == '__main__':
    main()
