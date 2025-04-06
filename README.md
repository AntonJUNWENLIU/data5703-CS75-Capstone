
## 🧠 Micro-SAM Integration (Experimental)

Micro-SAM is now available as an optional segmentation backend.  
To enable it, edit `New_server.py`:

```python
from micro_sam.automatic_segmentation import automatic_instance_segmentation
```

Micro-SAM supports point-based and automatic segmentation, suitable for batch processing and time-series data.

---

## ⚙️ Batch Processing (CLI)

You can now run segmentation on a whole folder using:

```bash
python -m micro_sam.automatic_segmentation \
  -i ./images/ --pattern *.tif \
  -o ./masks/ -e ./embeddings/ \
  -m vit_b --device cuda
```

This will automatically process each image and store results.
