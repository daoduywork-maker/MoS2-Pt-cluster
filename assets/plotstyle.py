"""Shared figure style for Project-2: same font, sizes and colours in every figure."""
import matplotlib as mpl

D3, PBE = "#2a78d6", "#eb6834"          # series colours: PBE+D3, plain PBE
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#d9d8d2"

def apply():
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
        "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
        "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.6,
        "savefig.dpi": 300, "savefig.bbox": "tight", "figure.dpi": 150,
    })
