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

    # We begin by turning everything off
    settings['spreading']['include'] = False
    settings['doppler']['include'] = False
    settings['atmospheric_absorption']['include'] = False
    settings['reflections']['include'] = False
    settings['turbulence']['include'] = False

    target = lambda name: os.path.join(args.target, "{}.hdf5".format(name))

    # Emission only
    simulate(settings, target('emission'))

    # Spreading magnitude
    settings['spreading']['include'] = True
    simulate(settings, target('spreading'))

    # Spreading magnitude + phase/delay resulting in Doppler shift
    settings['doppler']['include'] = True
    simulate(settings, target('doppler'))

    # Atmospheric attenuation
    settings['atmospheric_absorption']['include'] = True
    simulate(settings, target('attenuation'))

    # Ground reflection
    settings['reflections']['include'] = True
    simulate(settings, target('reflection'))

    # Turbulence
    #settings['turbulence']['include'] = True
    #simulate(settings, target('turbulence'))



if __name__ == '__main__':
    main()
