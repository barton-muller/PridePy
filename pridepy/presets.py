"""
PridePy.presets
Default plotting settings and savefig wrapper.
"""
import matplotlib as mpl
import seaborn as sns
import os
import matplotlib.pyplot as plt

SAVE_FIGS = True

# Seaborn base style
sns.set_style("white")

# Update rcParams
mpl.rcParams.update({
    'figure.figsize': (6, 4),
    'figure.dpi': 150,
    'figure.facecolor': 'white',
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'axes.labelweight': 'bold',
    'axes.linewidth': 1.2,
    'axes.edgecolor': 'black',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'xtick.minor.size': 3,
    'ytick.minor.size': 3,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'xtick.minor.width': 0.8,
    'ytick.minor.width': 0.8,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'xtick.minor.visible': False,
    'ytick.minor.visible': False,
    'lines.linewidth': 2.0,
    'lines.markersize': 6,
    'lines.markeredgewidth': 0.8,
    'font.size': 12,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
    'legend.fontsize': 12,
    'legend.frameon': False,
    'legend.loc': 'best',
    'savefig.dpi': 600,
    'savefig.bbox': 'tight',
    'savefig.transparent': True,
    'image.cmap': 'plasma',
    "errorbar.capsize" : 2.0,
})

sns.set_style("white", {
    "axes.spines.right": False,
    "axes.spines.top": False,
    "xtick.bottom": True,
    "ytick.left": True
})

_original_savefig = plt.savefig

def savefig_with_folder(fname, *args, folder="figs", **kwargs):
    if SAVE_FIGS:
        if not os.path.isabs(fname):
            os.makedirs(folder, exist_ok=True)
            fname = os.path.join(folder, fname)
        return _original_savefig(fname, *args, **kwargs)
    else:
        print('Currently not saving figures')

plt.savefig = savefig_with_folder
