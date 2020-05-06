import json
import argparse
from pathlib import Path
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('detjson')
# parser.add_argument('-c', '--cats', nargs='+', type=int, required=True)
parser.add_argument('filter_mapping')
args = parser.parse_args()

jsonpth = Path(args.detjson)
with jsonpth.open('r') as f:
    dets = json.load(f)

filter_mapping = {}
with open(args.filter_mapping,'r') as f:
    for line in f.readlines():
        bef, aft = line.strip().split(':')
        filter_mapping[int(bef)] = int(aft)

print('Wanted Categories filter mapping:')
pprint(filter_mapping)

wanted = []
for det in dets:
    bef = int(det['category_id'])
    if bef in filter_mapping:
        aft = filter_mapping[bef]
        det['category_id'] = aft
        wanted.append(det)

new_jsonpth = jsonpth.parent / '{}{}{}'.format(jsonpth.stem,'_filtered',jsonpth.suffix)
with new_jsonpth.open('w') as f:
    json.dump(wanted, f)

