import argparse
import os
import numpy as np
from h5store import h5save
from auraliser.propagation import apply_doppler#, interpolation_linear, interpolation_lanczos
import pandas as pd

#import matplotlib as mpl
#mpl.rc("figure", figsize=(6.0, 10.0))
#mpl.rc("font", size=10)
##mpl.rc('text', usetex=True)


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
        ('lanczos', 5),
        ('lanczos', 10)
    ]

    signals = [ apply_doppler(signal, delay, fs, method, kernelsize) for method, kernelsize in jobs ]

    for method, kernelsize, signal in zip(*(zip(*jobs)), signals):
        name = os.path.join(folder, '{}-{}.hdf5'.format(method, kernelsize))
        h5save(name, pd.Series(signal), {'fs':fs})

    #fig, axes = plt.subplots(4, 1)

    #for ax, signal, label in zip(axes.flat, signals.values(), signals.keys()):
        #signal.plot_spectrogram(ax=ax)


    ##for ax, s, label in zip(axes.flat, signals, labels):
        ##_, _, _, im = ax.specgram(s, Fs=s.fs, label=label, mode='psd', scale_by_freq=True, noverlap=128, NFFT=4096)
        ##ax.set_ylim(0.0, signal.fs/2.0)
        ##im.set_clim(clim)
        ##ax.set_title(label)
        ##ax.set_xlabel('$t$ in s')
        ##ax.set_ylabel('$f$ in Hz')

    #cb = fig.colorbar(im, ax=axes.ravel().tolist())

    #fig.savefig()




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    compute(args.target)


if __name__ == '__main__':
    main()
