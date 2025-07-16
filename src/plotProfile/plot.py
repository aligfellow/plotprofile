import matplotlib.pyplot as plt
import matplotlib.colors as mpc
from matplotlib.path import Path 
from scipy.signal import argrelextrema
import numpy as np
from itertools import cycle
import colorsys
import json
from pathlib import Path as PathPath

STYLE_PATH = PathPath(__file__).parent / "styles.json"

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
        self.axes = style_dict["axes"]
        self.axis_linewidth = style_dict["axis_linewidth"]
        self.colors = style_dict["colors"]
        self.arrow_color = style_dict["arrow_color"]
        self.annotation_color = style_dict["annotation_color"]
        self.segment_annotations = style_dict["segment_annotations"]

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
        buffer_space = 0.025 * (max(all_energies) - min(all_energies))
        buffer_range = 1.0

        base_colors = self.colors
        colors = (self.colors[:len(energy_sets)])[::-1]

        if len(base_colors) < len(energy_sets):
            num_needed = len(energy_sets) - len(base_colors)
            fallback_cmap = plt.cm.get_cmap('Dark2')
            fallback_colors = [fallback_cmap(i) for i in range(fallback_cmap.N)]
            color_cycle = cycle(fallback_colors)
            colors = list(base_colors) + [next(color_cycle) for _ in range(len(energy_sets) - len(base_colors))]



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

            # from matplotlib.patches import Path
            # patch = PathPatch(path, facecolor='none', edgecolor=light_colors[i], linewidth=self.line_width, linestyle=linestyle, dash_capstyle='round')
            # ax.add_patch(patch)
            
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


            from matplotlib.lines import Line2D
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

        # --- draw labels
        if self.labels:
            for i, (x, y) in enumerate(reversed(coords)):
                local_maxima = argrelextrema(np.array(y), np.greater)[0]
                for j, energy in enumerate(y):
                    if np.isnan(energy):
                        continue
                    coord_key = (x[j], energy)
                    if coord_key not in labeled_coords:
                        label_above = any(abs(lbl[1] - energy) <= buffer_range for lbl in labeled_coords if lbl[1] > energy)
                        label_below = any(abs(lbl[1] - energy) <= buffer_range for lbl in labeled_coords if lbl[1] < energy)
                        is_max = j in local_maxima

                        if is_max:
                            label_pos = energy + buffer_space if not label_above else energy - buffer_space
                            valign = 'bottom' if not label_above else 'top'
                        else:
                            label_pos = energy - buffer_space
                            valign = 'top'

                        ax.annotate(f"{energy:.1f}".replace('-', '−'), xy=(x[j], label_pos),
                                    xytext=(0, buffer_space if valign == 'bottom' else -buffer_space),
                                    textcoords='offset points', ha='center', va=valign, fontsize=self.font_size)
                        labeled_coords.add(coord_key)

        # --- legend
        if self.show_legend:
            handles, labels_ = ax.get_legend_handles_labels()
            # unique = dict(zip(labels, handles))  # Remove duplicates
            ax.legend(handles[::-1], labels_[::-1], loc='best', fontsize=self.font_size)

        # --- segment annotations with double-headed arrows
        if self.segment_annotations:
            # only draw if there is no x-axis to be shown
            if self.axes in ['x', 'both', 'box']:
                pass
            else:
                y_min, _ = ax.get_ylim()
                y_arrow = y_min - 0.00 * (max(all_energies) - min(all_energies))  # place below data
                for seg in self.segment_annotations:
                    x_start, x_end = seg['start'], seg['end']
                    label = seg.get('label', '')
                    color = seg.get('color', 'black')
                    text_color = seg.get('text_color', 'crimson')

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
                            shrinkA=2,
                            shrinkB=2,
                        ),
                        annotation_clip=False
                    )

                    # Draw label centered under arrow
                    x_center = (x_start + x_end) / 2
                    ax.text(
                        x_center, y_arrow - 0.5,
                        label,
                        ha='center', va='top',
                        fontsize=self.font_size,
                        color=self.annotation_color,
                        fontweight='semibold', 
                        fontstyle='italic'
                    )

        ax.set_ylabel(r'$\Delta G \text{ (kcal/mol)}$', fontsize=self.font_size)
        ax.set_xlabel('Reaction Coordinate', fontsize=self.font_size)

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
