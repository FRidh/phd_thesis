"""
Demonstrate the propagation effects.
Outputs a hdf5 file per event.
"""
import argparse
import os

# Model
import numpy as np
from acoustics import Signal
from auraliser import Auraliser, mono, get_default_settings
from auraliser.generator import Sine, Noise
from geometry import Point
from streaming import Stream
from streaming.signal import constant
from ism import Wall
from h5store import h5save
import pandas as pd

def simulate(settings, name):
    """Make simulation with parameters.

    """
    # Generic
    fs = 44100.0      # Sample frequency
    duration = 20.      # Duration in seconds
    df = 50.0           # Frequency resolution (impedances reflections)
    nsamples = int(fs*duration)
    dt = 1.0/fs                             # Seconds per sample
    t = np.arange(0.0, duration, dt)        # Time vector

    # Model
    model = Auraliser(duration=duration, settings=settings)
    model.settings['fs'] = fs

    # Source
    frequency = 2000.0
    speed = 100.0
    x = np.ones_like(t) * speed * (t - duration/2.0)    # Source moves along the x-axis.
    y = np.ones_like(t) * 0.01
    z = np.ones_like(t) * 200.0   # Altitude of source
    src = model.add_source(name='source', position=np.vstack((x,y,z)).T)
    #src = model.add_source(name='source', position=Point(0.0,0.0,0.0))
    subsrc = src.add_subsource(name='subsource')

    harmonics = 5
    for i in range(1, harmonics+1):
        subsrc.add_virtualsource('sine_{}'.format(i), signal = Sine(frequency=(frequency*i)))
    noise = subsrc.add_virtualsource('noise', signal = Noise(color='brown'), level=140.)

    # Receiver
    rcv = model.add_receiver(name='receiver', position=Point(0.0,0.0,4.0))




    frequencies = np.arange(0.0, fs/2.0, df)
    impedance = np.ones_like(frequencies) + 1j*np.ones_like(frequencies)

    groundcorners1 = [Point(-100.0, -100.0, 0.0),
                    Point(100.0, -100.0, 0.0),
                    Point(100.0, 100.0, 0.0),
                    Point(-100.0, 100.0, 0.0) ]
    ground1 = Wall(groundcorners1, Point(0.0, 0.0, 0.0), impedance)

    model.geometry.walls = [ground1]

    signal = pd.Series(mono( rcv.auralise() ).toarray())

    h5save(name, signal, {'fs': fs})


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
    settings['turbulence']['include'] = True
    #simulate(settings, target('turbulence'))



if __name__ == '__main__':
    main()
