import numpy as np
import json
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('DTjson')
parser.add_argument('minscore', type=float)
args = parser.parse_args()

with open(args.DTjson,'r') as f:
    d = json.load(f)

target_min = args.minscore
assert target_min > 0

new_dets = []
for det in d:
    if det['score'] > target_min:
        new_dets.append(det)

DTjson_path = Path(args.DTjson)
new_DTjson = DTjson_path.parent / '{}{}{}'.format(DTjson_path.stem, '_filtered-min-score', DTjson_path.suffix) 
with new_DTjson.open('w') as f:
    json.dump(new_dets, f)

diff = len(d) - len(new_dets)
print('Filtered away {} out of {} detections'.format(diff, len(d)))