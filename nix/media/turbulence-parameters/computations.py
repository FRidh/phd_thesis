"""
Demonstrate the effects of turbulence parameters.
Outputs a hdf5 file per event.
"""
import argparse
import os
from common_simulation import simulate
from auraliser import get_default_settings
import itertools
from concurrent.futures import ProcessPoolExecutor as Pool

def get_settings(length, variance):
    settings = get_default_settings()
    # Default propagation settings
    settings['spreading']['include'] = True
    settings['doppler']['include'] = True
    settings['doppler']['purge_zeros'] = True
    settings['atmospheric_absorption']['include'] = True
    settings['reflections']['include'] = True
    settings['reflections']['force_hard'] = True
    settings['reflections']['include'] = True

    # Turbulence settings
    settings['turbulence']['include'] = True
    settings['turbulence']['amplitude'] = True
    settings['turbulence']['phase'] = True
    settings['turbulence']['seed'] = 200

    settings['turbulence']['correlation_length'] = length
    settings['turbulence']['mean_mu_squared'] = variance

    return settings


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    target = lambda name: os.path.join(args.target, "{}.hdf5".format(name))

    run_simulation = lambda length, variance: simulate(
        get_settings(length, variance),
        os.path.join(args.target, "turbulence-{}-{}.hdf5".format(length, variance))
        )

    lengths = [ 1.0, 10.0, 100.0 ]
    variances = [ 1e-7, 1e-6, 1e-5]
    jobs = list(set(list(itertools.product(lengths, [1e-5])) + list(itertools.product([10.0], variances))))

    #jobs = [
        #(1.0, 100000),
        #(10.0, 1.e-5),
        #(100.0, 1.e-5),
        #(10.0, 1.e-5),
        #(10.0, 1.e-6),
        #(10.0, 1.e-7),
        #]
    #jobs = list(set(jobs))
    #print(jobs)

    list(itertools.starmap(run_simulation, jobs))

    #with Pool(2) as pool:
        #list(pool.map(run_simulation, list(zip(*jobs))))


    #for variance in variances:
        #settings['turbulence']['correlation_length'] = 10.0
        #settings['turbulence']['mean_mu_squared'] = variance
        #simulate(settings, target('variance-{}'.format(variance)))

    #for length in lengths:
        #settings['turbulence']['correlation_length'] = length
        #settings['turbulence']['mean_mu_squared'] = 1e-5
        #simulate(settings, target('correlation-length-{}'.format(length)))


if __name__ == '__main__':
    main()
