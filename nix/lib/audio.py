"""
Write .wav files.
The first argument to this script is a `source` directory, and
the second argument a `target` directory. Each file in it is converted
to `.wav`.

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

    for filename in filter(lambda x: x.endswith('.hdf5'), os.listdir(args.source)):
        create_audio(os.path.join(args.source, filename), os.path.join(args.target, "{}.wav".format(os.path.splitext(filename)[0])))

if __name__ == '__main__':
    main()
