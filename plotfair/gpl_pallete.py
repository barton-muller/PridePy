import csv
import os


def make_gpl_palette(
    csv_path=None,
    output_path=None,
    palette_name="plotfair",
    columns=1,
):
    """Create a GIMP/Inkscape .gpl color palette file from a CSV.

    Args:
        csv_path: Path to CSV with 'hex_code', 'name', and 'tags' columns.
            Defaults to colorsheet.csv next to this script.
        output_path: Where to save the .gpl file.
            Defaults to plotfair.gpl next to this script.
        palette_name: Name shown in the palette picker.
        columns: Number of columns to display in the palette swatch grid.

    Returns:
        Path to the generated .gpl file.
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "colorsheet.csv")

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "plotfair.gpl")

    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    lines = [
        "GIMP Palette",
        f"Name: {palette_name}",
        f"Columns: {columns}",
        "#",
    ]

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            r, g, b = hex_to_rgb(row["hex_code"])
            lines.append(f"{r:3d} {g:3d} {b:3d}    {row['name']}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return output_path


if __name__ == "__main__":
    make_gpl_palette()
