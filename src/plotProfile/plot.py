import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from scipy.signal import argrelextrema
import numpy as np
import colorsys


def desaturate(color, factor=1.2):
    rgb = mpc.to_rgb(color)
    hls = colorsys.rgb_to_hls(*rgb)
    hls_new = (hls[0], 1 - (0.4 * factor), 0.3 * factor)
    return colorsys.hls_to_rgb(*hls_new)


def generate_coordinates(energies):
    x_coords, y_coords = [], []
    i = 0
    while i < len(energies):
        x_coords.append(i)
        y_coords.append(energies[i])
        j = i + 1
        while j < len(energies) and energies[j] == energies[i]:
            j += 1
        if j - i > 1:
            midpoint = (x_coords[-1] + j - 1) / 2
            x_coords[-1] = midpoint
            y_coords[-1] = energies[i]
            x_coords.append(midpoint)
            y_coords.append(energies[i])
        i = j
    return x_coords, y_coords


def plot_profile(
    energy_sets,
    filename='reaction_profile',
    file_format='eps',
    curviness=0.42,
    point_type='dot',
    desaturate_factor=1.2,
    desaturate_curve=False,
    labels=True,
    dashed=None,
    colors=None,
    dpi=600
):
    dashed = dashed or []

    all_coords = [generate_coordinates(energies) for energies in energy_sets]
    bar_length, bar_width = 0.3, 2.5

    all_energies = [e for xs, ys in all_coords for e in ys if not np.isnan(e)]
    buffer_space = 0.025 * (max(all_energies) - min(all_energies))
    buffer_range = 1.0
    curve_width = 2.0

    default_colors = ['darkcyan', 'maroon', 'midnightblue', 'darkmagenta', 'darkgreen', 'saddlebrown']
    colors = (colors or default_colors[:len(energy_sets)])[::-1]
    light_colors = [desaturate(c, desaturate_factor) for c in colors]

    energy_sets = list(reversed(all_coords))
    dashed = [len(energy_sets) - i - 1 for i in dashed]
    labeled_coords = set()

    fig, ax = plt.subplots(figsize=(8, 4))

    # --- draw curves
    for i, (x, y) in enumerate(energy_sets):
        linestyle = 'dashed' if i in dashed else 'solid'
        verts, codes = [], [Path.MOVETO]

        for j in range(len(y) - 1):
            if not np.isnan(y[j]) and not np.isnan(y[j + 1]):
                verts.append([x[j], y[j]])
                verts.append([x[j] + curviness * (x[j + 1] - x[j]), y[j]])
                verts.append([x[j + 1] - curviness * (x[j + 1] - x[j]), y[j + 1]])
                verts.append([x[j + 1], y[j + 1]])
                if j != len(y) - 2:
                    codes += [Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.MOVETO]
                else:
                    codes += [Path.CURVE4, Path.CURVE4, Path.CURVE4]

        path = Path(verts, codes)
        patch = PathPatch(path, facecolor='none',
                          edgecolor=light_colors[i] if desaturate_curve else colors[i],
                          linewidth=curve_width, linestyle=linestyle)
        ax.add_patch(patch)

    # --- draw points
    for i, (x, y) in enumerate(energy_sets):
        for j, energy in enumerate(y):
            if np.isnan(energy): continue
            if point_type == 'bar':
                ax.plot([x[j] - bar_length / 2, x[j] + bar_length / 2], [energy, energy], color='black', lw=bar_width)
            elif point_type == 'dot':
                ax.plot(x[j], energy, 'o', markersize=5, color=colors[i])

    # --- draw labels
    if labels:
        for i, (x, y) in enumerate(energy_sets):
            local_maxima = argrelextrema(np.array(y), np.greater)[0]
            for j, energy in enumerate(y):
                if np.isnan(energy): continue
                coord_key = (x[j], energy)
                if coord_key not in labeled_coords:
                    label_above = any(abs(lbl[1] - energy) <= buffer_range for lbl in labeled_coords if lbl[1] > energy)
                    label_below = any(abs(lbl[1] - energy) <= buffer_range for lbl in labeled_coords if lbl[1] < energy)
                    is_max = j in local_maxima

                    if is_max:
                        if label_above:
                            label_pos = energy - buffer_space
                            valign = 'top'
                        else:
                            label_pos = energy + buffer_space
                            valign = 'bottom'
                    else:
                        label_pos = energy - buffer_space
                        valign = 'top'

                    ax.annotate(f"{energy:.1f}".replace('-', '−'), xy=(x[j], label_pos),
                                xytext=(0, buffer_space if valign == 'bottom' else -buffer_space),
                                textcoords='offset points', ha='center', va=valign, fontsize=10)
                    labeled_coords.add(coord_key)

    # --- final touches
    ax.set_ylabel(r'$\Delta G \text{ (kcal/mol)}$', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(f"{filename}.{file_format}", format=file_format, dpi=dpi, bbox_inches='tight')
    return fig

