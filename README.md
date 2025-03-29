# 5703 Napari Plugin v1.0

## Overview

This Napari plugin integrates the **SAM2** model to provide interactive and accurate image segmentation for biological and medical images.

Version **v1.0** introduces improved stability, refined labeling logic, and a new **label renaming feature** for enhanced usability.

---

## 🔥 Quick Start

⚠️ **Important: Start the backend server before launching the plugin!**

```bash
# Step 1: Run the backend server
cd Server
python New_server.py
```

```bash
# Step 2: Open the client/plugin
napari
```

---

## Key Features

### 🎯 Segmentation Modes

- **Point Prompt Segmentation** → stored in `Points_mask`
- **Box Prompt Segmentation** → stored in `Box_mask`
- **Auto Segmentation** → stored in `AutoSeg_mask`

Each segmentation assigns **unique label IDs**, ensuring proper multi-label support.

---

### 🧐 Labeling Modes

- **Add Mode**: Insert new labels on top of existing ones  
- **Refine Mode**: Update existing labels using:
  - `union`
  - `intersection`
  - `overwrite`

---

### ✏️ Label Renaming

You can assign meaningful **names to labels**, such as `"nucleus"` or `"membrane"`:

- Accessible via the `NAME LABEL` button
- Supports interactive overlay showing names directly on the viewer
- All label names are stored in metadata and rendered above each region

---

### ⚙️ Technical Improvements

- 🔁 **Event blocker**: Prevents recursive prompt loops by only using the latest point  
- 🧹 **Auto label ID assignment**: Tracks and increments from max label ID  
- 🧠 **Predictor caching fixed**: Server uses `predictor.set_image()` to load fresh images per request  
- 📀 **Coordinate accuracy**: All segmentation uses native image coordinates, avoiding shift artifacts

---

## Installation

Make sure the following dependencies are installed:

```bash
pip install sam2 napari flask
```

---

## Model Checkpoints

Download and store SAM2 checkpoints:

```bash
cd checkpoints
wget https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_large.pt
wget https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_small.pt
wget https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_tiny.pt
cd ..
```

Expected structure:

```
checkpoints/
├── sam2.1_hiera_large.pt
├── sam2.1_hiera_small.pt
└── sam2.1_hiera_tiny.pt
```

---

## Loading the SAM2 Model

Example:

```python
import sam2
import os
import torch

sam2_path = os.path.dirname(sam2.__file__)
CONFIG_PATH = os.path.join(sam2_path, "configs", "sam2.1", "sam2.1_hiera_l.yaml")

with torch.compile():
    predictor = SAM2ImagePredictor(build_sam2(CONFIG_PATH, checkpoint))
```

---

## How to Use the Plugin

1. **Start the server first**:
   ```bash
   cd Server
   python New_server.py
   ```

2. **Then open Napari**:
   ```bash
   napari
   ```

3. **Image Segmentation Modes**:
   - Draw **points** in the `Prompt Points` layer
   - Draw **boxes** in the `Bounding Box` layer
   - Click **AUTO-SEGMENT** to get full image labels

4. **Label Renaming**:
   - Use the `NAME LABEL` widget
   - Choose `label_id` and assign a name like `"cell nucleus"`
   - Overlay will update automatically to show label names

---

## Known Issues

- 🧊 **Empty mask on server**: Make sure `predictor.set_image()` is used per request.
- 📀 **Misaligned segmentation**: Solved via strict coordinate tracking.
- 🖥️ **Run order matters**: Always run `New_server.py` **before** interacting with the plugin.

---

## Roadmap

- 🔜 Export segmentation masks to file  
- 🔜 Batch processing for auto-segmentation  
- 🔜 Logging and advanced UI widgets for label control  

---

## Contact

Any question, please contact me by email or github
