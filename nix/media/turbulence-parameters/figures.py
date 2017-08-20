"""
Plot
"""

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

EXTENSION = "eps"
#EXTENSION = "png"

#XLIM = (10.0, 38.0)
YLIM = (0.0, 6000.0)
CLIM = (-20, +25)


def create_figure(source, target):
    s, meta = h5load(source)
    s = Signal(s, meta['fs'])
    ax = s.plot_spectrogram(ylim=YLIM, clim=CLIM, title='')
    fig = ax.get_figure()
    #fig.subplots_adjust(bottom=0.2, left=0.2)
    fig.tight_layout()
    fig.savefig(target, dpi=600)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()


    for filename in filter(lambda x: x.endswith('.hdf5'), os.listdir(args.source)):
        basename = os.path.splitext(filename)[0]
        create_figure(os.path.join(args.source, filename), os.path.join(args.target, "{}.{}".format(basename, EXTENSION)))

if __name__ == '__main__':
    main()
