# Fork of COCOAPI

All the things you need is in `PythonAPI/`

## Installation

```bash
sudo pip3 install Cython
cd PythonAPI
make
```

## Usage

```bash
cd PythonAPI
python3 eval.py <path to GT json> <path to predictions json> 
```
The JSON files for Ground Truth (GT) and Predictions are expected to be in [COCO format](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch/#coco-dataset-format) (ignore the segmentation stuff), thought not all are essential (for example things like `licenses` need not to be included in the json)

GT JSON should have `images`, `categories` and `annotations`.  

Prediction JSON can just be a list of predicted bounding boxes with `image_id` that corresponds to the `images` given in GT JSON
```json
[
  {"image_id": 0, "category_id": 1, "bbox": [0.0, 193.94281005859375, 131.76132202148438, 79.2210693359375], "score": 0.8640222549438477},
  {"image_id": 1, "category_id": 1, "bbox": [131.12359619140625, 174.27325439453125, 309.98846435546875, 62.258544921875], "score": 0.436798095703125},
  ...
]
```

## Other scripts that might be useful
- `PythonAPI/asym_eval.py`: Use this when only want to evaluate a subset of the images that are predicted on. Create a GT json that only contains the subset you want (important point: make sure the `image_id`s are unchanged), then test it against the prediction json (prediction json can contain images not in the subset GT json).

- `PythonAPI/visualise_bb.py`: Outputs visualised GT and predicted bbs on each validation image in the GT json. Able to take in asym pred vs GT (similar to `asym_eval.py`)
