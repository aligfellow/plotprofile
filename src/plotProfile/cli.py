import argparse
import json
import numpy as np
from .plot import ReactionProfilePlotter


def main():
    parser = argparse.ArgumentParser(description="Plot reaction profile from labeled energy data")
    parser.add_argument('--input', type=str, required=True, help='Path to JSON file with energy dict')
    parser.add_argument('--output', type=str, default='reaction_profile', help='Output filename (no extension)')
    parser.add_argument('--format', type=str, default='png', choices=['eps', 'png', 'svg', 'pdf'])
    parser.add_argument('--style', type=str, default='default', 
                       help='Style preset (default, presentation, etc.)')
    parser.add_argument('--point-type', type=str, 
                       help='Point style (bar, dot, hollow) - overrides style')
    parser.add_argument('--curviness', type=float, 
                       help='Curve smoothness (0-1) - overrides style')
    parser.add_argument('--labels', action='store_true', 
                       help='Show energy labels - overrides style')
    parser.add_argument('--no-labels', action='store_true', 
                       help='Hide energy labels - overrides style')
    parser.add_argument('--desaturate-curve', action='store_true', 
                       help='Desaturate curve colors - overrides style')
    parser.add_argument('--desaturate-factor', type=float, 
                       help='Desaturation factor - overrides style')
    parser.add_argument('--dashed', nargs='*', type=str, default=[], 
                       help='List of series to show as dashed')
    parser.add_argument('--include', nargs='*', type=str, 
                       help='Subset of keys to include in plot')
    parser.add_argument('--axes', type=str, choices=['x', 'y', 'both', 'box', 'none'], 
                       help='Which axes to show - overrides style')
    parser.add_argument('--annotations', type=str, 
                       help='Path to JSON file with segment annotations')

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        energy_dict = json.load(f)

    # Convert 'null' to np.nan
    for key in energy_dict:
        energy_dict[key] = [e if e is not None else np.nan for e in energy_dict[key]]

    # Load annotations if provided
    segment_annotations = None
    if args.annotations:
        with open(args.annotations, 'r') as f:
            segment_annotations = json.load(f)

    # Prepare style kwargs
    style_kwargs = {
        'style': args.style,
    }
    
    # Apply overrides from CLI arguments
    if args.point_type:
        style_kwargs['point_type'] = args.point_type
    if args.curviness is not None:
        style_kwargs['curviness'] = args.curviness
    if args.labels:
        style_kwargs['labels'] = True
    if args.no_labels:
        style_kwargs['labels'] = False
    if args.desaturate_curve:
        style_kwargs['desaturate'] = True
    if args.desaturate_factor is not None:
        style_kwargs['desaturate_factor'] = args.desaturate_factor
    if args.axes:
        style_kwargs['axes'] = args.axes if args.axes != 'none' else None
    if segment_annotations:
        style_kwargs['segment_annotations'] = segment_annotations

    plotter = ReactionProfilePlotter(**style_kwargs)

    # Handle dashed series
    if args.dashed:
        plotter.dashed = args.dashed

    plotter.plot(
        energy_dict, 
        filename=args.output, 
        file_format=args.format, 
        include_keys=args.include
    )


if __name__ == '__main__':
    main()