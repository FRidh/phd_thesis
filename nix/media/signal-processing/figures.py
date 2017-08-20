# Convolution
import argparse
import numpy as np
import os
#import seaborn as sns

#sns.set_context("paper", font_scale=4./3.)

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 2.5))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)
mpl.rc('axes', grid=True)
mpl.rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'],
                                'monospace': ['Computer Modern Typewriter']})
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    x = np.ones(8)
    h = np.ones(3)*0.5
    y = np.convolve(x, h, mode='full')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(y, marker='o', label='y')
    ax.plot(x, marker='D', label='x')
    ax.plot(h, marker='s', label='h')
    ax.set_ylim(0, 2)
    ax.legend()
    ax.set_xlabel("Sample")
    ax.set_ylabel("Value")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    #fig.subplots_adjust(bottom=0.2, left=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(args.target, "convolution.eps"))

if __name__ == '__main__':
    main()
