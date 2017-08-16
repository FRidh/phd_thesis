# Backside

Having an airport nearby can be convenient, but there are also strong
disadvantages. One major disadvantage is noise. Aircraft are loud, and because
they are elevated they affect more people than for example a car passing by. In
the last decades flying became more accessible. Cities are expanding and more
people than ever live close to an airport. While modern aircraft are more quiet,
the amount of people exposed to aircraft noise has gone up significantly.

This is a big issue, since aircraft noise is known to cause stress, annoyance,
and sleep disturbance. In order to determine how many people are affected by
aircraft noise, we first need to investigate when they are affected. Let us
consider for example annoyance. When is the aircraft noise causing annoyance and
what is making it so annoying? We need to find out what factors play a role, and
we need to try and quantify their contribution, because that gives the
possibility to develop aircraft that sound less annoying, or could cause less
sleep disturance.

In order to investigate these aspects, experiments need to be conducted, and
these typically involve people listening to sounds of aircraft and rating the
sounds. In science it is desirable to have fine control over your experiment in
order to reduce errors due to unwanted influences. While recordings of aircraft
could be used, they may include a lot of unwanted variables. For example, the
wind may affect the sound but you do not know by how much. How reliable will
your results then be?

A simulation tool can give a controlled and reproducible output, and therefore
such a tool was developed to simulate the audible sound of aircraft. In order to
be useful, such a tool should produce simulations, or auralisations, that sound
sufficiently similar to actual events. An experiment was therefore conducted
where participants rated how similar the auralisations were to the recordings.
The auralisations did not sound sufficiently similar to the recordings, and
improvements are therefore needed before the tool could be used for
investigating aircraft noise impact.

How realistic auralisations sound can depend on many factors. One factor that is
thought to be important is the impact of atmospheric turbulence on sound
propagation. When you listen to distant aircraft you can hear strong
fluctuations in the loudness. Earlier aircraft sound simulators did not include
this effect. An algorithm was therefore developed that would account for these
fluctuations, and this algorithm was implemented in the simulation tool.
According to the author this addition results in auralisations that sound more
realistic, but whether this is indeed the case has not yet been verified.
