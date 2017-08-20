"""
Plot
"""

# Plotting
import matplotlib.pyplot as plt
#import seaborn as sns
import argparse
import os
from acoustics import Signal
import pandas as pd

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 2.5))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)
mpl.rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'],
                                'monospace': ['Computer Modern Typewriter']})

EXTENSION = "eps"
#EXTENSION = "png"

#XLIM = (10.0, 38.0)
YLIM = (0.0, 8000.0)

CLIM = (-30, +40)

def plot(signals):

     # Create figure consisting of 3 spectrograms
    aircraft = signals.iloc[0].aircraft
    kind = signals.iloc[0].kind

    fig = plt.figure()
    ax = fig.add_subplot(131)
    signals[signals.part=='start'].iloc[0].signal.plot_spectrogram(ax=ax, title='', ylim=YLIM, clim=CLIM)

    ax = fig.add_subplot(132)
    signals[signals.part=='center'].iloc[0].signal.plot_spectrogram(ax=ax, title='', ylim=YLIM, clim=CLIM)
    ax.set_yticklabels([])
    ax.set_ylabel('')

    ax = fig.add_subplot(133)
    signals[signals.part=='end'].iloc[0].signal.plot_spectrogram(ax=ax, title='', ylim=YLIM, clim=CLIM)
    ax.set_yticklabels([])
    ax.set_ylabel('')

    # Delete colorbars
    fig.delaxes(fig.axes[3])
    fig.delaxes(fig.axes[1])

    fig.tight_layout()

    filename = os.path.join(args.target, "{}-{}.{}".format(kind, aircraft, EXTENSION))
    fig.savefig(filename, dpi=600)


def load_signal(filename):
    path = os.path.join(args.source, filename)
    signal = Signal.from_wav(path)
    _, event, _, kind, part = os.path.splitext(filename)[0].split('-')
    aircraft = event.split('_')[-1]
    return {'aircraft' : aircraft, 'kind' : kind, 'part' : part, 'signal' : signal }


def main():

    filenames = os.listdir(args.source)
    # List of tuples
    signals = pd.DataFrame(list(map(load_signal, filenames)))

    signals.groupby('kind').apply(plot)



if __name__ == '__main__':
    # Global
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()
    main()
