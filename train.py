from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
DATA_YAML = ROOT / "construction-safety-2" / "data.yaml"

if not DATA_YAML.is_file():
    raise FileNotFoundError(
        f"Dataset config not found at {DATA_YAML}. "
        "Download the dataset with download_dataset.py or verify construction-safety-2/ exists."
    )

weights = ROOT / "yolov8m.pt"
if not weights.is_file():
    weights = ROOT / "yolov8n.pt"
if not weights.is_file():
    weights = Path("yolov8m.pt")

model = YOLO(str(weights))

model.train(
    data=str(DATA_YAML),
    epochs=100,
    imgsz=640,
    batch=16,
    lr0=0.001,
    project=str(ROOT / "runs" / "detect"),
)
