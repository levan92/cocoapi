import json
import argparse
import numpy as np
from pathlib import Path
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

parser = argparse.ArgumentParser()
parser.add_argument('GTfile')
parser.add_argument('DTfile')
args = parser.parse_args()


GTpath = Path(args.GTfile)
DTpath = Path(args.DTfile)
assert GTpath.is_file()
assert DTpath.is_file()


cocoGt=COCO(str(GTpath))

gt_img_ids = cocoGt.getImgIds()
DT_json = json.load(open(str(DTpath)))
new_DT_annotations = [ instance for instance in DT_json if instance['image_id'] in gt_img_ids ]

cocoDt=cocoGt.loadRes(new_DT_annotations)

# print(cocoGt.getImgIds())
# imgIds=sorted(cocoGt.getImgIds())
# imgIds=imgIds[0:100]
# imgId = imgIds[np.random.randint(100)]

cocoEval = COCOeval(cocoGt,cocoDt,'bbox')
# cocoEval.params.imgIds  = imgIds
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()
