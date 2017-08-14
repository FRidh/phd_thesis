from auraliser import Auraliser, mono, get_default_settings
from acoustics import Signal
import numpy as np
from auraliser.auralisation import recursive_mapping_update, get_default_settings
import dill

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_auralisation(modelfile, settings):
    """Create auralisation. Load model from `modelfile` and update settings with `settings`
    """

    with open('auralisation.pickle', 'rb') as f:
        model = dill.load(f)

    model.settings = recursive_mapping_update(recursive_mapping_update(get_default_settings(), model.settings), settings)

    ##plt.plot(np.linalg.norm(np.diff(src.position*model.sample_frequency, axis=0), axis=-1)[10000::10])

    #maxspeed = np.linalg.norm(np.diff(src.position*model.sample_frequency, axis=0), axis=-1)[10000::10].max()
    #correlation_length = 20.
    #correlation_time = correlation_length / maxspeed

    #print("Minimum sample frequency: {}".format(5. / correlation_time))
    #print("Maximum hop size: {}".format(model.sample_frequency / (5./correlation_time)))


    model.settings = get_default_settings()
    model.settings['turbulence']['include'] = False
    model.settings['turbulence']['covariance'] = 'gaussian'
    model.settings['turbulence']['mean_mu_squared'] = 3.0e-6
    model.settings['turbulence']['correlation_length'] = 1.1
    #model.settings['turbulence']['ntaps'] = 4096
    #model.settings['turbulence']['saturation'] = True
    #model.settings['turbulence']['force_constant_distance'] = np.max
    #model.settings['turbulence']['amplitude'] = False
    #model.settings['turbulence']['phase'] = True
    #model.settings['turbulence']['fraction'] = 1
    model.settings['turbulence']['seed'] = 100

    model.settings['doppler']['purge_zeros'] = False
    model.settings['reflections']['include'] = True # Broken. Without everything works!
    model.settings['doppler']['include'] = True
    model.settings['spreading']['include'] = True
    model.settings['atmospheric_absorption']['include'] = True

    model.settings['turbulence']['nhop'] = 128
    model.settings['nblock'] = 128
    model.settings['reflections']['update_resolution'] = model.settings['nblock']
    model.settings

    rcv = model.get_object('receiver')

    fs = model.sample_frequency
    duration = 10.
    nsamples = int(fs*duration)


def main():

    # Without turbulence

    #model.settings['turbulence']['include'] = False
    model.settings['turbulence']['include'] = False
    model.settings['turbulence']['amplitude'] = False
    model.settings['turbulence']['phase'] = False
    signal = mono(rcv.auralise())
    signal = Signal(signal.take(nsamples).toarray(), fs)


    without = signal


    # With turbulence (logamp)

    model.settings['turbulence']['include'] = True
    model.settings['turbulence']['amplitude'] = True
    model.settings['turbulence']['phase'] = False
    signal = mono(rcv.auralise())
    signal = Signal(signal.take(nsamples).toarray(), fs)

    #_ = signal.plot_spectrogram(ylim=(0.0, 4000.0), clim=(-40, +60))

    with_logamp = signal


    # With turbulence (phase)

    model.settings['turbulence']['include'] = True
    model.settings['turbulence']['amplitude'] = False
    model.settings['turbulence']['phase'] = True
    signal = mono(rcv.auralise())
    signal = Signal(signal.take(nsamples).toarray(), fs)


    # In[21]:

    #Audio(data=signal, rate=signal.fs)


    # In[22]:

    _ = signal.plot_spectrogram(ylim=(0.0, 4000.0), clim=(-40, +60))


    # In[23]:

    with_phase = signal


    # ## With turbulence (logamp and phase)

    # In[24]:

    model.settings['turbulence']['include'] = True
    model.settings['turbulence']['amplitude'] = True
    model.settings['turbulence']['phase'] = True
    signal = mono(rcv.auralise())
    signal = Signal(signal.take(nsamples).toarray(), fs)


    # In[25]:

    #Audio(data=signal, rate=signal.fs)


    # In[26]:

    _ = signal.plot_spectrogram(ylim=(0.0, 4000.0), clim=(-40, +60))


    # In[27]:

    with_logamp_and_phase = signal


    # In[28]:

    signals = Signal([without, with_logamp, with_phase, with_logamp_and_phase], fs)


    # In[29]:

    labels = ['Without', 'Logamp', 'Phase', 'Both']


    # In[30]:

    fig = signals.plot_levels(labels=labels)


    # In[31]:

    _ = signals.plot_third_octaves(labels=labels)


    # ## Save figures and audio files

    # In[34]:

    #with sns.axes_style(rc={"axes.grid":False}):

    clim = (0.0, +70)
    ylim = (0.0, 4000.0)

    for signal, label in zip(signals, labels):
        signal.normalize().to_wav("../audio/auralisation_flight_{}.wav".format(label.lower()))
        fig = signal.plot_spectrogram(ylim=ylim, clim=clim, title="")
        fig.subplots_adjust(bottom=0.2, left=0.2)
        fig.savefig("../figures/auralisation_flight_{}.eps".format(label.lower()))




if __name__ == '__main__':
    main()

