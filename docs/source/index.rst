plotfair
========

Beautiful color and plotting utilities for matplotlib and plotly.

**plotfair** provides curated color palettes, perceptually uniform colormaps,
and convenient wrappers to make publication-quality figures with consistent
styling across matplotlib, plotly, and interplot backends.

Features
--------

**PaintKit Color System**
   Curated color swatches with filtering by saturation (bright, dark, muted)
   and color family. Includes the Flexoki color scheme.

**Perceptual Colormaps**
   Create colormaps that are perceptually uniform using CIECAM02 color space,
   ensuring smooth gradients for data visualization.

**Matplotlib Presets**
   Publication-ready defaults with enhanced DPI, clean styling, and automatic
   figure saving to organized folders.

**Plotly Wrapper**
   Matplotlib-like interface for Plotly via the ``Plty`` class, making it easy
   to create interactive plots with familiar syntax.

**Interplot Integration**
   Pre-configured settings for the interplot library with matplotlib-style
   plotting via the ``Iplt`` class.

Quick Example
-------------

.. code-block:: python

   import plotfair as pf
   import matplotlib as mpl

   # Set a dark color scheme with rainbow ordering
   scheme = pf.paintkit.filter(tags={'dark'}).ordered_swatches(pf.full_rainbow)
   mpl.rcParams['axes.prop_cycle'] = scheme.to_cycler()

   # Create a perceptual colormap
   cmap = pf.colormaps.perceptual_colormap_nonuniform(
       ['#344885', '#E9C46A', '#AF3029'],  # blue -> yellow -> red
       [0.0, 0.5, 1.0]
   )
   pf.show_colormap(cmap, name='Custom')

.. note::

   This project is under active development.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`