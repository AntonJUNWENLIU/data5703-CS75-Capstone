import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import sys
import torch
import logging
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image

from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

from micro_sam.util import get_sam_model
from micro_sam.embedding import precompute_image_embeddings
from micro_sam.instance_segmentation import AutomaticMaskGenerator
from micro_sam.automatic_segmentation import get_predictor_and_segmenter, automatic_instance_segmentation



# ========== Globals ==========
_cached_embedding = None


# ========== Device Detection ==========
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


# ========== Paths and configurations ==========
CHECKPOINT_PATH = "./checkpoints/sam2.1_hiera_large.pt"
CONFIG_PATH = "configs/sam2.1/sam2.1_hiera_l.yaml"

device = get_best_device()

# ========== Load models ==========
logging.info("Loading SAM2 model...")
try:
    model_sam2 = build_sam2(CONFIG_PATH, CHECKPOINT_PATH, device=device)
    model_sam2.to(device)
    predictor = SAM2ImagePredictor(model_sam2)
    logging.info("SAM2 model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    sys.exit(1)

# ========== Flask app ==========
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "SAM2 Server is running"})

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


# ========== Micro-SAM segmentation helper ==========
def run_micro_sam_auto_segmentation(image_np, model_type="vit_b", device=device, embedding=None):
    """
    A drop-in replacement for micro-sam AMG instance segmentation.
    Automatically detects 2D/3D and runs correct workflow.
    If embedding is provided, use it directly.
    """
    if image_np.ndim == 3 and image_np.shape[-1] in (1, 3):
        ndim = 2
    else:
        ndim = image_np.ndim

    assert ndim in (2, 3), f"Expected 2D or 3D image, got shape={image_np.shape}"

    predictor, segmenter = get_predictor_and_segmenter(
        model_type=model_type,
        device=device,
        amg=True,  # Enable automatic mask generation mode
        is_tiled=False,
    )

    # Optional: inject precomputed embeddings
    if embedding is not None:
        predictor.set_precomputed_embeddings(embedding)

    prediction = automatic_instance_segmentation(
        predictor=predictor,
        segmenter=segmenter,
        input_path=image_np,
        ndim=ndim,
    )

    return prediction



# ========== Combined SAM2 + micro-sam ==========
def run_sam2_and_micro(image_np, device=device):
    global _cached_embedding

    # 1. SAM2 prediction
    mask_generator_sam2 = SAM2AutomaticMaskGenerator(
        model_sam2,
        points_per_side=16,
        pred_iou_thresh=0.7,
        stability_score_thresh=0.8
    )
    masks_sam2 = mask_generator_sam2.generate(image_np)
    label_sam2 = np.zeros(image_np.shape[:2], dtype=np.uint16)
    for i, m in enumerate(masks_sam2):
        label_sam2[m["segmentation"]] = i + 1

    # 2. micro-sam prediction using fallback-compatible method
    print("Running micro-sam automatic instance segmentation...")
    label_micro = run_micro_sam_auto_segmentation(
        image_np=image_np,
        model_type="vit_b",  # can change to "vit_b_lm" if needed
        device=device,
        embedding=_cached_embedding
    )
    label_micro = label_micro.astype(np.uint16)

    return label_sam2.tolist(), label_micro.tolist()


# ========== Embedding Endpoint ==========
@app.route("/compute_embedding", methods=["POST"])
def compute_embedding():
    try:
        data = request.json
        image_path = data["image_path"]
        image = np.array(Image.open(image_path).convert("RGB"))

        predictor = get_sam_model("vit_b", device=device)
        embedding = precompute_image_embeddings(predictor, image)

        global _cached_embedding
        _cached_embedding = embedding

        return jsonify({"status": "embedding computed "})
    except Exception as e:
        logging.error(f"Embedding error: {e}")
        return jsonify({"error": str(e)}), 500


# ========== Auto Segment Endpoint ==========
@app.route("/auto_segment", methods=["POST"])
def auto_segment():
    try:
        data = request.json
        image_path = data.get("image_path")

        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400

        image_pil = Image.open(image_path).convert("RGB")
        image_np = np.array(image_pil)

        with torch.inference_mode():
            sam2_mask, micro_mask = run_sam2_and_micro(image_np, device)

        return jsonify({
            "sam2_mask": sam2_mask,
            "micro_mask": micro_mask
        })

    except Exception as e:
        logging.error(f"Error during auto_segment: {e}")
        return jsonify({"error": str(e)}), 500


# ========== Run Flask and Napari ==========
from napari import Viewer, run
import threading

def start_napari():
    viewer = Viewer()
    viewer.window.show()
    run()

def start_flask():
    app.run(host="0.0.0.0", port=5703, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    viewer = Viewer()
    run()
    # start_flask()
