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
mpl.rc("figure", figsize=(2.9, 2.5))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)


def create_figure(source, target, clim):
    s, meta = h5load(source)
    s = Signal(s, meta['fs'])
    fig = s.plot_spectrogram(clim=clim, ylim=(0.0, 4000.0))
    fig.subplots_adjust(bottom=0.2, left=0.2)
    fig.savefig(target, dpi=600)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    clims = {
        'emission' :        (+20.0, +70.0),
        'spreading':        (-10.0, +40.0),
        'doppler' :         (-10.0, +40.0),
        'attenuation':      (-10.0, +40.0),
        'reflection':       (-10.0, +40.0),
        'turbulence':       (-10.0, +40.0)
    }

    for filename in os.listdir(args.source):
        basename = os.path.splitext(filename)[0]
        clim = clims[basename]
        create_figure(os.path.join(args.source, filename), os.path.join(args.target, "{}.eps".format(basename)), clim)

if __name__ == '__main__':
    main()
