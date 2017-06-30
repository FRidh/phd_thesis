import argparse
import os
import numpy as np
import pandas as pd
from h5store import h5save
from auraliser.propagation import apply_doppler


def compute(folder):

    # Signal properties
    duration = 10.0
    fs = 44100.0
    frequency = 5000.0
    nsamples = int(fs*duration)
    times = np.arange(nsamples) / fs

    # Emission signal
    signal = np.sin(2.0*np.pi*frequency*times)

    # Source velocity
    velocity = 70.0

    # Soundspeed
    soundspeed = 343.0

    # Geometry
    x = times * velocity
    x -= x.max()/2.0
    y = np.zeros(nsamples)
    z = 100.0 * np.ones(nsamples)

    # Positions of source and receiver
    position_source = np.vstack((x,y,z)).T
    position_receiver = np.zeros(3)

    distance = np.linalg.norm((position_source - position_receiver), axis=-1)
    delay = distance / soundspeed

    jobs = [
        ('linear', None),
        ('lanczos', 2),
        #('lanczos', 5),
        ('lanczos', 10)
    ]

    signals = [ apply_doppler(signal, delay, fs, method, kernelsize) for method, kernelsize in jobs ]

    for method, kernelsize, signal in zip(*(zip(*jobs)), signals):
        if kernelsize is None:
            basename = method
        else:
            basename = '{}-{}'.format(method, kernelsize)
        name = os.path.join(folder, '{}.hdf5'.format(basename))
        h5save(name, pd.Series(signal), {'fs':fs, 'method': method, 'kernelsize': kernelsize})


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    compute(args.target)


if __name__ == '__main__':
    main()
