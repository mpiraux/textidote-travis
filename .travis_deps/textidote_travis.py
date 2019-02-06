#!/usr/bin/env python3
import configparser
import subprocess
import os.path
import sys


def run(cmd):
    p = subprocess.run(cmd, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return p.returncode, p.stderr


config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = lambda option: option
config.read(sys.argv[1])

textidote_cmd = 'textidote {opts} {input_files} > {output}'
output_files = []
error_occured = False

for s in config.sections():
    opts = {}
    file_types = {}
    for k, v in config[s].items():
        if v is not None:
            opts[k] = v
        else:
            _, ext = os.path.splitext(k)
            if ext != '.tex':
                ext = '.md'
            l = file_types.get(ext, [])
            l.append(k)
            file_types[ext] = l

    for t, files in file_types.items():
        output_file = '{}{}.txt'.format(s, t)
        output_files.append(output_file)
        cmd = textidote_cmd.format(opts=' '.join('{} {}'.format(k, v) for k, v in opts.items()), input_files=' '.join(files), output=output_file)
        print(cmd)
        e, stderr = run(cmd)
        print(stderr)
        error_occured = e != 0 if not error_occured else error_occured

for filename in output_files:
    print('=' * 10, filename, '=' * 10)
    with open(filename) as f:
        print(f.read())

exit(error_occured)
