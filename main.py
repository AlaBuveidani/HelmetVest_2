from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "best.pt"

if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"Model weights not found at {MODEL_PATH}. "
        "Train the model with train.py or place best.pt in the project root."
    )

app = FastAPI()
model = YOLO(str(MODEL_PATH))


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    np_arr = np.frombuffer(contents, np.uint8)
    try:
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except cv2.error as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not decode image. Upload a valid JPEG or PNG file.",
        ) from exc

    if img is None:
        raise HTTPException(
            status_code=400,
            detail="Could not decode image. Upload a valid JPEG or PNG file.",
        )

    results = model(img)
    boxes = results[0].boxes
    names = model.names

    if boxes is None or len(boxes) == 0:
        return []

    return [
        {
            "class": names[int(cls)],
            "conf": float(conf),
            "box": [int(x1), int(y1), int(x2), int(y2)],
        }
        for (x1, y1, x2, y2), cls, conf in zip(
            boxes.xyxy, boxes.cls, boxes.conf
        )
    ]
