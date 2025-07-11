# PridePy

A package for default matplotlib settings that are better for including in posters/presentations/reports as well as providing a better set of colours which can be used to make nice qualitative colourmaps as well as gradients.
  
  <img src="https://github.com/user-attachments/assets/5b459000-0cc4-44ab-b634-b683cdd4bf7f" height="350" />
  <img src="https://github.com/user-attachments/assets/23035b7b-6f01-41da-9a44-3d7c8fa495f4" height="350" />

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

