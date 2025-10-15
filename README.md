# plotprofile 
Python code for quick plotting of professional looking reaction profiles with various customisation options available

More information can be found at [ReadTheDocs](https://plotprofile.readthedocs.io/)

[![PyPI Downloads](https://static.pepy.tech/badge/plotprofile)](https://pepy.tech/projects/plotprofile)

## Installation
### Google Colab
Can be used with `colab.ipynb` without a local install.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aligfellow/plotprofile/blob/main/examples/colab.ipynb)

### Pip
Simplest installation:
```bash
pip install plotprofile
```
or from the latest version:
```bash
pip install git+https://github.com/aligfellow/plotprofile.git
```
### Local installation
```bash
git clone git@github.com:aligfellow/plotprofile.git
cd plotprofile
pip install .
```

## Minimal Python Usage 
```python
from plotprofile import ReactionProfilePlotter

energy_sets = {
    "Pathway A": [0.00, -2.0, 10.2, 1.4, -1.5, 2.0, -7.2],
    "Pathway B": [None, -2.0, 6.2, 4.3, 5.8, 2.0],
}

plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/profile0")
```
<img src="./images/profile0.png" height="300" alt="Example 0">

## Further Python Examples
### Example 1
```python
from plotprofile import ReactionProfilePlotter

energy_sets = {
    "Pathway A": [0.00, -2.0, 10.2, 1.4, -1.5, 2.0, -7.2],
    "Pathway B": [None, -2.0, 6.2, 4.3, 5.8, 2.0],
    "Pathway C": [None, -2.0, -6.8,-6.8, None, -2.0],
    "diastereomer": [None, None, 12.2],
    "diastereomer2": [None, None, 9.8, 9.8]
}
annotations = {
    'Step 1': (0,3),
    'Step 2': (3,5),
    'Step 3': (5,6),
}

plotter = ReactionProfilePlotter(dashed=["Pathway C"])
plotter.plot(energy_sets, annotations=annotations, filename="../images/profile1")
```
Passing in `annotations` for labelling of the reaction profile:
- this is done in the plotting function rather than the class
- using dictionary with keys of labels and a tuple of the start and end x-indices
- allowing for multiple plots of the same style with different annotations

<img src="./images/profile1.png" height="300" alt="Example 1">

### Example 2 
A variety of other paremters can be tuned for the plotting, including:
- `axes="box|y|x|both|None"` 
- `curviness=0.42` - reduce for less curve and vice versa
- `colors=["list","of","colors"]|cmap` - specify colour list or colour map
    - if the colour list is too short then colours will be repeated. 
    - if the cmap is invalid, `viridis` will be set as a default
- `show_legend=Bool`
- `units="kj|kcal"`
- `energy="e|electronic|g|gibbs|h|enthalpy|s|entropy|"`
- `x_label` and `y_label` can be used to set cutoms axis labels, **superceeding** `units` or `energy`

Using `style="presentation"` which sets a larger `figsize=(X,X)` with thicker lines and a larger font size:
```python
plotter = ReactionProfilePlotter(style="presentation", dashed=["Pathway B"], point_type='dot', desaturate=False, colors='Blues_r', show_legend=False, curviness=0.5, x_label='Reaction Profile', y_label='Free Energy (kcal/mol)')
plotter.plot(energy_sets, filename="../images/profile2")
```

<img src="./images/profile2.png" height="300" alt="Example 2">

### Example 3 
- Straight lines set in a style, which can also be done by passing in `curviness=0`
- Labels can be placed below the annotation arrow 
- Some parameters regarding the plotting data can be tuned in `ReactionProfilePlotter.plot`:
    - `include_keys` - only some of the energy_sets keys() included in the plot
    - `exclude_from_legend` - excluded one of the energy_sets key from the legend

```python
plotter = ReactionProfilePlotter(style="straight", figsize=(6,4), dashed=["Pathway C"], point_type='bar', annotation_color='black', axes='y', colors=['midnightblue', 'slateblue', 'darkviolet'], energy='electronic', units='kj', annotation_below_arrow=True, dash_spacing=5.0, desaturate=False)
plotter.plot(energy_sets, annotations=annotations, filename="../images/profile3", exclude_from_legend=["Pathway B"], include_keys=["Pathway A", "Pathway B", "Pathway C", "diastereomer"])
```

<img src="./images/profile3.png" height="300" alt="Example 3">

### Example 4 
- Point labels can be also added by passing `point_labels` to `ReactionProfilePlotter.plot`
- Annotations can accomodate newline characters `\n` and spacing will be adjusted automatically

```python
from plotprofile import ReactionProfilePlotter

energy_sets = {
    "1": [-3.0, 12.5, 2.9, 0.0, 1.8, 10.5, 2.9]
}

annotations = {
    'Step 1': (0,3),
    'Step 2\nAlternate': (3,6),
}

point_labels = {
    "1": [None, "TS1", None, "Int1", None, "TS2"]
}

plotter = ReactionProfilePlotter(figsize=(4.5,4), axes='box', show_legend=False)
plotter.plot(energy_sets, annotations=annotations, point_labels=point_labels, filename="../images/profile4")
```

<img src="./images/profile4.png" height="300" alt="Example 4">

### Example 5 
- Bar lengths and widths can be adjusted
- Default line/curve behaviour with bars is to connect at the edges, this can be turned off with `connect_bar_ends=False`
- Dash spacing of the line can be changed with `dash_spacing` 


```python
from plotprofile import ReactionProfilePlotter

energy_sets = {
    "1": [-3.0, 12.5, 2.9, 0.0, 1.8, 10.5, 2.9]
}

annotations = {
    'Step 1': (0,3),
    'Step 2\nAlternate': (3,6),
}

point_labels = {
    "1": [None, "TS1", None, "Int1", None, "TS2"]
}

plotter = ReactionProfilePlotter(figsize=(4.5,4), axes='box', curviness=0.5, show_legend=False, point_type='bar', bar_length=0.3, bar_width=3, connect_bar_ends=False, dashed=["1"], dash_spacing=1.5)
plotter.plot(energy_sets, annotations=annotations, point_labels=point_labels, filename="../images/profile5")
```
<img src="./images/profile5.png" height="300" alt="Example 5">


See [examples/example.ipynb](./examples/example.ipynb) 

## Further details 
>[!IMPORTANT]
>- Secondary curves can begin from after the 1st point, just need to have a `None` entry in the list of energies *e.g.* `[None, 0.0, 1.0]`
>- Individual points can be placed if this is a list with only one energy value (*e.g.* uncluttered diastereomeric TS for example, see examples)
>    - labels of theses are not added to the legend
>    - these can even be placed as individual points between two indices with `[None, 5.0, 5.0]`
>- Spacing of points on the profile can be altered by:
>    - passing the same energy twice in a row, which will place the point halfway between the two x-indices, *i.e.* Pathway C point in examples, *e.g.* `[0.0, 5.0, 5.0]`
>    - with an entry like `[0.0, None, 1.0]` which will have a line connecting indexes 0 and 2 of this list with the correct x-axis alignment
>- data types can be:
>    - dict, with labels for the legend
>    - list of lists (no labelling of different profiles)
>    - single list

## CLI 
>[!NOTE]
>Currently untested - though this won't work for now
```bash
python -m plotprofile --input examples/input.json --labels --format png
```

## To Do 
>[!TIP]
>- label placement is primitive and could be improved
>   - for now these can be tweaked with postprocessing 
>- check cli options

## Configuration options 
The behavior can be customized via `styles.json` or by passing parameters to `ReactionProfilePlotter()`. Here are all available options from `styles.json`:
```json
{
    "default": {
      "figsize": [5,4.5],
      "point_type": "hollow",
      "curviness": 0.42,
      "desaturate": true,
      "desaturate_factor": 1.2,
      "dashed": [],
      "dashed_spacing": 2.5,
      "labels": true,
      "show_legend": true,
      "line_width": 2.5,
      "bar_width": 3.0,
      "bar_length": 0.3,
      "marker_size": 6,
      "font_size": 12,
      "font_family": "Arial",
      "font_weight": "bold",
      "font_style": "normal",
      "axis_linewidth": 2.0,
      "buffer_factor": 0.05,
      "axes": "box",
      "colors": ["darkcyan", "maroon", "midnightblue", "darkmagenta", "darkgreen", "saddlebrown"],
      "segment_annotations": [],
      "arrow_color": "xkcd:dark grey",
      "annotation_color": "maroon",
      "annotation_size": 11,
      "energy": "G",
      "units": "kcal",
      "annotation_below_arrow": false,
      "annotation_space": 0.05,
      "annotation_buffer": 0.0,
      "arrow_width": 1.5,
      "sig_figs": 1,
      "point_label_color": "black",
      "connect_bar_ends": true
    },
    "presentation": {
      "figsize": [8, 5],
      "font_size": 14,
      "annotation_size": 14,
      "marker_size": 8,
      "line_width": 3.0,
      "bar_width": 3.5,
      "annotation_space": 0.12,
      "arrow_width": 2.5
    },
    "straight": {
      "curviness": 0.0
    }
  }
```
