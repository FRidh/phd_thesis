"""
Plot propagation effects
"""

# Plotting
import matplotlib.pyplot as plt
#import seaborn as sns
import argparse
import os
from acoustics import Signal
from h5store import h5load

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 3.0))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)

#EXTENSION = "eps"
EXTENSION = "png"

XLIM = (10.0, 38.0)
YLIM = (0.0, 4000.0)
CLIM = (-50.0, +50.0)


def create_figure(source, target, plotargs=None):
    if plotargs is None:
        plotargs = {}
    s, meta = h5load(source)
    s = Signal(s, meta['fs'])
    fig = s.plot_spectrogram(clim=CLIM, xlim=XLIM, ylim=YLIM, title='', **plotargs)
    #fig.subplots_adjust(bottom=0.2, left=0.2)
    fig.tight_layout()
    fig.savefig(target, dpi=600)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    for filename in os.listdir(args.source):
        basename = os.path.splitext(filename)[0]
        create_figure(os.path.join(args.source, filename), os.path.join(args.target, "{}.{}".format(basename, EXTENSION)))

if __name__ == '__main__':
    main()
