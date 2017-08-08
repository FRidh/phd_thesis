# Attenuation coefficient
import argparse
import numpy as np
import os
import seaborn as sns
sns.set_context("paper")#, font_scale=4./3.)

import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 2.5))
mpl.rc("font", size=10)
mpl.rc('text', usetex=True)
import matplotlib.pyplot as plt

from acoustics.atmosphere import Atmosphere
from acoustics.reflection import impedance_delany_and_bazley, reflection_factor_plane_wave

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    # Frequency vector
    f = np.logspace(1.0, 4.0, 100)
    # Flow resistivity for grass
    res = 200000.
    # Angle of incidence vector
    angles = np.linspace(0.0, 90.0, 100)

    # Impedance Delany and Bazely
    #imp = impedance_delany_and_bazley(f, res)
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.semilogx(f, imp.real, label="Real")
    #ax.semilogx(f, imp.imag, label="Imaginery{}", linestyle='-.')
    #ax.legend()
    #ax.set_xlabel(r'$f$ in Hz')
    #ax.set_ylabel(r'$Z$ in -')
    #fig.tight_layout()
    #fig.savefig(os.path.join(args.target, "impedance.eps"))

    # Reflection
    #r = reflection_factor_plane_wave(imp, (angles/180.*np.pi)[...,None])

    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #im = ax.pcolormesh(f, angles, np.abs(r))
    #ax.set_xlabel(r'$f$ in Hz')
    #ax.set_ylabel(r'$\theta$ in \textdegree')
    #cb = ax.get_figure().colorbar(mappable=im)
    #cb.set_label(r'$|R|$ in -')
    #fig.tight_layout()
    #fig.savefig(os.path.join(args.target, "reflection-abs.eps"))

    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #im = ax.pcolormesh(f, angles, np.angle(r)*180/np.pi)
    #ax.set_xlabel(r'$f$ in Hz')
    #ax.set_ylabel(r'$\theta$ in \textdegree')
    #cb = ax.get_figure().colorbar(mappable=im)
    #cb.set_label(r'$\angle R$ in \textdegree')
    #fig.tight_layout()
    #fig.savefig(os.path.join(args.target, "reflection-angle.eps"))


    # Atmospheric attenuation
    a = Atmosphere()
    fig = a.plot_attenuation_coefficient(f)
    fig.tight_layout()
    fig.savefig(os.path.join(args.target, "attenuation.eps"))


if __name__ == '__main__':
    main()



