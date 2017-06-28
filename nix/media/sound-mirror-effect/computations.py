"""
Demonstrate the propagation effects.
Outputs a hdf5 file per event.
"""
import argparse
import os
from common_simulation import simulate
from auraliser import get_default_settings

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    settings = get_default_settings()

    # We only want to have the ground reflection.
    # But, in order to compute the reflection we also need a
    # propagation delay!
    settings['spreading']['include'] = False
    settings['doppler']['include'] = True
    settings['atmospheric_absorption']['include'] = False
    settings['reflections']['include'] = True
    settings['turbulence']['include'] = False

    target = lambda name: os.path.join(args.target, "{}.hdf5".format(name))

    # Ground reflection, hard.
    settings['reflections']['force_hard'] = True
    simulate(settings, target('hard'))

    # Ground reflection, soft.
    settings['reflections']['force_hard'] = False
    simulate(settings, target('soft'))


if __name__ == '__main__':
    main()
