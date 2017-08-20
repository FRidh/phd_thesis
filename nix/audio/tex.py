import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('rules', type=str)
parser.add_argument('target', type=str)
args = parser.parse_args()

rules = pd.read_csv(args.rules, dtype=str).fillna("")

rules['Filename'] = rules.apply(lambda x: f"\code{{{x['Figure'].replace('.','-')}{x['Extra']}.wav}}", axis=1)
table = rules[['Figure', 'Description', 'Filename']]
table = table.set_index('Figure', drop=True)

with open(args.target, 'w') as f:
    f.write(table.to_latex(escape=False))
