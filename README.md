# PridePy

A package for default matplotlib settings that are better for including in posters/presentations/reports as well as providing a better set of colours which can be used to make nice qualitative colourmaps as well as gradients.
  
  <img src="https://github.com/user-attachments/assets/5b459000-0cc4-44ab-b634-b683cdd4bf7f" height="350" />
  <img src="https://github.com/user-attachments/assets/23035b7b-6f01-41da-9a44-3d7c8fa495f4" height="350" />

## Features
### Paintkit
- Custom color swatches and palettes
- Perceptually uniform and sRGB colormap creation
### matplotlib addons
- Default plotting presets for publication-quality figures
- Plotting wrappers for curve fitting and more
### Plotly addons
- matplotlib Plotly wrapper e.g. use plty.plot instead of plt.plot
- Plotly templates

## Installation
```bash
pip install .
```
Or build a wheel and install:
```bash
python setup.py sdist bdist_wheel
pip install dist/PridePy-*.whl
```

## Paintkit Usage Example
```python
import PridePy as pp
import matplotlib.pyplot as plt
import numpy as np

# Use a custom color cycle
ax.set_prop_cycle((pp.paintkit.filter(tags={'dark'})).ordered_swatches(pp.full_rainbow).to_cycler())
```
options for colour schemes include
for saturation: bright, dark, muted
for color schemes: rainbow, full_rainbow, tab10
```python 
# color schemes
rainbow = ['green','lightblue', 'blue', 'purple', 'pink','fuchia', 'orange']
full_rainbow = ['green','teal','lightblue', 'blue', 'purple', 'pink','fuchia', 'red', 'orange', 'yellow']
tab10 = ['blue', 'orange', 'green', 'pink', 'purple', 'lightblue', 'fuchia','yellow', 'teal', 'red']

#use this to set default color cycle
bright_tab10 = pp.paintkit.filter(tags={'dark'}).ordered_swatches(pp.full_rainbow) #change these to get scheme of choice
pp.mpl.rcParams['axes.prop_cycle'] = bright_tab10.to_cycler() 
```

```python
# Use a perceptual colormap
colors = [swatch.hex for swatch in pp.colors.paintkit.ordered_swatches(['blue','pink','orange']).colors]
positions = [0.0, 0.5, 1.0]
cmap = pp.colormaps.perceptual_colormap_nonuniform(colors, positions)
pp.colormaps.show_colormap(cmap, name='Perceptual Colormap')
```
Can also be used for better figure saving by setting `SAVEFIG = True` saving to default figs folder:
```python
def savefig_with_folder(fname, *args, folder="figs", **kwargs):
    if SAVE_FIGS:
        if not os.path.isabs(fname):
            os.makedirs(folder, exist_ok=True)
            fname = os.path.join(folder, fname)
        return _original_savefig(fname, *args, **kwargs)
    else:
        print('Currently not saving figures')

plt.savefig = savefig_with_folder
```

## matplotlib addons usage
Given this is not a common package I use condittional import allowing code to be run without PridePy.
After importing one can set default colorscheme and template for plots.
The `pp.paintkit.filter(tags={'bright'}).ordered_swatches(pp.tab10)` is the default color cycle.

```python
try:
    import pridepy as pp # type: ignore
    from pridepy.plt_y import plty  # type: ignore # mpl-like plotly wrapper

    #update colorscheme and default template
    pp.scheme = pp.paintkit.filter(tags={'bright'}).ordered_swatches(pp.tab10)
    pp.mpl.rcParams['axes.prop_cycle'] = pp.scheme.to_cycler()  # set default color cycle
    pp.plotly_scheme = pp.paintkit_to_colorway(pp.scheme)
    pp.plt_y.pio.templates['pridepy'].layout.colorway = pp.plotly_scheme 
    pp.plt_y.pio.templates.default = 'plotly_dark+presentation+pridepy+loglog'

    plty = pp.plt_y.Plty() #update wrapper for new presets

except ImportError as e:
    print(f"{e}. Proceeding with default plots")
    print(" Can be installed with \"pip install git+https://github.com/barton-muller/PridePy.git\"")
```

## Plotly addons usage
I initialise plotly in the code above aswell. Setting the color scheme and template.
Plotly templates can be combined with `+` very nicely. The default is `'plotly_white+presentation+pridepy'`
The plotly templates can be found [here](https://plotly.com/python/templates/).
The main ones of interest are `plotly`=default, `plotly_dark`=dark mode, and `plotly_white`=for publications
My template addons are `loglog` and `pridepy` which are defined in `plt_y.py`
The colorsceme needs to be set in the colorway attribute of the layout.

Theres a class Plty which I make an instance of called plty. A Ploty figure is stored at plty.fig for direct interaction with plotly but then I've added some functions to make plotly it easier to use.
- `plot(x, y)` and `plot(y)` for line plots with label argument same as plt.plot
- `hist(data, bins=50)` for histograms
- `xlim(xmin, xmax)` and `ylim(ymin, ymax)` for axis limits  
- `save_to_clipboard()` is experiemntal function to copy figures as PNGs. very useful for my notebook although it uses a custom script - see docstring
- `show()` to show figure and restet figure to empty `plty.fig = go.Figure()` and `show_()` to clear figure without showing
- if you dont run show you will build up traces on your plot with repeated runs

```python
from pridepy.plt_y import plty
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plty.plot(x, y, color='blue', label='sin(x)')
# set titiles and size. can also use nondefault template here
plty.fig.update_layout(
    # template='plotly_white+presentation+pridepy+loglog',
    width=800, height=400,
    title='Dwell Time Distribution', xaxis_title='First Passage Time', yaxis_title='Probability Density')
plty.show() #show figure and then clear it
```
## Flexoki colors
[flexoki colors](https://stephango.com/flexoki) by stephango
> Flexoki is an inky color scheme for prose and code. Flexoki is designed for reading and writing on digital screens. It is inspired by analog inks and warm shades of paper.
> Flexoki is minimalistic and high-contrast. The colors are calibrated for legibility and perceptual balance across devices and when switching between light and dark modes.
> Flexoki is open-source under the MIT license. Flexoki is available for dozens of popular apps, including Obsidian using my theme Minimal.

This is very simmilar what I'm trying to do so I've added it to PridePy.
The colors are available under the tag `flexoki` and theres `muted` and `dark` versions. They work with orderings of `tab10` and `full_rainbow` or `flexoki` which is same as rainbow but starts at blue
Flexoki color scheme © Stephen Ango, licensed under the MIT License. Used with attribution.

Theres a whole pallete of different shaded colors which I could acsess through[flexoki-py](https://github.com/moss-xyz/flexoki-py) which has simmilar color pallete abilities and can add itself to mpl colour list.


## TODO

- [ ] More color schemes i.e. customise rainbow to dark to include teal
- [ ] Find missing colors and make red region more distinct
- [ ] purple and pink are not distinct enough in tab10 bright
- [x] look at [flexoki colors](https://stephango.com/flexoki) which is what i was trying to make
- [ ] Sperate setting for poster/pres/report that can be invoked separately
- [ ] Clipping to 0 automatically
- [ ] Include some of the old wrappers again
- [ ] Default colormaps?
- [ ] Expand plty wrapper to include more plotly functions

## Documentation
See docstrings in each module for details on classes and functions.

## Useful websites

- [OKLCH Color Picker](https://oklch.com/)
- [iwanthue – Distinct Color Generator](https://medialab.github.io/iwanthue/)
- [Coolors – Color Schemes Generator](https://coolors.co/)
- [Palettable – Color Palettes in Python](https://jiffyclub.github.io/palettable/)
- [flexoki colors](https://stephango.com/flexoki)
