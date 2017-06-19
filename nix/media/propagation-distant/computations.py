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
from auraliser.generator import Sine, Noise, NoiseBands
from geometry import Point
from streaming import Stream
from streaming.signal import constant
from ism import Wall
from h5store import h5save
import pandas as pd
from acoustics.reflection import impedance_attenborough
from acoustics.signal import OctaveBand

def simulate(settings, name):
    """Make simulation with parameters.

    """
    # Generic
    fs = 44100.0      # Sample frequency
    duration = 40.      # Duration in seconds
    df = 50.0           # Frequency resolution (impedances reflections)
    nsamples = int(fs*duration)
    dt = 1.0/fs                             # Seconds per sample
    t = np.arange(0.0, duration, dt)        # Time vector

    # Model
    model = Auraliser(duration=duration, settings=settings)
    model.settings['fs'] = fs

    # Source
    frequency = 2000.0
    speed = 150.0
    x = np.ones_like(t) * speed * (t - duration/2.0)    # Source moves along the x-axis.
    y = np.ones_like(t) * 3.0
    z = np.ones_like(t) * 1000.0   # Altitude of source
    src = model.add_source(name='source', position=np.vstack((x,y,z)).T)
    #src = model.add_source(name='source', position=Point(0.0,0.0,0.0))
    subsrc = src.add_subsource(name='subsource')

    harmonics = 5
    for i in range(1, harmonics+1):
        subsrc.add_virtualsource('sine_{}'.format(i), signal = Sine(frequency=(frequency*i)))
    #noise = subsrc.add_virtualsource('noise', signal = Noise(color='pink'), level=140.)

    # 16 to 16000 Hz
    octaves = OctaveBand(fstart=15., fstop=10000)
    # [ 16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000., 16000.0 ]
    levels = np.array([105, 110, 115, 110, 110, 110, 105, 100, 95, 90])[:,None]

    noise = subsrc.add_virtualsource('noise',
                                     signal = NoiseBands(
                                         bands=octaves,
                                         gains=levels,
                                         color='pink'), level=120.)

    # Receiver
    rcv = model.add_receiver(name='receiver', position=Point(0.0,-1000,1.8))

    frequencies = np.arange(0.1, fs/2.0, df)
    flow_resistivity = 2e5
    impedance = np.nan_to_num(impedance_attenborough(frequencies, flow_resistivity))

    dx = 10000.0
    groundcorners1 = [Point(-dx, -dx, 0.0),
                      Point(+dx, -dx, 0.0),
                      Point(+dx, +dx, 0.0),
                      Point(-dx, +dx, 0.0)]
    ground1 = Wall(groundcorners1, Point(0.0, 0.0, 0.0), impedance)

    model.geometry.walls = [ground1]

    signal = pd.Series(mono( rcv.auralise() ).toarray())

    h5save(name, signal, {'fs': fs})


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    target = lambda name: os.path.join(args.target, "{}.hdf5".format(name))

    settings = get_default_settings()

    settings['turbulence']['include'] = False
    simulate(settings, target('without'))

    settings['turbulence']['include'] = True
    simulate(settings, target('with'))

    ## We begin by turning everything off
    #settings['spreading']['include'] = False
    #settings['doppler']['include'] = False
    #settings['atmospheric_absorption']['include'] = False
    #settings['reflections']['include'] = False
    #settings['turbulence']['include'] = False



    ## Emission only
    #simulate(settings, target('emission'))

    ## Spreading magnitude
    #settings['spreading']['include'] = True
    #simulate(settings, target('spreading'))

    ## Spreading magnitude + phase/delay resulting in Doppler shift
    #settings['doppler']['include'] = True
    #simulate(settings, target('doppler'))

    ## Atmospheric attenuation
    #settings['atmospheric_absorption']['include'] = True
    #simulate(settings, target('attenuation'))

    ## Ground reflection
    #settings['reflections']['include'] = True
    #simulate(settings, target('reflection'))

    ## Turbulence
    ##settings['turbulence']['include'] = True
    ##simulate(settings, target('turbulence'))



if __name__ == '__main__':
    main()
