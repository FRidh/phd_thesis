import numpy as np
from acoustics import Signal
from auraliser import Auraliser, mono, get_default_settings
from auraliser.generator import Sine, Noise, NoiseBands
from geometry import Point
from ism import Wall
import pandas as pd
from h5store import h5save
from acoustics.reflection import impedance_delany_and_bazley
from acoustics.signal import OctaveBand

def simulate(settings, name, with_tones=True, with_noise=True):
    """Make simulation with parameters.

    """
    # Generic
    fs = 44100.0      # Sample frequency
    duration = 30.      # Duration in seconds
    df = 10.0           # Frequency resolution (impedances reflections)
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
    y = np.ones_like(t) * 3.0
    z = np.ones_like(t) * 200.0   # Altitude of source
    src = model.add_source(name='source', position=np.vstack((x,y,z)).T)
    #src = model.add_source(name='source', position=Point(0.0,0.0,0.0))
    subsrc = src.add_subsource(name='subsource')


    if with_tones:
        harmonics = 5
        for i in range(1, harmonics+1):
            subsrc.add_virtualsource('sine_{}'.format(i), signal = Sine(frequency=(frequency*i)))

    if with_noise:
        #noise = subsrc.add_virtualsource('noise', signal = Noise(color='pink'), level=140.)

        # 16 to 16000 Hz
        octaves = OctaveBand(fstart=15., fstop=16000)

        levels = {
            '16.'   :   105.,
            '31.5'  :   110.,
            '63'    :   115.,
            '125'   :   120.,
            '250'   :   120.,
            '500'   :   115.,
            '1000'  :   110.,
            '2000'  :   105.,
            '4000'  :   95.,
            '8000'  :   80.,
            }

        levels = np.array(list(levels.values()))[:,None]

        noise = subsrc.add_virtualsource('noise',
                                        signal = NoiseBands(
                                            bands=octaves,
                                            gains=levels,
                                            color='pink',
                                            state=np.random.RandomState(seed=100)
                                            ), level=120.)

    # Receiver
    rcv = model.add_receiver(name='receiver', position=Point(2.0,-5.0,1.7))

    # Ground surface
    frequencies = np.arange(0.1, fs/2.0, df)
    flow_resistivity = 2e5 # Flow resistivity of grass
    impedance = np.nan_to_num(impedance_delany_and_bazley(frequencies, flow_resistivity))
    #impedance = np.ones_like(frequencies) + 1j*np.ones_like(frequencies)

    dx = 100.0
    groundcorners1 = [Point(-dx, -dx, 0.0),
                      Point(+dx, -dx, 0.0),
                      Point(+dx, +dx, 0.0),
                      Point(-dx, +dx, 0.0)]
    ground1 = Wall(groundcorners1, Point(0.0, 0.0, 0.0), impedance)
    model.geometry.walls = [ground1]

    # Immission
    signal = pd.Series(mono( rcv.auralise() ).toarray())

    h5save(name, signal, {'fs': fs})
