# AGENTS.md

## Cursor Cloud specific instructions

This repo is a small Python service: a YOLO (Ultralytics) construction-safety object
detector served via FastAPI. There is no README, no tests, and no linter configured.

### Layout / what runs
- `main.py` — FastAPI app exposing `POST /detect` (multipart image upload → JSON list of
  `{class, conf, box}`). Run it in dev with `uvicorn main:app --reload` (Swagger UI at `/docs`).
- `train.py` — Ultralytics training script (100 epochs); produces a model.
- `download_dataset.py` — pulls the Roboflow `construction-safety` dataset (needs network/Roboflow access).
- `data.yaml` — dataset config (5 classes: helmet, no-helmet, no-vest, person, vest).

### Non-obvious gotchas
- **`best.pt` is required at import time.** `main.py` raises `FileNotFoundError` on startup
  unless `best.pt` exists in the repo root. `*.pt` is gitignored and the real trained model is
  NOT in the repo. The real `best.pt` comes from `train.py`, which needs the dataset
  (`construction-safety-2/`, downloaded via `download_dataset.py`) and ~100 CPU/GPU epochs —
  infeasible to fully run in a quick session.
  - For dev/demo without training, drop in a pretrained Ultralytics model as a stand-in:
    `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"` then `cp yolov8n.pt best.pt`.
    The API then loads and returns COCO-class detections (e.g. `person`, `bus`) — enough to
    verify the full FastAPI + YOLO + OpenCV stack end to end.
- **CPU-only VM.** `torch` installs NVIDIA/CUDA wheels but runs fine on CPU; ignore the lack of GPU.
- Dependencies live in a local virtualenv at `.venv` (created by the startup update script).
  Activate with `source .venv/bin/activate`, or call binaries directly via `.venv/bin/...`.
- `train.py` and `download_dataset.py` are not wired into the API and are not needed to run the service.

### Quick verification (hello world)
```
source .venv/bin/activate
[ -f best.pt ] || { python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"; cp yolov8n.pt best.pt; }
uvicorn main:app --host 0.0.0.0 --port 8000 --reload   # leave running
curl -L -o /tmp/t.jpg https://ultralytics.com/images/bus.jpg
curl -X POST localhost:8000/detect -F "file=@/tmp/t.jpg;type=image/jpeg"
```
