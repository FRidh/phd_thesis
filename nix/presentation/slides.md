---
title:  "Auralisation of airplanes considering sound propagation in a turbulent atmosphere"
author: Frederik Rietdijk
date: June 8th, 2017
theme: black

---

## Auralisation of airplanes considering sound propagation in a turbulent atmosphere

Frederik Rietdijk

September 22nd, 2017

## Introduction

### Story


<div class="notes">

- short story about personal experience with aircraft noise in Zurich.
- include an aircraft sound

</div>

### Aircraft noise

- 

- introduction to aircraft sound

### Auralisation

- introduction to auralisation / virtual acoustics

### Goal

1. Develop a tool to simulate the audible sound of the current fleet of airplanes
2. Improve plausibility by considering atmospheric turbulence

### Presentation overview

- Aircraft auralisation tool
    - Propagation
    - Emission
- Perceptual validation
- Atmospheric turbulence
- Conclusions

## Aircraft auralisation tool

### Overview

- Simulate audible sound
- Sound propagation
- Sound emission
- Backpropagation

## Sound propagation

### Propagation model


<div class="notes">

- order matters

</div

### Reflection



### Emission

<!-- ![](../media/propagation/emission.png){#id .class width=1000 height=500px} -->

<!--<p><audio controls><source src="../media/propagation/emission.wav" /></audio></p>-->

### Spreading

<!--![](../media/propagation/spreading.png){#id .class width=1000 height=500px}
<p><audio controls><source src="../media/propagation/spreading.wav" /></audio></p>-->

### Doppler shift

<!--![](../media/propagation/doppler.png){#id .class width=1000 height=500px}
<p><audio controls><source src="../media/propagation/doppler.wav" /></audio></p>-->

<!--### Atmospheric attenuation

![](../media/propagation/attenuation.png){#id .class width=1000 height=500px}
<p><audio controls><source src="../media/propagation/attenuation.wav" /></audio></p>-->

### Ground reflection

<!--![](../media/propagation/reflection.png){#id .class width=1000 height=500px}
<p><audio controls><source src="../media/propagation/reflection.wav" /></audio></p>-->


## Sound emission

### Emission "model"


### Recording


### Backpropagation


### Emission


### Auralisation


## Perceptual validation

### Goal

*Validate that the auralisation tool delivers plausible auralisations, taking into account the differences between airplane models*

### Possible approaches

- Compare sound pressure levels? Spectrally?
- Compare effective perceived noise level (EPNL)?
- Psychoacoustic measures? Loudness, ...?
- Variations in group?
- Compare groups, not individual stimuli

### Hypothesis

*recordings and auralisations of aircraft of the same
type and under similar conditions are samples of the same group*

### Method

- Take offs, 8x 12 second events
    - 2x A320 and 2x RJ1H
    - auralisation for each recording
- Rate similarity between two stimuli
    - 11-point scale, "not so much" to "very much"
    - 28 combinations of recordings and auralisations
- Long events, cut into 3 parts of 4 seconds
    - approach, fly-over, distancing
    - each part considered separately
    - all stimuli presented before test as "anchor"
- Mono, headphones, no HRTF's, fade in/out

## Results

### What some participants said

- Noted larger differences at especially the approach and the distancing
- Heard “two or three“ airplanes
- Surprised when told that simulations were included

### Descriptors

<!-- ![](../media/table_analysis.png){#id .class width=1000px height=800px} -->

### Descriptors, without approach

<!-- ![](../media/table_analysis_no_approach.png){#id .class width=1000px height=800px} -->

### Total

![](figures/generated/listening-analysis/histograms.png){#id .class width=800px height=800px}

### Total, without approach

![](figures/generated/listening-analysis/histograms_no_approach.png){#id .class width=800px height=800px}

### Discussion

- Standard deviations all similar
    - Large difference mean values, hypothesis not valid
- Small difference "total"/"total without approach"
    - Does not affect conclusion
- Distributions in a row are not alike, hypothesis not valid
- Auralisations may sound like another airplane type
- Only few events considered
- Improvement: better synthesis of BPF


## Atmospheric turbulence

### Introduction

- Temperature and wind fluctuations
- Refractive-index variations
- 
- Amplitude and phase modulations (scintillations)
- Improve perceptual validity

<!-- spectrogram showing the spikes -->

<div class="notes">

- be clear that this is about sound propagation

</div

### Goal

*Design a filter that accounts for scintillations*

### 


### Results - Tone


### Results - Airplane


### Discussion


## Conclusions

- Airplane auralisation tool was developed
    - Propagation model
    - Backpropagation model, feature extraction
- Perceptual validation through listening test
    - Similarity of recordings and auralisations tested
    - Auralisations not yet similar to recordings
    - Participants can discriminate between aircraft types


## Future work

- Improve synthesis of tones phase, and BPF power
- Use more events per group in listening test
- Develop generic airplane emission model
- Subjective validation of scintillations model


<!-- ## Aircraft take-off -->

<!--### Recording

![](data/recording.png)

<audio controls><source src="data/recording.wav" /></audio>

### Auralisation

![](data/auralisation.png)

<audio controls><source src="data/auralisation.wav" /></audio>

### Auralisation with turbulence

![](data/turbulence.png)

<audio controls><source src="data/turbulence.wav" /></audio>-->


<!--
## Atmospheric turbulence

*Develop an algorithm for taking into account fluctuations due to turbulence*-->


<!--## Quality of simulations

- Listening test
- Participants rated similarity
- Auralisations rated as plausible-->

<!--
## Conclusions

- Auralisation tool developed
- Novel algorithm for turbulence fluctuations
- Differences still noticeable
- Auralisations rated as plausible-->


## That's it!

Thank you for your attention



<!--
Presentation
- 5 minutes introduction
- 10 minutes auralisation tool
    - 2 minutes overview
    - 4 minutes propagation
    - 4 minutes backpropagation
- 7 minutes validation
- 5 minutes turbulence
- 3 minutes conclusion
-->
