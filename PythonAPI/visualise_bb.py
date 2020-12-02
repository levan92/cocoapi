import json
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict

import cv2
from tqdm import tqdm

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

parser = argparse.ArgumentParser()
parser.add_argument('GTfile')
parser.add_argument('DTfile')
parser.add_argument('root', help='path to root')
parser.add_argument('outdir', help='path to output dir')
args = parser.parse_args()

GTpath = Path(args.GTfile)
DTpath = Path(args.DTfile)
assert GTpath.is_file()
assert DTpath.is_file()

root_path = Path(args.root)
assert root_path.is_dir()

outdir = Path(args.outdir)
outdir.mkdir(parents=True, exist_ok=True)

cocoGt=COCO(str(GTpath))
gt_img_ids = cocoGt.getImgIds()
DT_json = json.load(open(str(DTpath)))
new_DT_annotations = [ instance for instance in DT_json if instance['image_id'] in gt_img_ids ]
cocoDt=cocoGt.loadRes(new_DT_annotations)

# Quantitative Eval
cocoEval = COCOeval(cocoGt,cocoDt,'bbox')
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()

# Qualitative Eval - Visualisation
print('Generating visualisation of predictions and GTs on validation images..')
cats = cocoGt.loadCats(cocoGt.getCatIds())
imgs_deets = cocoGt.loadImgs(gt_img_ids)

img2GT = defaultdict(list)
img2DT = defaultdict(list)

gt_ann_ids = cocoGt.getAnnIds()
instances_gt = cocoGt.loadAnns(gt_ann_ids)
for inst in instances_gt:
    img2GT[inst['image_id']].append(inst)
dt_ann_ids = cocoDt.getAnnIds()
instances_dt = cocoDt.loadAnns(dt_ann_ids)
for inst in instances_dt:
    img2DT[inst['image_id']].append(inst)

def draw(img, ltwh, text='', color=(255,255,0)):
    thickness = 2
    font = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 0.5
    fontThickness = 1
    buff = 5

    l,t,w,h = ltwh
    r = l + w
    b = t + h
    l,t,r,b = [ int(x) for x in [l,t,r,b] ]
    cv2.rectangle(img, (l,t), (r,b), color, thickness)
    if text:
        cv2.putText(img, text, (l+buff,b-buff),  font, fontScale, color, fontThickness)

for img_id in tqdm(gt_img_ids):
    imgpath = root_path / imgs_deets[img_id]['file_name']
    assert imgpath.is_file()
    img = cv2.imread(str(imgpath))
    
    gts = img2GT[img_id]
    for gt in gts:
        cat_id = gt['category_id']
        cat = cats[cat_id-1]['name']
        text = cat
        ltwh = gt['bbox']
        draw(img, ltwh, text=text, color=(0,255,0))

    dts = img2DT[img_id]
    for dt in dts:
        cat_id = dt['category_id']
        cat = cats[cat_id-1]['name']
        score = dt['score']
        text = f'{cat}:{score:0.2f}'
        ltwh = dt['bbox']
        draw(img, ltwh, text=text, color=(0,0,255))

    viz_path = outdir / f'{img_id}-{imgpath.stem}.jpg'
    cv2.imwrite(str(viz_path), img)

