# Fork of COCOAPI

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

- `PythonAPI/asym_eval.py`: Use this when only want to evaluate a subset of the images that are predicted on. Create a GT json that only contains the subset you want (important point: make sure the `image_id`s are unchanged), then test it against the prediction json (prediction json can contain images not in the subset GT json).

- `PythonAPI/visualise_bb.py`: Outputs visualised GT and predicted bbs on each validation image in the GT json. Able to take in asym pred vs GT (similar to `asym_eval.py`)