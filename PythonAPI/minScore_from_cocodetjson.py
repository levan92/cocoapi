import numpy as np
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('DTjson')
args = parser.parse_args()

with open(args.DTjson,'r') as f:
    d = json.load(f)

min_score = np.inf
for det in d:
    if det['score'] < min_score:
        min_score = det['score']

print('Min score amongst all detections:',min_score)
