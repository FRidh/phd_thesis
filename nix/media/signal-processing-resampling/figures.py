# Plotting
import matplotlib.pyplot as plt
#import seaborn as sns
import argparse
import os
from acoustics import Signal
from h5store import h5load

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 2.5))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)
mpl.rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'],
                                'monospace': ['Computer Modern Typewriter']})

EXTENSION = "eps"
#EXTENSION = "png"

def create_spectrogram(signal, target, plotargs=None):
    if plotargs is None:
        plotargs = {}
    ax = signal.plot_spectrogram(**plotargs)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(target, dpi=600)


def load_signal(path):
    """Load signal.

    :returns: `(signal, method, kernelsize, basename)`

    """
    s, meta = h5load(path)
    s = Signal(s, meta['fs'])
    s.method = meta['method']
    s.kernelsize = meta['kernelsize']
    s.basename = os.path.splitext(os.path.basename(path))[0]
    return s


def create_label(method, kernelsize):
    label = method.capitalize()
    if kernelsize is not None:
        label = r"{}, $a={}$".format(label, kernelsize)
    return label


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    filenames = os.listdir(args.source)
    paths = (os.path.join(args.source, filename) for filename in filenames)
    signals = list(map(load_signal, paths))

    # Create spectrograms
    plotargs = {
        'clim':     (-40,+40),
        'title':    '',
        }

    # Create spectrograms
    for signal in signals:
        create_spectrogram(signal, os.path.join(args.target, "{}.{}".format(signal.basename, EXTENSION)), plotargs)

    # Time-level
    s = Signal(signals, signals[0].fs)
    name = os.path.join(args.target, "levels.{}".format(EXTENSION))
    ax = s.plot_levels()
    ax.legend(labels=[create_label(signal.method, signal.kernelsize) for signal in signals])
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(name, dpi=600)

if __name__ == '__main__':
    main()
