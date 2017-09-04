from wand.image import Image
import argparse
from pathlib import Path

FORMAT = 'png'

parser = argparse.ArgumentParser()
parser.add_argument("source", type=str)
parser.add_argument("target", type=str)
args = parser.parse_args()

source = Path(args.source)
target = Path(args.target)

for f in source.rglob('*.eps'):
    print(f)
    with Image(filename=f) as img:
        img.format = FORMAT
        #img.save(filename=target.joinpath(f.relative_to(source).with_suffix(FORMAT)))
