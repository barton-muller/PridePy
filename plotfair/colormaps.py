"""
PridePy.colormaps
Colormap creation utilities for perceptual and sRGB gradients.
"""
import numpy as np
from matplotlib.colors import ListedColormap, to_rgb, LinearSegmentedColormap
from colorspacious import cspace_convert

def perceptual_colormap_nonuniform(colors, positions=None, n=256, space="CAM02-UCS"):
    """
    Generate a perceptually uniform colormap between fixed color anchors at nonuniform positions.
    """
    num_colors = len(colors)
    if positions is None:
        positions = np.linspace(0.0, 1.0, num_colors)
    else:
        assert len(colors) == len(positions)
        assert positions[0] == 0.0 and positions[-1] == 1.0
    rgb_colors = np.array([to_rgb(c) for c in colors])
    perceptual_colors = cspace_convert(rgb_colors, "sRGB1", space)
    steps = np.linspace(0, 1, n)
    interpolated = []
    for idx in range(len(positions) - 1):
        start_pos = positions[idx]
        end_pos = positions[idx + 1]
        start_col = perceptual_colors[idx]
        end_col = perceptual_colors[idx + 1]
        segment_mask = (steps >= start_pos) & (steps <= end_pos)
        local_t = (steps[segment_mask] - start_pos) / (end_pos - start_pos)
        for t in local_t:
            interpolated.append((1 - t) * start_col + t * end_col)
    interpolated = np.array(interpolated)
    rgb_interp = cspace_convert(interpolated, space, "sRGB1")
    rgb_interp = np.clip(rgb_interp, 0, 1)
    return ListedColormap(rgb_interp, name="perceptual_nonuniform")

def srgb_gradient_colormap(colors, positions=None, n=256, name="srgb_colormap"):
    """
    Create a linear sRGB gradient colormap from anchor colors.
    """
    rgb_colors = [to_rgb(c) for c in colors]
    if positions is not None:
        assert len(positions) == len(rgb_colors)
        assert positions[0] == 0.0 and positions[-1] == 1.0
        return LinearSegmentedColormap.from_list(name, list(zip(positions, rgb_colors)), N=n)
    else:
        return LinearSegmentedColormap.from_list(name, rgb_colors, N=n)

def show_colormap(cmap, name=None, height=0.5):
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, height))
    ax.imshow(gradient, aspect='auto', cmap=cmap)
    ax.set_axis_off()
    if name:
        ax.set_title(name, fontsize=10)
    plt.show()
