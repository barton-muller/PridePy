"""
PridePy.colors
Color utilities, swatch classes, color reading, colormap creation.
"""
import colorsys
import csv
import numpy as np
from matplotlib.colors import ListedColormap, to_rgb, LinearSegmentedColormap
from matplotlib import cycler
from colorspacious import cspace_convert
import matplotlib as mpl
import os

# --- ColorSwatch and PaintKit ---
def hex_to_rgb(hex_code):
    hex_clean = hex_code.lstrip("#")
    return tuple(int(hex_clean[i:i+2], 16)/255 for i in (0, 2, 4))
def floats_to_rgbstring(color_float):
    """Convert a float tuple to an RGB string for use by plotly
    form (0.0, 0.0, 0.0) to "rgb(0, 0, 0)"""
    return f"rgb({int(color_float[0]*255)}, {int(color_float[1]*255)}, {int(color_float[2]*255)})"

class ColorSwatch:
    def __init__(self, name, hex_code, tags=None):
        self.name = name
        self.hex = hex_code.upper()
        self.tags = set(tags) if tags else set()
        self.rgb = hex_to_rgb(self.hex)
        self.hsl = self._hex_to_hsl()

    def _hex_to_hsl(self):
        r, g, b = self.rgb
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h * 360, s, l

    def has_tag(self, tag):
        return tag in self.tags

    def __repr__(self):
        return f"ColorSwatch(name='{self.name}', hex='{self.hex}', tags={self.tags})"

class PaintKit:
    def __init__(self, colors):
        self.colors = colors
        self.color_tags = ['green','teal','lightblue', 'blue', 'purple', 'pink','fuchia', 'red', 'orange', 'yellow']
        self.saturation_tags = ['bright', 'dark', 'muted']

    def __add__(self, other):
        return PaintKit(self.colors + other.colors)
    def __len__(self):
        return len(self.colors)
    def __repr__(self):
        ret = ""
        for color in self.colors:
            ret += f"ColorSwatch(name='{color.name}', hex='{color.hex}', tags={color.tags}) \n"

        self.display_paintkit( label='name')
        return f"Collection of {len(self.colors)} colors"
    def filter(self, *, tags=None, any_tags=None):
        result = self.colors
        if any_tags:
            result = [c for c in result if c.tags & any_tags]
        if tags:
            result = [c for c in result if tags.issubset(c.tags)]
        return PaintKit(result)
    def get_named(self, *names):
        return [c for c in self.colors if c.name in names]
    def ordered_swatches(self, tag_list):
        swatches = []
        missing = []
        for tag in tag_list:
            filtered = self.filter(tags={tag}).colors
            if filtered:
                swatches.append(filtered[0])
            else:
                missing.append(tag)
        if missing:
            print(f"Missing tags: {missing}")
        return PaintKit(swatches)
    def to_cmap(self, colors=None, name="custom_cmap"):
        if colors is None:
            colors = self.colors
        return ListedColormap([c.hex for c in colors], name=name)
    def to_cycler(self, colors=None):
        if colors is None:
            colors = self.colors
        return cycler(color=[c.hex for c in colors])
    def display_paintkit(self, color_tags=None, saturation_tags=None, label='hex'):
        """
        Display a grid of swatches by color and saturation tags.
        """
        import matplotlib.pyplot as plt
        import numpy as np
        grid_rows = []
        label_rows = []
        included = set()
        if color_tags is None:
            color_tags = self.color_tags
        if saturation_tags is None:
            saturation_tags = sorted({
                tag for sw in self.colors
                for tag in sw.tags
                if tag in {'bright', 'dark', 'muted'}
            })

        for sat in saturation_tags:
            row_colors = []
            row_labels = []
            for col in color_tags:
                swatches = self.filter(tags={sat, col}).colors
                if swatches:
                    sw = swatches[0]
                    rgb = hex_to_rgb(sw.hex)
                    row_colors.append(rgb)
                    row_labels.append(sw.hex if label == 'hex' else sw.name)
                    included.update(swatches)
                else:
                    row_colors.append((1, 1, 1))
                    row_labels.append("")
            grid_rows.append(row_colors)
            label_rows.append(row_labels)

        grid = np.array(grid_rows)
        unmatched = [sw for sw in self.colors if sw not in included]
        if unmatched:
            n_cols = len(color_tags)*2
            n_rows = int(np.ceil(len(unmatched) / n_cols))
            grid_un = np.ones((n_rows, n_cols, 3))
        else:
            n_rows = 0

        fig, (ax_grid, ax_unmatched) = plt.subplots(
            2, 1,
            figsize=(len(color_tags) * 1.5, len(saturation_tags) * 1.2 + n_rows*1.2),
            height_ratios=[len(saturation_tags), n_rows/2 if n_rows else 0.5],
            constrained_layout=True
        )

        # --- Main Grid Plot ---
        ax_grid.imshow(grid, aspect='equal')

        for i, row in enumerate(label_rows):
            for j, text in enumerate(row):
                if text:
                    r, g, b = grid[i][j]
                    brightness = 0.299*r + 0.587*g + 0.114*b
                    text_color = 'black' if brightness > 0.6 else 'white'
                    ax_grid.text(j, i, text, ha='center', va='center',
                                color=text_color, fontsize=7, fontweight='bold')

        ax_grid.set_xticks(range(len(color_tags)))
        ax_grid.set_xticklabels(color_tags, fontsize=10, rotation=45, ha='right')
        ax_grid.set_yticks(range(len(saturation_tags)))
        ax_grid.set_yticklabels(saturation_tags, fontsize=10)
        ax_grid.set_title("Color Tag (X) vs Saturation Tag (Y)", fontsize=12)

        # --- Unmatched Swatches Plot ---
        ax_unmatched.axis('off')
        if unmatched:
            label_un = [["" for _ in range(n_cols)] for _ in range(n_rows)]
            for idx, sw in enumerate(unmatched):
                r, c = divmod(idx, n_cols)
                grid_un[r, c] = hex_to_rgb(sw.hex)
                label_un[r][c] = sw.hex if label == 'hex' else sw.name
            ax_unmatched.imshow(grid_un, aspect='equal')
            for r in range(n_rows):
                for c in range(n_cols):
                    text = label_un[r][c]
                    if text:
                        r_val, g_val, b_val = grid_un[r][c]
                        brightness = 0.299 * r_val + 0.587 * g_val + 0.114 * b_val
                        text_color = 'black' if brightness > 0.6 else 'white'
                        ax_unmatched.text(c, r, text, ha='center', va='center',
                                        color=text_color, fontsize=6, fontweight='bold')
            ax_unmatched.set_title("Unmatched Swatches", fontsize=12)
        plt.show()

def read_colors_from_csv(filename):
    swatches = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tags = set(t.strip() for t in row['tags'].split(';') if t.strip())
            swatches.append(ColorSwatch(name=row['name'], hex_code=row['hex_code'], tags=tags))
    return swatches

# --- Colormap creation ---
def perceptual_colormap_nonuniform(colors, positions=None, n=256, space="CAM02-UCS"):
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

def paintkit_to_colorway(paintkit):
    colorway = [c['color'] for c in paintkit.to_cycler()._left]
    return colorway

# --- Build paintkit from CSV and set mpl color cycle ---
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'colorsheet.csv')
    color_swatches = read_colors_from_csv(csv_path)
    paintkit = PaintKit(color_swatches)
    use_paintkit = True
except FileNotFoundError:
    print("colorsheet.csv not found in PridePy directory.")
    use_paintkit = False

if use_paintkit:
    rainbow = ['green','lightblue', 'blue', 'purple', 'pink','fuchia', 'orange']
    full_rainbow = ['green','teal','lightblue', 'blue', 'purple', 'pink','fuchia', 'red', 'orange', 'yellow']
    tab10 = ['blue', 'orange', 'green', 'pink', 'purple', 'lightblue', 'fuchia','yellow', 'teal', 'red']
    bright_tab10 = paintkit.filter(tags={'bright'}).ordered_swatches(tab10)
    mpl.rcParams['axes.prop_cycle'] = bright_tab10.to_cycler()
    scheme = paintkit.filter(tags={'bright'}).ordered_swatches(tab10)
    mpl.rcParams['axes.prop_cycle'] = scheme.to_cycler()  # set default color cycle
    plotly_scheme = paintkit_to_colorway(scheme)
