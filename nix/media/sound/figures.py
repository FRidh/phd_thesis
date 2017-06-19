# Attenuation coefficient
import argparse
import numpy as np
import os
import seaborn as sns

sns.set_context("paper", font_scale=4./3.)

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 3.0))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)

from acoustics.atmosphere import Atmosphere


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    a = Atmosphere()
    f = np.logspace(1.0, 4.0, 100)
    fig = a.plot_attenuation_coefficient(f)
    #fig.subplots_adjust(bottom=0.2, left=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(args.target, "attenuation.eps"))


if __name__ == '__main__':
    main()



