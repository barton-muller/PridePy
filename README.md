# PridePy

Beautiful, flexible color and plotting utilities for matplotlib in Python.

## Features
- Custom color swatches and palettes
- Perceptually uniform and sRGB colormap creation
- Default plotting presets for publication-quality figures
- Plotting wrappers for curve fitting and more

## Installation
```bash
pip install .
```
Or build a wheel and install:
```bash
python setup.py sdist bdist_wheel
pip install dist/PridePy-*.whl
```

## Usage Example
```python
import PridePy as pp
import matplotlib.pyplot as plt
import numpy as np

# Use a custom color cycle
plt.plot(np.arange(10), label='demo')
plt.legend()
plt.show()

# Use a perceptual colormap
colors = [swatch.hex for swatch in pp.colors.paintkit.ordered_swatches(['blue','pink','orange']).colors]
positions = [0.0, 0.5, 1.0]
cmap = pp.colormaps.perceptual_colormap_nonuniform(colors, positions)
pp.colormaps.show_colormap(cmap, name='Perceptual Colormap')
```

## Documentation
See docstrings in each module for details on classes and functions.
# Pridey
# Pridey
