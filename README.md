# Construction Safety PPE Detection

A computer vision project that detects personal protective equipment (PPE) in construction site images. It uses a [YOLOv8](https://docs.ultralytics.com/) object detection model and exposes a lightweight [FastAPI](https://fastapi.tiangolo.com/) service for running inference over uploaded images.

The model is trained to recognize five classes relevant to workplace safety: `helmet`, `no-helmet`, `no-vest`, `person`, and `vest`.

## Features

- **REST API for detection** — upload an image and receive detected objects with class labels, confidence scores, and bounding boxes.
- **PPE-aware classes** — distinguishes between workers wearing or missing helmets and vests.
- **Reproducible training** — a training script built on YOLOv8 with configurable hyperparameters.
- **Dataset download helper** — a script to fetch the dataset export used for training.
- **Simple, dependency-driven setup** — all requirements pinned in `requirements.txt`.

## Tech Stack

- **Language:** Python 3
- **Model / CV:** Ultralytics YOLOv8, OpenCV, NumPy
- **Deep learning runtime:** PyTorch, TorchVision
- **API:** FastAPI, Uvicorn, python-multipart
- **Dataset tooling:** Roboflow

## Project Structure

```
.
├── main.py               # FastAPI app exposing the /detect endpoint
├── train.py              # Trains a YOLOv8 model on the dataset
├── download_dataset.py   # Downloads the dataset export (YOLOv8 format)
├── data.yaml             # Dataset config: paths and class names
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

Generated or downloaded artifacts (not tracked in version control):

- `best.pt` — trained model weights loaded by the API.
- `construction-safety-2/` — dataset export used for training.
- `runs/` — training outputs and metrics.

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

This project reads configuration from environment variables. Create a `.env` file (or export the variables in your shell) using placeholder values such as the following:

```env
# API key for the dataset provider (used by download_dataset.py)
ROBOFLOW_API_KEY=<your-roboflow-api-key>
```

> Never commit real credentials. Use placeholders in documentation and keep your actual `.env` file out of version control.

## Usage

### 1. Download the dataset (optional, for training)

```bash
python download_dataset.py
```

This downloads the dataset export in YOLOv8 format. Make sure the resulting folder matches the `path` setting in `data.yaml`.

### 2. Train the model (optional)

```bash
python train.py
```

Training produces model weights under `runs/`. Copy or rename the resulting best weights to `best.pt` in the project root so the API can load them.

### 3. Run the API server

Make sure `best.pt` exists in the project root, then start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive API docs are served at `http://127.0.0.1:8000/docs`.

### 4. Send a detection request

Upload an image to the `/detect` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/detect" \
  -F "file=@path/to/image.jpg"
```

Example response:

```json
[
  {
    "class": "helmet",
    "conf": 0.92,
    "box": [34, 58, 120, 140]
  }
]
```

Each result includes the detected `class`, the confidence score `conf`, and the bounding box `box` as `[x1, y1, x2, y2]` pixel coordinates.

## Screenshots

_Add screenshots or sample detection results here._

<!--
![Detection example](docs/screenshot-1.png)
![API docs](docs/screenshot-2.png)
-->

## License

No license has been specified for this project yet. Add a `LICENSE` file and update this section to declare the terms under which the project may be used.
