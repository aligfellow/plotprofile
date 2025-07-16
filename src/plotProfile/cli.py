import argparse
import numpy as np
import json
from .plot import plot_profile


def main():
    parser = argparse.ArgumentParser(description="Plot reaction profile from energy data")
    parser.add_argument('--input', type=str, required=True, help='Path to JSON file containing energy sets')
    parser.add_argument('--output', type=str, default='reaction_profile', help='Output filename (no extension)')
    parser.add_argument('--format', type=str, default='png', choices=['eps', 'png', 'svg', 'pdf'])
    parser.add_argument('--point-type', type=str, default='dot', choices=['bar', 'dot'])
    parser.add_argument('--curviness', type=float, default=0.42)
    parser.add_argument('--labels', action='store_true')
    parser.add_argument('--desaturate-curve', action='store_true')
    parser.add_argument('--desaturate-factor', type=float, default=1.2)
    parser.add_argument('--dashed', nargs='*', type=int, default=[])

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        energy_sets = json.load(f)

    # Convert any 'null' to np.nan
    for i, s in enumerate(energy_sets):
        energy_sets[i] = [e if e is not None else np.nan for e in s]

    plot_profile(
        energy_sets=energy_sets,
        filename=args.output,
        file_format=args.format,
        curviness=args.curviness,
        point_type=args.point_type,
        desaturate_factor=args.desaturate_factor,
        desaturate_curve=args.desaturate_curve,
        labels=args.labels,
        dashed=args.dashed
    )

