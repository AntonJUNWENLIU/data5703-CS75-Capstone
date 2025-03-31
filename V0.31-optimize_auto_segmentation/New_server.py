import os
import sys
import torch
import logging
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image

from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

# 1) Device Detection
def get_best_device():
    if torch.backends.mps.is_available():
        print("Using MPS (Apple GPU).")
        return "mps"
    elif torch.cuda.is_available():
        print("Using CUDA (NVIDIA GPU).")
        return "cuda"
    else:
        print("Using CPU.")
        return "cpu"

# 2) Paths and configurations
CHECKPOINT_PATH = "./checkpoints/sam2.1_hiera_large.pt"
CONFIG_PATH = "configs/sam2.1/sam2.1_hiera_l.yaml"

device = get_best_device()

# 3) Load model
logging.info("Loading SAM2 model...")
try:
    model = build_sam2(CONFIG_PATH, CHECKPOINT_PATH, device=device)
    model.to(device)
    predictor = SAM2ImagePredictor(model)
    logging.info("SAM2 model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    sys.exit(1)

# 4) Create Flask application
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "SAM2 Server is running"})

# 5) Click-based segmentation endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        image_path = data.get("image_path")
        input_prompts = data.get("prompts", [])

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_pil = Image.open(image_path).convert("RGB")
        image_np = np.array(image_pil)

        predictor.set_image(image_np)

        all_masks = []
        with torch.inference_mode(), torch.autocast(device, dtype=torch.float32):
            for prompt in input_prompts:
                point_coords = np.array(prompt.get("point_coords", []), dtype=np.float32)
                point_labels = np.array(prompt.get("point_labels", []), dtype=np.int64)

                masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)
                all_masks.append(masks.tolist())

        return jsonify({"masks": all_masks})

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

# 6) Automatic segmentation endpoint
@app.route("/auto_segment", methods=["POST"])
def auto_segment():
    try:
        data = request.json
        image_path = data.get("image_path")

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_pil = Image.open(image_path).convert("RGB")
        image_np = np.array(image_pil)

        mask_generator = SAM2AutomaticMaskGenerator(model, points_per_side=16, pred_iou_thresh=0.7, stability_score_thresh=0.8)

        with torch.inference_mode(), torch.autocast(device, dtype=torch.float32):
            masks = mask_generator.generate(image_np)

        all_masks_list = [m["segmentation"].astype(np.uint8).tolist() for m in masks]

        return jsonify({"masks": all_masks_list})

    except Exception as e:
        logging.error(f"Error during auto_segment: {e}")
        return jsonify({"error": str(e)}), 500

# 7) Adaptive auto-segmentation endpoint
@app.route("/auto_segment_adaptive", methods=["POST"])
def auto_segment_adaptive():
    try:
        data = request.json
        image_path = data.get("image_path")

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_pil = Image.open(image_path).convert("RGB")
        image_np = np.array(image_pil)

        height, width = image_np.shape[:2]

        # Adaptive parameter setting
        if max(height, width) <= 512:
            params = dict(points_per_side=32, pred_iou_thresh=0.85, stability_score_thresh=0.9, crop_n_layers=1, crop_overlap_ratio=0.5)
        elif max(height, width) <= 1024:
            params = dict(points_per_side=24, pred_iou_thresh=0.8, stability_score_thresh=0.85, crop_n_layers=1, crop_overlap_ratio=0.3)
        else:
            params = dict(points_per_side=16, pred_iou_thresh=0.7, stability_score_thresh=0.8, crop_n_layers=0, crop_overlap_ratio=0.2)

        mask_generator = SAM2AutomaticMaskGenerator(model, **params)

        with torch.inference_mode(), torch.autocast(device, dtype=torch.float32):
            masks = mask_generator.generate(image_np)

        all_masks_list = [m["segmentation"].astype(np.uint8).tolist() for m in masks]

        return jsonify({"masks": all_masks_list, "params_used": params})

    except Exception as e:
        logging.error(f"Error during adaptive auto_segment: {e}")
        return jsonify({"error": str(e)}), 500

# 8) Box-based segmentation endpoint
@app.route("/box_segment", methods=["POST"])
def box_segment():
    try:
        data = request.json
        image_path = data.get("image_path")
        box_coords = data.get("box_coords")

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_pil = Image.open(image_path).convert("RGB")
        image_np = np.array(image_pil)

        predictor.set_image(image_np)

        x_min, y_min, x_max, y_max = box_coords
        box_array = np.array([float(x_min), float(y_min), float(x_max), float(y_max)], dtype=np.float32)

        with torch.inference_mode():
            masks, _, _ = predictor.predict(
                point_coords=None,
                point_labels=None,
                box=box_array[None, :],
                multimask_output=False
            )

        binary_mask = (masks[0] > 0.5).astype(int).tolist()

        return jsonify({"mask": binary_mask})

    except Exception as e:
        logging.error(f"Error during box_segment: {e}")
        return jsonify({"error": str(e)}), 500

# 9) Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5703, debug=False)
