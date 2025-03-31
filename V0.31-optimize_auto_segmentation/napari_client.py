import os
import requests
import napari
import numpy as np
from PIL import Image

from magicgui import magicgui
from magicgui.widgets import FileEdit
from pathlib import Path

SERVER_URL_PREDICT = "http://127.0.0.1:5703/predict"  # Click-based segmentation endpoint
SERVER_URL_AUTO = "http://127.0.0.1:5703/auto_segment_adaptive"  # Automatic segmentation endpoint

g_current_image_path = None  # Stores the currently selected image path

def send_sam_predict_request(image_path, point_coords, point_labels):
    """Send a request to the click-based segmentation endpoint"""
    data = {"image_path": image_path, "prompts": [{"point_coords": point_coords, "point_labels": point_labels}]}
    try:
        response = requests.post(SERVER_URL_PREDICT, json=data)
        response.raise_for_status()
        masks = response.json().get("masks", [])
        if not masks:
            print("No mask returned")
            return None
        mask = np.array(masks[0], dtype=np.float32)
        return mask[0] if mask.ndim == 3 else mask  # Handle multi-channel cases
    except Exception as e:
        print("Request error:", e)
        return None



def send_auto_segment_request(image_path):
    """Send a request to the adaptive automatic segmentation endpoint"""
    try:
        response = requests.post(SERVER_URL_AUTO, json={"image_path": image_path})
        response.raise_for_status()
        result = response.json()
        masks = result.get("masks", [])
        params = result.get("params_used", {})
        print("Adaptive segmentation parameters used:", params)
        return [np.array(m, dtype=np.uint8) for m in masks]
    except Exception as e:
        print("Automatic segmentation request error:", e)
        return []

def main():
    viewer = napari.Viewer()

    @magicgui(call_button="Select img", filename={"widget_type": FileEdit, "mode": "r"})
    def load_image_widget(filename: Path = Path()):
        """Load an image into Napari"""
        global g_current_image_path
        if not filename.exists():
            print("Invalid file")
            return
        g_current_image_path = str(filename.resolve())
        image = Image.open(g_current_image_path).convert("RGB").resize((512, 512), Image.BICUBIC)
        viewer.layers.clear()
        viewer.add_image(np.array(image), name="Current Image")
        viewer.add_points(name="Prompt Points", ndim=2, size=20, face_color="magenta")

    @magicgui(call_button="Point segment")
    def run_sam_segmentation(viewer: napari.Viewer, points_layer: napari.layers.Points):
        """Perform click-based segmentation"""
        global g_current_image_path
        if not g_current_image_path or not os.path.exists(g_current_image_path):
            print("Please select an image")
            return
        coords_xy = points_layer.data[:, ::-1] if points_layer.data.size else np.array([])
        if coords_xy.size == 0:
            print("Please add prompt points")
            return
        mask = send_sam_predict_request(g_current_image_path, coords_xy.tolist(), [1] * len(coords_xy))
        if mask is not None:
            viewer.layers.remove("SAM_mask") if "SAM_mask" in viewer.layers else None
            viewer.add_labels((mask > 0.5).astype(np.uint8), name="SAM_mask")
            print("Segmentation complete")

    @magicgui(call_button="Auto segment")
    def run_auto_segmentation(viewer: napari.Viewer):
        """Perform automatic segmentation"""
        global g_current_image_path
        if not g_current_image_path or not os.path.exists(g_current_image_path):
            print("Please select an image")
            return
        masks = send_auto_segment_request(g_current_image_path)
        if not masks:
            print("No automatic segmentation results")
            return
        label_mask = sum(i * mask for i, mask in enumerate(masks, start=1))
        viewer.layers.remove("AutoSeg_Labels") if "AutoSeg_Labels" in viewer.layers else None
        viewer.add_labels(label_mask, name="AutoSeg_Labels")
        print("Automatic segmentation complete")

    viewer.window.add_dock_widget(load_image_widget, area="right")
    viewer.window.add_dock_widget(run_sam_segmentation, area="right")
    viewer.window.add_dock_widget(run_auto_segmentation, area="right")

    napari.run()


if __name__ == "__main__":
    main()
