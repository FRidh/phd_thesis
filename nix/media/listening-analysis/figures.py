import argparse
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import glob
import collections
import itertools
import numpy as np
import seaborn as sns
import csv

import matplotlib as mpl
mpl.rc("figure", figsize=(3.0, 2.5))
mpl.rc("font", size=10)
#mpl.rc("legend", fontsize=7)
mpl.rc("text", usetex=True)
mpl.rc('font', **{'family':'serif', 'serif':['Computer Modern Roman'],
                                'monospace': ['Computer Modern Typewriter']})

DPI = 600

FIGSIZE_SMALL = (3.0, 2.5)
FIGSIZE_WIDE = (6.0, 2.5)
FIGSIZE_LARGE = (6.0, 6.0)


NBINS = 11 # because we use an eleven-point scale

SCALING = NBINS - 1

AIRCRAFT = {
    '11_103_A320' : ('A320', 1),
    '17_131_A320' : ('A320', 2),
    '10_068_RJ1H' : ('RJ1H', 3),
    '12_093_RJ1H' : ('RJ1H', 4)
}

Pair = collections.namedtuple('Pair', ['participant', 'part', 'pair', 'a', 'b'])


def jsonload(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def yield_stimuli(stimuli):
    for stimulus in stimuli:
        event = stimulus['event']['event']
        aircraft, occasion = AIRCRAFT[event]
        yield {
            'part': stimulus['part'],
            'occasion': occasion,
            'kind' : stimulus['kind'],
            'hash': stimulus['hash'],
            'aircraft': aircraft,
            'event' : event,
        }


def get_pairs(tests):
    for instance, test in tests.items():
        for part in test['parts']:
            for i, pair in enumerate(test['tests'][part]['pairs']):
                yield Pair(instance, part, i+1, pair[0]['hash'], pair[1]['hash'])


def makefig(target, data, x, y, hue=None, xlabel="", title="", plotkind="swarm"):
    PLOT = {
        "swarm": sns.swarmplot,
        "box" : sns.boxplot,
        "violin": sns.violinplot,
    }
    func = PLOT[plotkind]

    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE_WIDE)
    order = sorted(set(data[x]))
    ax = func(x=x, y=y, hue=hue, data=data, order=order, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Similarity rating")
    ax.set_title(title)#Similarity ratings grouped by aircraft type combinations. Recordings only.")
    fig = ax.get_figure()
    fig.suptitle("")
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #labels = ax.get_xticklabels()
    #for label in labels:
        #label.set_rotation(30)
    fig.savefig(target, dpi=DPI, bbox_extra_artists=[legend], bbox_inches='tight')
    #return fig


def makefig_kdeplot(data, x, y, xlabel="Similarity rating", ylabel="Kernel density estimate", title=""):

    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE_SMALL)
    for name, column in data.reset_index(drop=True).pivot(columns=x, values=y).iteritems():
        sns.kdeplot(column.dropna(), ax=ax)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 2.3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)#Similarity ratings grouped by aircraft type combinations. Recordings only.")
    fig = ax.get_figure()
    fig.suptitle("")
    #labels = ax.get_xticklabels()
    #for label in labels:
        #label.set_rotation(30)
    fig.tight_layout()#subplots_adjust(bottom=0.35, left=0.25)
    return fig


#def kdeplot_of_groups(groups, target, xlabel="Similarity rating", ylabel="Kernel density estimate"):
    #fig, ax = plt.subplots(1, 1, figsize=FIGSIZE_WIDE)

    #lines = ['-', '--', '-.', ':']

    #for label, group, line in zip(*zip(*groups), itertools.cycle(lines)):
        #sns.kdeplot(group.rating.dropna(), ax=ax, label="{}, {}".format(*label), linestyle=line)
    #ax.set_xlim(0.0, 1.0)
    #ax.set_ylim(0.0, 2.3)
    #ax.set_xlabel(xlabel)
    #ax.set_ylabel(ylabel)
    #legend = ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    #fig.subplots_adjust(right=0.8)
    #fig.savefig(target, dpi=DPI, bbox_extra_artists=[legend], bbox_inches='tight')


def histplot_groups(data, target, xlabel="Similarity rating", ylabel="Density"):
    groups = data.groupby(['aircraft', 'kind'])

    nrows, ncolumns = 3, 3
    fig, axes = plt.subplots(nrows, ncolumns, figsize=FIGSIZE_LARGE, sharex=True, sharey=True)
    indices = list(itertools.product(range(nrows), range(ncolumns)))

    #data.rating.hist(by=data['aircraft', 'kind'], ax=ax)
    for label, group, ix in zip(*zip(*groups), indices):
        label = "{}, {}".format(*label)
        ax = axes[ix]
        sns.distplot(group.rating.dropna(), ax=ax, bins=NBINS, axlabel=label, kde_kws={
            'linewidth' : 1,
            #'color'     : 'green'
            }, hist_kws={
            'linewidth' : 1,
            'histtype'  : 'step',
            'color'     : 'black'
            })
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 3.5)
        ax.set_title(label)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if ix[0] != 2:
            ax.set_xlabel("")
        if ix[1] != 0:
            ax.set_ylabel("")

    fig.savefig(target, dpi=DPI, bbox_inches='tight')

def get_dataset(folder_test, file_results):

    # Load test parts
    parts = jsonload(os.path.join(folder_test, 'config_stimuli.json'))['stimuli']['parts']
    # Load test stimuli
    stimuli = jsonload(os.path.join(folder_test, 'stimuli.json'))
    stimuli = pd.DataFrame(list(yield_stimuli(stimuli))).set_index('hash')
    stimuli.loc[stimuli.kind == 'recording', 'kind'] = 'rec'
    stimuli.loc[stimuli.kind == 'turbulence', 'kind'] = 'sim'

    # Load tests
    tests = (jsonload(filename) for filename in glob.iglob(os.path.join(folder_test, 'tests', '*.json')))
    tests = {test['instance']: test for test in tests}

    # Pairs
    pairs = pd.DataFrame(list(get_pairs(tests)))
    pairs = pairs.set_index(['part', 'pair', 'participant'])

    # Load test results
    results = pd.read_csv(file_results)

    # Melt so we have a part column and rating column instead
    results = pd.melt(results, id_vars=['participant', 'pair'], var_name='part', value_name='rating')

    # Ratings from 0 to 10.
    results.rating -= 1

    # Normalize ratings from 0 to 1.
    normalize = lambda x: (x-x.min()) / (x.max()-x.min())
    #results.rating = results.groupby(['participant', 'part']).rating.transform(normalize)
    results.rating /= SCALING

    # And use a multi-index
    results = results.set_index(['part', 'pair', 'participant'])

    ratings = pairs.join(results)
    # We're not anymore interested in the pair numbers, since those were test/participant-dependent and contain no more interesting information since we now have the hashes of the stimuli
    ratings.index = ratings.index.droplevel('pair')
    ratings.reset_index().set_index(['part', 'participant', 'a', 'b']).head()

    full = ratings.merge(stimuli, left_on='a', right_index=True).merge(stimuli, left_on='b', right_index=True, suffixes=('_a', '_b'))
    full = full.rename(columns={'a':'hash_a', 'b':'hash_b'})
    full['part'] = full.part_a
    del full['part_a']
    del full['part_b']
    full = full.assign(aircraft=(full.aircraft_a+", "+full.aircraft_b), kind=(full.kind_a+", "+full.kind_b)).replace("sim, rec", "rec, sim")

    # Get rid of part multiindex, and move participant to column.
    full = full.reset_index('part', drop=True).reset_index()

    full = full.replace({
        'start' :   'approach',
        'center':   'fly-over',
        'end'   :   'distancing'
        })

    return full


#def zscores_effect_approaches(data, target):
    #from statsmodels.stats.weightstats import ztest

    #a = {name: group for name, group in data.groupby(['aircraft', 'kind'])}
    #b = {name: group for name, group in data[data.part!='approach'].groupby(['aircraft', 'kind'])}

    #scores = list()

    #for name in b.keys():
        #x = a[name]
        #y = b[name]
        #zscore, pvalue = ztest(x.rating.dropna(), y.rating.dropna())
        #scores.append({'name':name, '$z$-score':zscore, '$p$-value':pvalue})

    #scores = pd.DataFrame(scores).set_index('name', drop=True)
    #with open(target, 'w') as f:
        #f.write(scores.to_latex(escape=False, float_format='%.2f'))


def create_figures(data, target):
    #### How similar are the recordings? We average over all parts.
    ###kind = 'rec'
    ###selection = data[(data.kind_a==kind) & (data.kind_b==kind)]
    ###fig = makefig_kdeplot(data=selection, x='aircraft', y='rating')
    ###fig.savefig(os.path.join(target, 'figure1_ratings_recordings.eps'), dpi=DPI)

    #### How similar are the auralizations? We average over all parts.
    ###kind = 'sim'
    ###selection = data[(data.kind_a==kind) & (data.kind_b==kind)]
    ###fig = makefig_kdeplot(data=selection, x='aircraft', y='rating')
    ###fig.savefig(os.path.join(target, 'figure2_ratings_simulations.eps'), dpi=DPI)

    ####
    ###aircraft = 'A320'
    ###selection = data[(data.aircraft_a==aircraft) & (data.aircraft_b==aircraft)]
    ###fig = makefig_kdeplot(data=selection, x='kind', y='rating')
    ###fig.savefig(os.path.join(target, 'figure3_ratings_{}.eps'.format(aircraft)), dpi=DPI)

    ####
    ###aircraft = 'RJ1H'
    ###selection = data[(data.aircraft_a==aircraft) & (data.aircraft_b==aircraft)]
    ###fig = makefig_kdeplot(data=selection, x='kind', y='rating')
    ###fig.savefig(os.path.join(target, 'figure4_ratings_{}.eps'.format(aircraft)), dpi=DPI)

    ####
    ####ax = data.boxplot('rating', by=['aircraft', 'kind'])
    ####labels = ax.get_xticklabels()
    ####for label in labels:
        ####label.set_rotation(30)
    ####ax.set_title("Similarity ratings grouped by aircraft and stimuli type combinations")
    ####ax.set_xlabel("Groups")
    ####ax.set_ylabel("Similarity rating")
    ####fig = ax.get_figure()
    ####fig.suptitle("")
    ####fig.savefig(os.path.join(target, 'figure_ratings.eps'), dpi=DPI)

    #### The following two figures are boxplots per stimuli type combination and per part.

    ####
    ###aircraft = 'A320'
    ###selection = data[(data.aircraft_a==aircraft) & (data.aircraft_b==aircraft)]# & (data.part=='end')]
    ###makefig(os.path.join(target, 'figure5_ratings_{}.eps'.format('part_'+aircraft)),
            ###selection, 'kind', 'rating', hue="part", xlabel="Stimuli type combinations", plotkind='box')

    ####
    ###aircraft = 'RJ1H'
    ###selection = data[(data.aircraft_a==aircraft) & (data.aircraft_b==aircraft)]# & (data.part=='end')]
    ###makefig(os.path.join(target, 'figure6_ratings_{}.eps'.format('part_'+aircraft)),
            ###selection, 'kind', 'rating', hue="part", xlabel="Stimuli type combinations", plotkind='box')


    #kdeplot_of_groups(data.groupby(['aircraft', 'kind']), os.path.join(target, 'figure_kde.eps'))


    #Histograms of all groups
    histplot_groups(data                            , os.path.join(target, 'histograms.eps'))
    histplot_groups(data[data.part!='approach']     , os.path.join(target, 'histograms_no_approach.eps'))
    histplot_groups(data[data.part=='approach']     , os.path.join(target, 'histograms_approach.eps'))
    histplot_groups(data[data.part=='fly-over']      , os.path.join(target, 'histograms_flyover.eps'))
    histplot_groups(data[data.part=='distancing']   , os.path.join(target, 'histograms_distancing.eps'))


def write_latex_table(df, filename):

    names = {
        'mean'   :   '$\mu$',
        'std'    :   '$\sigma$',
        'count'  :   '$n$',
        'kind'   :   'stimuli'
        }
    #pd.set_option('precision', 2) # Precision of floats
    df = df.rename(columns=names)
    #df = df.drop('SE', axis=1) # Drop SE because its very small.

    with open(filename, 'w') as f:
        f.write(df.to_latex(escape=False, float_format='%.2f'))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('folder_tests', type=str)
    parser.add_argument('file_results', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    data = get_dataset(args.folder_tests, args.file_results)

    # zscore difference with and without approaches
    #zscores_effect_approaches(data, os.path.join(args.target, 'table_zscore_effect_approaches.tex'))

    # Tables
    # We aggregate observations that are samples from a larger distribution.
    # Therefore, we consider the sample standard deviation which has 1 ddof fewer (N-1).
    # pandas already does that by default.

    agg = data.groupby(['part', 'kind', 'aircraft']).rating.aggregate({'mean':'mean', 'std':'std', 'count':'count', 'SE': lambda x: np.std(x,ddof=1)/np.sqrt(len(x))})
    write_latex_table(agg, os.path.join(args.target, 'table_analysis_parts.tex'))
    agg = data.groupby(['kind', 'aircraft']).rating.aggregate({'mean':'mean', 'std':'std', 'count':'count', 'SE': lambda x: np.std(x,ddof=1)/np.sqrt(len(x))})
    write_latex_table(agg, os.path.join(args.target, 'table_analysis.tex'))

    # Exclude start/approach part
    agg = data[data.part!='approach'].groupby(['kind', 'aircraft']).rating.aggregate({'mean':'mean', 'std':'std', 'count':'count', 'SE': lambda x: np.std(x,ddof=1)/np.sqrt(len(x))})
    write_latex_table(agg, os.path.join(args.target, 'table_analysis_no_approach.tex'))

    # Figures
    create_figures(data, args.target)

if __name__ == '__main__':
    main()
