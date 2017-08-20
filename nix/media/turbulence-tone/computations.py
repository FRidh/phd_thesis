
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_context("paper", font_scale=6./3.)
import matplotlib as mpl
mpl.rc("figure", figsize=(6.0, 2.5))
mpl.rc("font", size=10)
#mpl.rc("legend", fontsize=7)
mpl.rc("text", usetex=True)
mpl.rc("lines", markersize=4)
mpl.rc("lines", linewidth=0.8)
#get_ipython().magic('matplotlib inline')
from scintillations.stream import *
from scintillations.sequence import *
from acoustics import Signal
#from IPython.display import Audio
import itertools
from streaming.signal import constant


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('target', type=str)
args = parser.parse_args()

# # Common values

# In[39]:

FIGURES = "."
AUDIO = "."
EXTENSION = ".eps"

def savefig(fig, name):
    return fig.savefig(os.path.join(args.target, FIGURES, name+EXTENSION))

def saveaudio(signal, name):
    signal.normalize().to_wav(os.path.join(args.target, AUDIO, name))

linestyles = ["-","--","-.",":"]#, 'steps']
markers = ['p','o','s','.','+']


# In[3]:

speeds = np.array([1, 10, 12, 100, 110])
correlation_length = 20.
ntaps_corr = 8192

duration = 10.
fs = 8000.
nsamples = int(fs*duration)
times = np.arange(nsamples) / fs

frequency = 1000.

correlation_length = 1.1
mean_mu_squared = 3.0e-6
soundspeed = 343.2
distance = 500.

include_saturation = True
include_amplitude = True
include_phase = True

window = None
seed = 5


# # Modulated tone

# In[4]:

speed = 2.0

correlation_time = correlation_length/speed
fs_min = 5. / correlation_time
print("Correlation time: {}".format(correlation_time))
print("Sample frequency: {}".format(fs_min))

logamp, phase = generate_fluctuations_logamp_and_phase(nsamples, fs_min, ntaps_corr, correlation_length, speed, frequency, soundspeed,
                                           distance, mean_mu_squared, include_saturation=include_saturation, state=np.random.RandomState(seed=seed), window=window)
logamp = Signal(logamp, fs_min)
phase = Signal(phase, fs_min)
both = Signal([logamp, phase], fs_min)
labels = [r'$\chi$', r'$S$']

ax = both.pick(0., 10.).plot(labels=labels, title="", ylabel="Log-amplitude $\chi$, phase $S$")
fig = ax.get_figure()
fig.tight_layout()
savefig(fig, "logamp_and_phase")

_tau = tau(ntaps_corr, fs_min)


# In[8]:

tone = Signal(np.sin(2.*np.pi*frequency*times), fs).calibrate_to(94.)
modulated = modulate_tone(tone, fs, frequency, fs_min, correlation_length, speed, distance, soundspeed, mean_mu_squared,
                          ntaps_corr=ntaps_corr, window=window, include_saturation=include_saturation,
                          state=np.random.RandomState(seed=seed), include_amplitude=include_amplitude,
                          include_phase=include_phase)
both = Signal([tone, modulated], fs)
print(both.levels()[1].std(axis=-1))

saveaudio(tone, "tone.wav")
saveaudio(modulated, "modulated.wav")


# In[9]:
labels=["Tone", "Modulated"]
ax = both.plot_levels(title="", labels=labels)
fig = ax.get_figure()
fig.tight_layout()
savefig(fig, "modulated_levels")


ax = both.plot_power_spectrum(xlim=(985, 1015), ylim=(30.0, 100.0), xscale='linear', labels=labels, title="")
fig = ax.get_figure()
fig.tight_layout()
savefig(fig, "tone_broadening")


# # Correlation for different speeds

# In[11]:

ntaps_corr*64/1024


# In[46]:

correlation_length = 20.

speeds = np.array([1,10,20,100,110])

fig = plt.figure()
ax = fig.add_subplot(111)

_linestyles = itertools.cycle(iter(linestyles))

cycle = lambda x: itertools.cycle(iter(x))

points = 32

for ls, marker, speed in zip(cycle(linestyles), cycle(markers), speeds): #[1.0, 10.0, 100.0]:

    _tau = tau(512, fs=5.0/2)
    _tau = _tau[_tau>0]
    print(len(_tau))

    ax.plot(_tau, correlation_spherical_wave(_tau, correlation_length/speed), label=speed, ls=ls, marker=marker)
ax.set_xlabel(r"$\tau$ in s")
ax.set_ylabel(r"$B$")
ax.set_xlim(0.0, 10.0)
ax.legend()
fig.tight_layout()
savefig(fig, "correlation")


# # Scintillations for different speeds

# In[43]:

from scintillations.stream import modulate
from streaming.signal import sine, constant

seed = 100

signal = sine(frequency, fs).take(nsamples)

correlation_time = correlation_length / speeds.min()
fmin = 5. / correlation_time
print("Minimum sample frequency: {}".format(fmin))

nhop = 64
print("Actual sample frequency: {}".format(fs/nhop))

#fmin = fs / nhop # ideal

speeds = np.array([1,10,20,100,110])
fmin = (5. * speeds / correlation_length).max() * 10.0


_linestyles = itertools.cycle(iter(linestyles))

results = []
for speed in speeds:
    signal = sine(frequency, fs)
    result = modulate(signal, fs, nhop, correlation_length, speed, distance, soundspeed, mean_mu_squared, fmin, ntaps_corr, state=np.random.RandomState(seed=seed), include_saturation=True)
    result = Signal(result.take(nsamples).toarray(), fs)
    saveaudio(result, "scintillations_speed_{}.wav".format(speed))
    results.append(result)


modulated = Signal(results, fs)
ax = modulated.plot_levels(labels=speeds, title="")
fig = ax.get_figure()
fig.tight_layout()
savefig(fig, "scintillations_levels")



