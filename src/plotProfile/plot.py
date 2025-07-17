import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from matplotlib.path import Path 
from matplotlib.lines import Line2D
import seaborn as sns
from scipy.signal import argrelextrema
import numpy as np
from itertools import cycle
import math
from matplotlib.patches import Circle
from matplotlib.transforms import Bbox

import colorsys
import json
from pathlib import Path as PathPath
from adjustText import adjust_text

STYLE_PATH = PathPath(__file__).parent / "styles.json"

from matplotlib.font_manager import FontProperties


def _load_style(style_name):
    with open(STYLE_PATH, 'r') as f:
        styles = json.load(f)
    base = styles.get("default", {})
    overlay = styles.get(style_name, {})
    base.update(overlay)
    return base

def desaturate_colour(color, factor=1.2):
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

def cubic_bezier_points(P0, P1, P2, P3, num=500):
    t = np.linspace(0, 1, num)
    points = ((1 - t)**3)[:, None] * P0 + \
            3 * ((1 - t)**2)[:, None] * t[:, None] * P1 + \
            3 * (1 - t)[:, None] * (t**2)[:, None] * P2 + \
            (t**3)[:, None] * P3
    return points

class ReactionProfilePlotter:
    def __init__(self, style='default', **kwargs):
        style_dict = _load_style(style)
        style_dict.update(kwargs)

        self.figsize = tuple(style_dict['figsize'])
        self.point_type = style_dict["point_type"]
        self.curviness = style_dict["curviness"]
        self.desaturate = style_dict["desaturate"]
        self.desaturate_factor = style_dict["desaturate_factor"]
        self.dashed = style_dict["dashed"]
        self.labels = style_dict["labels"]
        self.show_legend = style_dict["show_legend"]
        self.line_width = style_dict["line_width"]
        self.bar_width = style_dict["bar_width"]
        self.marker_size = style_dict["marker_size"]
        self.font_size = style_dict["font_size"]
        self.font_kwargs = {
            'fontsize': style_dict.get('font_size', 10),
        }
        self.font_properties = self._get_font_properties(style_dict)
        self.axes = style_dict["axes"]
        self.axis_linewidth = style_dict["axis_linewidth"]
        self.colors = style_dict.get("colors", 'viridis')
        self.arrow_color = style_dict["arrow_color"]
        self.annotation_color = style_dict["annotation_color"]
        self.segment_annotations = style_dict["segment_annotations"]
        self.buffer_factor = style_dict.get("buffer_factor", 0.025)
        self.energy = style_dict.get("energy", "G")
        self.units = style_dict.get("units", "kcal")
        self.annotation_kwargs = {
            'fontsize': style_dict.get('annotation_size', self.font_size),
            'fontfamily': style_dict.get('font_family', 'sans-serif'),
            'fontweight': style_dict.get('annotation_weight', 'semibold'),
            'fontstyle': style_dict.get('annotation_style', 'italic'),
        }
    def _get_font_properties(self, font_dict):
        return FontProperties(
            family=font_dict.get('font_family', 'sans-serif'),
            weight=font_dict.get('font_weight', 'normal'),
            style=font_dict.get('font_style', 'normal'),
            size=font_dict.get('font_size', 10),
        )

    def _resolve_colors(self, setting, num_colors):
        if isinstance(setting, str):
            try:
                return sns.color_palette(setting, num_colors)
            except ValueError:
                try:
                    cmap = plt.get_cmap(setting)
                    return [cmap(i / num_colors) for i in range(num_colors)]
                except ValueError:
                    raise ValueError(f"Invalid color palette name: '{setting}'")
        
        elif isinstance(setting, list):
            if len(setting) < num_colors:
                raise ValueError(
                    f"Color list has only {len(setting)} colors but {num_colors} are needed. "
                    f"Provide a longer list or use a colormap name like 'viridis'."
                )
            return setting[:num_colors]

        elif hasattr(setting, "__call__"):  # matplotlib colormap object
            return [setting(i / num_colors) for i in range(num_colors)]

        else:
            raise TypeError("`colors` must be a palette name (str), colormap object, or list of color codes.")

    def plot(self, energy_dict, filename=None, file_format='png', dpi=600, include_keys=None):
        if include_keys is not None:
            energy_dict = {k: v for k, v in energy_dict.items() if k in include_keys}
        labels = list(energy_dict.keys())
        energy_sets = [  # convert None to np.nan
            [e if e is not None else np.nan for e in energy_dict[k]]
            for k in labels
        ]
        dashed_indices = [labels.index(k) for k in self.dashed if k in labels]

        coords = [generate_coordinates(e) for e in energy_sets]
        all_energies = [e for xs, ys in coords for e in ys if not np.isnan(e)]
        buffer_space = self.buffer_factor * (max(all_energies) - min(all_energies))
        buffer_range = 1.0

        base_colors = self.colors
        colors = self._resolve_colors(base_colors, len(energy_sets))
        colors = colors[::-1]

        light_colors = [desaturate_colour(c, self.desaturate_factor) for c in colors] if self.desaturate else colors

        fig, ax = plt.subplots(figsize=self.figsize)
        labeled_coords = set()
        if self.labels:
            ax.margins(x=0.08, y=0.1)  # Add to avoid label overlap with edge of plot

        # --- draw curves
        for i, (x, y) in enumerate(reversed(coords)):
            linestyle = 'dashed' if i in [len(coords) - 1 - d for d in dashed_indices] else 'solid'
            verts, codes = [], [Path.MOVETO]

            for j in range(len(y) - 1):
                if np.isnan(y[j]) or np.isnan(y[j + 1]):
                    continue
                if not verts:
                    verts.append([x[j], y[j]])
                    # codes = [Path.MOVETO]
                verts.append([x[j] + self.curviness * (x[j + 1] - x[j]), y[j]])
                verts.append([x[j + 1] - self.curviness * (x[j + 1] - x[j]), y[j + 1]])
                verts.append([x[j + 1], y[j + 1]])
                codes += [Path.CURVE4, Path.CURVE4, Path.CURVE4]

            path = Path(verts, codes)
            label = labels[len(coords) - 1 - i]
            
            verts = np.array(verts)
            all_points = []
            for j in range(0, len(verts) - 3, 3):
                P0 = verts[j]
                P1 = verts[j + 1]
                P2 = verts[j + 2]
                P3 = verts[j + 3]
                bezier_points = cubic_bezier_points(P0, P1, P2, P3)
                all_points.append(bezier_points)
            all_points = np.vstack(all_points)
            ax.plot(all_points[:, 0], all_points[:, 1], color=light_colors[i], linewidth=self.line_width, linestyle=linestyle, dash_capstyle='round')

            legend_line = Line2D(
                [0], [0],
                color=light_colors[i],
                linewidth=self.line_width,
                linestyle=linestyle,
                label=label,
                dash_capstyle='round'
            )
            ax.add_line(legend_line)

        # --- draw points
        for i, (x, y) in enumerate(reversed(coords)):
            for j, energy in enumerate(y):
                if np.isnan(energy):
                    continue
                if self.point_type == 'bar':
                    ax.plot([x[j] - 0.15, x[j] + 0.15], [energy, energy], color='black', lw=self.bar_width)
                elif self.point_type in ['dot', '.']:
                    ax.plot(x[j], energy, 'o', markersize=self.marker_size, color=colors[i])
                elif self.point_type in ['hollow', 'o']:
                    ax.plot(x[j], energy, marker='o', markerfacecolor='white', markeredgecolor=colors[i], markeredgewidth=self.line_width)


        if self.labels:
            label_coords = []
            label_vals = []
            labeled_set = set()
            curves = []
            texts = []

            # Sort points for local max detection
            sorted_points = sorted([(x, y) for coords_ in coords for x, y in zip(*coords_) if not np.isnan(y)], key=lambda p: p[0])
            x_group = {}
            for px, py in sorted_points:
                x_group.setdefault(round(px, 3), []).append(py)

            sorted_xs = sorted(set(round(px, 3) for px, _ in sorted_points))
            x_index_map = {xv: i for i, xv in enumerate(sorted_xs)}

            for x, energy in sorted_points:
                rx = round(x, 3)
                idx = x_index_map.get(rx, None)

                is_local_max = False
                if idx is not None and 0 < idx < len(sorted_xs) - 1:
                    prev_x = sorted_xs[idx - 1]
                    next_x = sorted_xs[idx + 1]
                    current_y = max(x_group[rx])
                    prev_y = max(x_group[prev_x])
                    next_y = max(x_group[next_x])
                    is_local_max = current_y > prev_y and current_y > next_y

                preferred_above = is_local_max
                preferred_y = energy + buffer_space if preferred_above else energy - buffer_space
                valign = 'bottom' if preferred_above else 'top'

                def find_parent_curve_index(x, y, coords):
                    for i, (xs, ys) in enumerate(coords):
                        for x0, y0 in zip(xs, ys):
                            if np.isclose(x, x0, atol=1e-5) and np.isclose(y, y0, atol=1e-3):
                                return i
                    return None

                # Find which curve this point belongs to
                parent_idx = find_parent_curve_index(x, energy, coords)
                if parent_idx is None:
                    continue

                # Get y-values from other curves at this x
                other_yvals = []
                for i, (xs, ys) in enumerate(coords):
                    if i == parent_idx:
                        continue
                    # Interpolate y at x
                    try:
                        y_interp = np.interp(x, xs, ys)
                        other_yvals.append(y_interp)
                    except Exception:
                        continue

                if other_yvals:
                    nearest_other_y = min(other_yvals, key=lambda y: abs(preferred_y - y))
                    dist_to_own_curve = abs(preferred_y - energy)
                    dist_to_other_curve = abs(preferred_y - nearest_other_y)

                    if dist_to_other_curve < dist_to_own_curve:
                        # Label is nearer another curve — flip placement
                        preferred_above = not preferred_above
                        preferred_y = energy + buffer_space if preferred_above else energy - buffer_space
                        valign = 'bottom' if preferred_above else 'top'

                # Proceed with label
                label_text = f"{energy:.1f}".replace('-', '−')
                label_key = (x, label_text)
                if label_key in labeled_set:
                    continue
                labeled_set.add(label_key)

                label_coords.append((x, preferred_y))
                label_vals.append(label_text)

                ax.annotate(
                    label_text,
                    xy=(x, preferred_y),
                    xytext=(0, buffer_space if valign == 'bottom' else -buffer_space),
                    textcoords='offset points',
                    ha='center',
                    va=valign,
                    fontproperties=self.font_properties,
                    fontweight='normal',
                )


        # --- legend
        if self.show_legend:
            handles, labels_ = ax.get_legend_handles_labels()
            # unique = dict(zip(labels, handles))  # Remove duplicates
            ax.legend(handles[::-1], labels_[::-1], loc='best', prop=self.font_properties)

        # --- segment annotations with double-headed arrows
        if self.segment_annotations:
            y_min, _ = ax.get_ylim()
            y_arrow = y_min - 0.00 * (max(all_energies) - min(all_energies))  # place below data
            for label, (x_start, x_end) in self.segment_annotations.items():
                color = self.arrow_color
                text_color = self.annotation_color

                # Draw double-headed arrow
                ax.annotate(
                    '', 
                    xy=(x_end, y_arrow), 
                    xytext=(x_start, y_arrow),
                    arrowprops=dict(
                        arrowstyle='<->',
                        color=self.arrow_color,
                        lw=self.line_width,
                        # ls='--',
                        shrinkA=0.5,
                        shrinkB=0.5,
                    ),
                    annotation_clip=False
                )

                x_center = (x_start + x_end) / 2
                ax.text(
                    x_center, y_arrow - 0.5,
                    label,
                    ha='center', va='top',
                    color=self.annotation_color,
                    **self.annotation_kwargs,
                )
            # only draw if there is no x-axis to be shown
            if self.axes in ['x', 'both', 'box']:
                y_min, y_max = ax.get_ylim()
                energy_range = max(all_energies) - min(all_energies)

                y_buffer = 0.08 * energy_range
                ax.set_ylim(y_min - y_buffer, y_max)

        if self.units.lower() == "kj":
            units = 'kJ/mol'
        else:
            units = 'kcal/mol'
        if self.energy.lower() == 'e' or self.energy.lower() == 'energy' or self.energy.lower() == 'electronic':
            energy = 'E'
        elif self.energy.lower() == 'h' or self.energy.lower() == 'enthalpy': 
            energy = 'H'
        elif self.energy.lower() == 's' or self.energy.lower() == 'entropy':
            energy = 'S'
        else:
            energy = 'G'
        ax.set_ylabel(f'Δ{energy} ({units})', fontproperties=self.font_properties)
        ax.set_xlabel('Reaction Coordinate', fontproperties=self.font_properties)

        # Hide all spines and ticks by default
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Remove all ticks and tick labels by default
        ax.tick_params(
            axis='x', which='both',
            bottom=False, top=False,
            labelbottom=False
        )
        ax.tick_params(
            axis='y', which='both',
            left=False, right=False,
            labelleft=False, labelright=False
        )

        if self.axes == 'x':
            ax.spines['bottom'].set_visible(True)
            ax.spines['bottom'].set_linewidth(self.axis_linewidth)
            ax.set_ylabel(None)

        elif self.axes == 'y':
            ax.spines['left'].set_visible(True)
            ax.spines['left'].set_linewidth(self.axis_linewidth)
            ax.set_xlabel(None)

            ax.tick_params(
                axis='y', which='both',
                left=True,
                labelleft=True,
                width=self.line_width,
                length=5,
                labelsize=self.font_size,
            )

            
        elif self.axes == 'both':
            ax.spines['bottom'].set_visible(True)
            ax.spines['left'].set_visible(True)
            ax.spines['bottom'].set_linewidth(self.axis_linewidth)
            ax.spines['left'].set_linewidth(self.axis_linewidth)

            ax.tick_params(
                axis='x', which='both',
                bottom=False,
                labelbottom=False
            )
            ax.tick_params(
                axis='y', which='both',
                left=True,
                labelleft=True,
                width=self.line_width,
                length=5,
                labelsize=self.font_size,
            )            


        elif self.axes == 'box':
            for spine_name in ['bottom', 'top', 'left', 'right']:
                ax.spines[spine_name].set_visible(True)
                ax.spines[spine_name].set_linewidth(self.axis_linewidth)

            ax.tick_params(
                axis='x', which='both',
                bottom=False,
                labelbottom=False
            )
            ax.tick_params(
                axis='y', which='both',
                left=True,
                labelleft=True,
                width=self.line_width,
                length=5,
                labelsize=self.font_size,
            )


        else:
            ax.set_xlabel(None)
            ax.set_ylabel(None)

        fig.tight_layout()

        if filename:
            fig.savefig(f"{filename}.{file_format}", format=file_format, dpi=dpi, bbox_inches='tight')

        return None


# Convenience function (no need to instantiate class)
def plot_reaction_profile(energy_dict, **kwargs):
    plotter = ReactionProfilePlotter()
    return plotter.plot(energy_dict, **kwargs)
