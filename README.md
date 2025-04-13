# 5703 Napari Plugin v1.0

## 1. Overview

This plugin integrates the **SAM2** model with the **Napari** visualization interface to enable efficient segmentation of biomedical images.

Version 1.0 implements the following features:
- Supports point prompts, box prompts, and automatic segmentation
- Provides multiple label fusion strategies (merge / intersect / overwrite)
- Supports **tile-based segmentation** for improved resolution handling
- Adds custom label naming and in-view visualization
- Refactors server/client logic to resolve fixed image segmentation errors

---

## 2. Quick Start

### 1. Start the Backend Server
```bash
cd Server
python New_server.py
```

### 2. Launch the Napari Plugin
```bash
napari
```

---

## 3. Key Features

### Segmentation Modes
- **Point Prompt** → `Points_mask`
- **Box Prompt** → `Box_mask`
- **Auto Segmentation** → `AutoSeg_mask`

### Tile-based Segmentation
- For large-scale images, supports `tile_shape` division
- Segments image by tiles and stitches results to avoid boundary errors

### Label Renaming
- Users can assign custom names (e.g., “Nucleus”, “Membrane”) to label IDs
- Displayed directly in the Napari layer UI

### Technical Enhancements
- Ensures `predictor.set_image()` is invoked on every image switch
- Removed unnecessary prompt-loop bugs
- Manages label ID assignment automatically

---

## 4. Installation

Ensure the following dependencies are installed:
```bash
pip install sam2 napari flask
```

Or install the full environment from:
```bash
pip install -r requirements.txt
```

> It is recommended to use Conda for creating an isolated environment to avoid version conflicts.

---

## 5. Model Configuration

First, download SAM2 checkpoints:
```bash
cd checkpoints
wget https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_large.pt
...
```

Set up `config_path`:
```python
import sam2
import os
sam2_path = os.path.dirname(sam2.__file__)
CONFIG_PATH = os.path.join(sam2_path, "configs", "sam2.1", "sam2.1_hiera_l.yaml")
```

---

## 6. How to Use the Plugin

1. Start the server and Napari
2. Load an image and input prompts (point/box)
3. Click AUTO-SEGMENT to generate segmentation
4. Assign a label name and visualize in Napari

---

## 7. Known Issues

- Segmentation fails: ensure `set_image()` is called on every switch
- Misaligned masks: fixed by restoring original image coordinates
- Slight inconsistencies across Windows/macOS environments

---

## 8. Roadmap

- [ ] Support packaging & export for tile-based segmentation
- [ ] Enhance logging and error reporting
- [ ] Implement UI label management panel
- [ ] Integrate Micro-SAM for efficient tiling + embedding

---

## 9. Contact

For questions, contact Jie Chen (or raise an issue on GitHub).
