# README - 5703 Plugin v1.0

## Overview

This plugin integrates the **SAM2** model with the **Napari** interface to enhance image segmentation capabilities. Version **v0.3** introduces several improvements in functionality, accuracy, and stability.

---

## Key Features

**Enhanced Logic and Code Refactoring**

- Segmentation results are now written into separate `Labels` layers for better visualization:
  - **Point** → `Points_mask`
  - **Box** → `Box_mask`
  - **Auto-Segmentation** → `AutoSeg_Labels`

**Flexible Labeling Modes**

- Supports two fusion modes for Point and Box prompts:
  - \`\`: Adds new labels without modifying existing ones.
  - \`\`: Refines existing labels using `union`, `intersection`, or `overwrite` logic.

**Improved Stability and Performance**

- Improved **coordinate handling** to ensure segmentation aligns correctly with the original image.
- Flask server logic enhanced by adding `predictor.set_image()` to prevent stale image caching issues.

**Event Blocking Mechanism**

- Ensures only the latest point is retained during Point-based segmentation to prevent recursive errors.

**Multi-label Overlay**

- Each new segmentation now assigns a unique label ID by referencing the maximum label value in the current layer.

---

## Installation

Ensure you have the following dependencies installed:

```bash
pip install sam2
pip install napari
pip install flask
```

---

## Configuration

To resolve file path issues in SAM2, ensure your `CONFIG_PATH` is set correctly:

### Recommended Solution

```python
import sam2
import os

sam2_path = os.path.dirname(sam2.__file__)
CONFIG_PATH = os.path.join(sam2_path, "configs", "sam2.1", "sam2.1_hiera_l.yaml")
```

### Alternative Solutions

- Correct the path in `initialize()`:

```python
initialize(config_path=os.path.join(sam2_path, "configs"), version_base=None)
```

- If needed, ensure your working directory is set correctly:

```bash
cd E:\USYD\Course\25S1\5703\CAPSTONE
```

---

## Usage

1. **Launch Napari**

   ```bash
   napari
   ```

2. **Load Image**\
   Drag and drop the desired image file into Napari.

3. **Segmentation Modes**

   - **Point Segmentation:** Add points in the `Prompt Points` layer to trigger segmentation.
   - **Box Segmentation:** Draw a bounding box in the `Box_mask` layer.
   - **Auto Segmentation:** Use the `/auto_segment` API for full image segmentation.

4. **Result Viewing**

   - Segmentation results are stored in the following layers:
     - \`\` → Auto-segmentation results
     - \`\` → Point prompt results
     - \`\` → Box prompt results

---

## Known Issues

- **Empty Mask Issue:** Ensure Flask is correctly resetting images with `predictor.set_image()` to avoid stale image caching.
- **Coordinate Misalignment:** All segmentation methods now use original image coordinates to ensure accuracy.

---

## Upcoming Improvements

🔹 Additional testing on complex images to validate robustness.\
🔹 Improved logging for easier debugging.\
🔹 Performance optimization for faster processing of large-scale images.

---



