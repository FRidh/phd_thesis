import argparse
import pandas as pd
import shutil
import os

parser = argparse.ArgumentParser()
parser.add_argument('rules', type=str)
parser.add_argument('files', type=str)
parser.add_argument('target', type=str)
args = parser.parse_args()

rules = pd.read_csv(args.rules).fillna("")

rules['Filename'] = rules.apply(lambda x: f"{x['Figure'].replace('.','-')}{x['Extra']}.wav", axis=1)
#print(rules[['Source', 'Filename']])

for i, row in rules.iterrows():
    shutil.copyfile(os.path.join(args.files, row.Source), os.path.join(args.target, row.Filename))
