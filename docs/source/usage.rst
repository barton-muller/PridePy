Usage Guide
===========

.. _installation:

Installation
------------

Install plotfair using pip:

.. code-block:: console

   $ pip install plotfair

Or install from source:

.. code-block:: console

   $ pip install .

Quick Start
-----------

Import plotfair and start using its features:

.. code-block:: python

   import plotfair as pf
   import matplotlib.pyplot as plt

   # Access the paintkit color palette
   print(pf.paintkit)

   # Filter colors by tags
   dark_colors = pf.paintkit.filter(tags={'dark'})

PaintKit: Colors and Palettes
-----------------------------

The ``paintkit`` object provides access to curated color swatches that can be
filtered, ordered, and converted to matplotlib cyclers or colormaps.

Filtering Colors
^^^^^^^^^^^^^^^^

.. code-block:: python

   import plotfair as pf

   # Filter by saturation
   bright = pf.paintkit.filter(tags={'bright'})
   dark = pf.paintkit.filter(tags={'dark'})
   muted = pf.paintkit.filter(tags={'muted'})

   # Filter by color family
   blues = pf.paintkit.filter(tags={'blue'})

   # Get flexoki color scheme
   flexoki = pf.paintkit.filter(tags={'flexoki'})

Setting Color Cycles
^^^^^^^^^^^^^^^^^^^^

Use predefined color orderings with filtered swatches:

.. code-block:: python

   import plotfair as pf
   import matplotlib as mpl

   # Available orderings
   # pf.rainbow = ['green', 'lightblue', 'blue', 'purple', 'pink', 'fuchia', 'orange']
   # pf.full_rainbow = ['green', 'teal', 'lightblue', 'blue', 'purple', 'pink', 'fuchia', 'red', 'orange', 'yellow']
   # pf.tab10 = ['blue', 'orange', 'green', 'pink', 'purple', 'lightblue', 'fuchia', 'yellow', 'teal', 'red']

   # Create an ordered swatch collection
   scheme = pf.paintkit.filter(tags={'dark'}).ordered_swatches(pf.full_rainbow)

   # Set as default matplotlib color cycle
   mpl.rcParams['axes.prop_cycle'] = scheme.to_cycler()

   # Or set on a specific axes
   ax.set_prop_cycle(scheme.to_cycler())

Creating Colormaps
^^^^^^^^^^^^^^^^^^

Create perceptually uniform colormaps from color swatches:

.. code-block:: python

   import plotfair as pf

   # Get hex colors from swatches
   colors = [s.hex for s in pf.paintkit.ordered_swatches(['blue', 'pink', 'orange']).colors]
   positions = [0.0, 0.5, 1.0]

   # Create perceptually uniform colormap
   cmap = pf.colormaps.perceptual_colormap_nonuniform(colors, positions)

   # Display the colormap
   pf.show_colormap(cmap, name='Custom Colormap')

   # Use in a plot
   plt.imshow(data, cmap=cmap)

Matplotlib Presets
------------------

Importing ``plotfair.presets`` automatically configures matplotlib with
publication-quality defaults:

.. code-block:: python

   import plotfair.presets

   # Now matplotlib is configured with:
   # - Higher DPI (150)
   # - Larger font sizes
   # - Clean spine styling
   # - Transparent backgrounds

Enhanced Figure Saving
^^^^^^^^^^^^^^^^^^^^^^

The presets module patches ``plt.savefig`` to automatically save to a ``figs/`` folder:

.. code-block:: python

   import matplotlib.pyplot as plt
   import plotfair.presets

   plt.plot([1, 2, 3], [1, 4, 9])
   plt.savefig('my_figure.png')  # Saves to figs/my_figure.png

Control saving with the ``SAVE_FIGS`` flag:

.. code-block:: python

   import plotfair.presets as presets
   presets.SAVE_FIGS = False  # Disable automatic saving

Plotly Wrapper (Plty)
---------------------

The ``Plty`` class provides a matplotlib-like interface for Plotly:

.. code-block:: python

   from plotfair import Plty
   import numpy as np

   plty = Plty()

   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Plot like matplotlib
   plty.plot(x, y, label='sin(x)')
   plty.xlabel('x')
   plty.ylabel('y')
   plty.title('Sine Wave')
   plty.show()

Available methods:

- ``plot(x, y, label=None, color=None)`` - Line plots
- ``hist(data, bins=50)`` - Histograms
- ``xlim(xmin, xmax)`` / ``ylim(ymin, ymax)`` - Axis limits
- ``xlabel(label)`` / ``ylabel(label)`` / ``title(label)`` - Labels
- ``loglog()`` / ``linear()`` - Scale switching
- ``show()`` - Display and reset figure
- ``save_to_clipboard()`` - Copy figure as PNG (experimental)

Plotly Templates
^^^^^^^^^^^^^^^^

Combine Plotly templates with plotfair's custom templates:

.. code-block:: python

   from plotfair.plt_y import plty, pio

   # Available templates: 'pridepy', 'loglog'
   pio.templates.default = 'plotly_white+presentation+pridepy'

   # For log-log plots
   pio.templates.default = 'plotly_dark+presentation+pridepy+loglog'

Interplot Integration
---------------------

The ``Iplt`` class wraps interplot with matplotlib-like syntax:

.. code-block:: python

   from plotfair import Iplt
   import numpy as np

   iplt = Iplt()

   x = np.linspace(0, 10, 100)
   y = np.sin(x)

   # Matplotlib-style format strings
   iplt.plot(x, y, 'ro-', label='Data')
   iplt.show()

Configure interplot settings:

.. code-block:: python

   from interplot import iplot
   import plotfair as pf

   # Set color cycle (list of hex colors)
   iplot.conf.COLOR_CYCLE = pf.paintkit_to_colorway(pf.paintkit.filter(tags={'bright'}))

   # Set interactivity mode
   iplot.conf.INTERACTIVE = False  # Matplotlib backend
   iplot.conf.INTERACTIVE = True   # Plotly backend

Complete Setup Example
----------------------

A typical setup for consistent plotting across your project:

.. code-block:: python

   import plotfair as pf
   import matplotlib as mpl
   from plotfair.plt_y import plty, pio

   # Configure color scheme
   scheme = pf.paintkit.filter(tags={'bright'}).ordered_swatches(pf.tab10)

   # Set matplotlib defaults
   mpl.rcParams['axes.prop_cycle'] = scheme.to_cycler()

   # Set plotly defaults
   plotly_colors = pf.paintkit_to_colorway(scheme)
   pio.templates['pridepy'].layout.colorway = plotly_colors
   pio.templates.default = 'plotly_white+presentation+pridepy'

   # Now all your plots will use consistent colors