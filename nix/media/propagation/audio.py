"""
Write audio for propagation effects.
"""
import argparse
import os
from acoustics import Signal
from h5store import h5load

def create_audio(source, target):

    s, meta = h5load(source)
    s = Signal(s, meta['fs'])
    s.normalize().to_wav(target)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    for name in os.listdir(args.source):
        create_audio(os.path.join(args.source, name), os.path.join(args.target, "{}.wav".format(os.path.splitext(name)[0])))

if __name__ == '__main__':
    main()
