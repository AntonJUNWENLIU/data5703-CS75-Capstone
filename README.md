# Micro-SAM - V2.0.1

[![Docs](https://shields.mitmproxy.org/badge/docs-pdoc.dev-brightgreen.svg)](https://computational-cell-analytics.github.io/micro-sam/)
[![Conda](https://anaconda.org/conda-forge/micro_sam/badges/version.svg)](https://anaconda.org/conda-forge/micro_sam)
[![Codecov](https://codecov.io/gh/computational-cell-analytics/micro-sam/graph/badge.svg?token=7ETPP5CABP)](https://codecov.io/gh/computational-cell-analytics/micro-sam)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7919746.svg)](https://doi.org/10.5281/zenodo.7919746)

---

<p align="right">
  <img src="https://github.com/computational-cell-analytics/micro-sam/blob/master/doc/logo/logo_and_text.png" width="300">
</p>

**Micro-SAM** is a Napari plugin that enables interactive segmentation for microscopy images, powered by Meta’s [Segment Anything](https://segment-anything.com/).  
It supports fast 2D segmentation and microscopy-specific model fine-tuning.

---

## 🔧 Features

- ✅ **Interactive 2D segmentation**  
  Supports prompt-based segmentation using point, box, brush, and eraser tools with real-time mask visualization.

- ✅ **Folder selection & batch image access**  
  Allows users to select a folder and browse multiple images, including support for multi-channel data with a channel slider.

- ✅ **Custom cache path configuration**  
  Users can define a custom cache directory for embeddings and segmentation results, enabling organized storage and reproducibility.

- ✅ **Efficient loading of saved segmentation results**  
  Previously saved masks are automatically loaded when available, avoiding redundant computation and accelerating workflows.


<p align="center">
  <img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/d04cb158-9f5b-4460-98cd-023c4f19cccd" width="250">
  <img src="https://github.com/computational-cell-analytics/micro-sam/assets/4263537/dfca3d9b-dba5-440b-b0f9-72a0683ac410" width="250">
</p>

---

## 🚀 Getting Started

Set up the plugin locally with the following steps:

```bash
# 2. Install in editable mode
pip install -e .

# 3. Launch napari
napari
```

To ensure all dependencies are correctly configured, use the provided environment:

```bash
conda env create -f environment.yaml
conda activate micro-sam
```

See the [official documentation](https://computational-cell-analytics.github.io/micro-sam/) for more setup instructions and usage tips.

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
