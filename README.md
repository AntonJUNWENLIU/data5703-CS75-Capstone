# CS75 Napari Cell-segmentation Plug-in Based on micro-sam - V2.0.1

---

<p align="right">
  <img src="![截屏2025-05-29 15 39 48](https://github.com/user-attachments/assets/189b392e-af18-46c4-8a1d-b7936c9353a4)
" width="300">
</p>

**CS75 Cell-segmentation Plug-in** is a cell image segmentation plug-in based on Napari, designed for researchers to perform multi-channel microscopic image analysis. Users can load .tiff or .jpg images in batches by dragging a single image or selecting a folder, using the slider to switch different channels, and performing embedded calculations and automatic segmentation on each channel. The plug-in supports two ways to save segmentation results: pixel-level and object-level. It allows users to set a label ID for each channel and merge and save the results through a commit operation. In case of unsatisfactory segmentation results, users can manually adjust parameters or use interactive tools such as box selection, point selection, and eraser to make corrections. Finally, the segmentation results of all channels can be exported as TIFF files for subsequent analysis and archiving. It supports fast 2D segmentation and microscopy-specific model fine-tuning.

---

## 🔧 Features

🖼️ **1. Image Loading & Channel Control**
- Support dragging a single image or selecting a folder to load images in batches
- Support image formats: .tiff, .jpg
- Support multi-channel image switching, browse each channel through the slider
- Each channel can be processed and segmented separately

🧠 **2. Embedding & Segmentation**
- Compute Embedding operation can be performed on the current channel to generate and cache embedded features
- Click the button to perform automatic segmentation
- The automatically generated segmentation results are displayed as mask layers, and the layer order can be adjusted to view the effect

💾 **3. Segmentation Result Management (Mask Management)**
- Provides two saving modes:
- Pixels mode: All results are saved in the same mask
- Objects mode: Generate a separate mask for each segmentation
- Support setting the label ID for each segmentation
- Provide a Commit button to merge segmentation results and save as the final mask

🎛️ **4. Parameter Tuning & Segmentation Optimisation**
- Adjustable segmentation model parameters, such as minimum area, stability, threshold, etc.
- Each parameter adjustment can affect the subsequent segmentation effect in real time

✍️ **5. Interactive Segmentation Tools**
- Box segmentation: Re-segment the area locally by selecting a box
- Point prompts: Click on the image to add positive/negative points to guide segmentation correction
- Eraser tool: Manually erase the segmentation error area
- Supports visibility switch (seen/unseen) of the mask layer

📤 **6. Exporting Results**
- Supports exporting segmentation results of different images and channels as .tiff or .zarr files
- The exported content has a clear structure, suitable for subsequent analysis and archiving

<p align="center">
  <img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/d04cb158-9f5b-4460-98cd-023c4f19cccd" width="250">
  <img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/dfca3d9b-dba5-440b-b0f9-72a0683ac410" width="250">
</p>

---

## 🚀 How to configure the virtual environment and gett started

Set up the plugin locally with the following steps:

```bash
# 1. Install in editable mode
pip install -e .

# 2. Launch napari
napari
```

To ensure all dependencies are correctly configured, use the provided environment:

```bash
conda env create -f environment.yaml
conda activate micro-sam
```

---

## Plugin Usage Instructions (Step-by-step)

### 1. **Launch the Plugin**
- Open your terminal in a conda environment where the plugin is installed.
- Run:
  ```bash
  napari
  ```
- In Napari, go to the top menu:  
  **Plugins → Annotator 2D**


### 2. **Load Image(s)**
- Option 1: Drag a single `.tiff` or `.jpg` image into the Napari window.  
- Option 2: Click the **Select Folder** button on the right panel to load a folder of images.


### 3. **Navigate Image and Channel**
- Click the **Open** button to display the first image.
- Use the **channel slider** at the bottom to switch between different image channels (e.g., Ch1, Ch2...).


### 4. **Compute Embedding**
- For each channel you want to segment:
  - Select the channel via the slider.
  - Click **Compute Embedding** to generate feature representations (required before segmentation).


### 5. **Automatic Segmentation**
- Click **Automatic Segmentation** to generate segmentation masks for the current channel.
- The result will appear in the **layer panel on the left**.


### 6. **Choose Save Mode & Label**
- From the dropdown, choose one of the **preserve modes**:
  - `pixels`: overwrite the same mask
  - `objects`: save each result as a separate mask
- Adjust the **Label ID** using the `+` or `–` buttons before committing.


### 7. **Commit the Result**
- Click **Commit** to save the segmentation result to the final mask layer.
- Repeat steps 3–7 for all desired channels.


### 8. **(Optional) Refine the Mask**
- If segmentation is inaccurate:
  - Use **parameter sliders** (e.g., threshold, min area) to adjust the model.
  - Use **Box Segmentation** to draw a region and refine it.
  - Use **Point Prompts** to add positive or negative points for fine control.
  - Use the **Eraser Tool** to manually clean small errors.


### 9. **Manage Layers**
- Use the **Seen/Unseen (eye icon)** on the left to toggle mask visibility.
- Drag masks to reorder layers if needed.


### 10. **Export Segmentation Results**
- When all desired masks are committed:
  - Click **Export to TIFF** (bottom-right)  
  - This will save all masks per image and channel to the output folder.


---

## Back-end Design structure

Diagram below is the back-end design structure.

![image](https://github.com/user-attachments/assets/3338eba4-7d5e-4322-af25-23dc1a7d56c8)

---

## Sample Result

### Segmentation Result Output

![image](https://github.com/user-attachments/assets/31ff6e8d-d492-4a96-a1e3-439004c06578)

### Ground Truth Mask

![image](https://github.com/user-attachments/assets/f97398fa-0772-4e7e-8e2a-ff9be29ed8fc)

---

## 📖 Citation

If you use this tool in your work, please cite the following:

- [Micro-SAM: Nature Methods 2024](https://www.nature.com/articles/s41592-024-02580-4)  
- [Segment Anything](https://arxiv.org/abs/2304.02643)  
- [MobileSAM](https://arxiv.org/abs/2306.14289) (for ViT-tiny models)

---

## 🔬 Related Projects

- [Patho-SAM](https://github.com/computational-cell-analytics/patho-sam) – for histopathology
- [Medico-SAM](https://github.com/computational-cell-analytics/medico-sam) – for medical imaging
- [PEFT-SAM](https://github.com/computational-cell-analytics/peft-sam) – for parameter-efficient fine-tuning

Other related Napari-based SAM plugins:
- [napari-sam (MIC-DKFZ)](https://github.com/MIC-DKFZ/napari-sam)
- [napari-segment-anything (royerlab)](https://github.com/royerlab/napari-segment-anything)

---

© Computational Cell Analytics – MIT License
