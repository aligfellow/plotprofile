# plotProfile
Python code for plotting reaction profiles with various style options

## Installation
```bash
git clone git@github.com:aligfellow/plotProfile.git
cd plotProfile
pip install .
```
- *check the installation, `pip install .` seems to not respect the json locally*

## To Do
- label placement is primitive and could be improved
   - for now these can be tweaked with postprocessing 
- check cli options

## Python Usage examples
Use case for example: 
```python
import plotProfile
import numpy as np

energy_sets = {
    "Pathway A": [0.00, -2.0, 10.2, 1.4, -1.5, 2.0, -7.2],
    "Pathway B": [np.nan, -2.0, 6.2, 4.3, 5.8, 2.0],
    "Pathway C": [np.nan, -2.0, -6.8,-6.8],
}

annotations = {
    'Step 1': (0,3),
    'Step 2': (3,5),
    'Step 3': (5,6),
}

plotter = plotProfile.plot.ReactionProfilePlotter(style="default", dashed=["off-cycle", "Pathway C"], segment_annotations=annotations)
plotter.plot(energy_sets)
```
- Here we pass in annotations for a labelling of the reaction profile

<img src="./images/profile1.png" height="200" alt="Example 1">

A variety of paremters can be tuned for the plotting, including:
- `axes="box|y|x|both|None"` 
- `curviness=0.42` - reduce for less curve and vice versa
- `colors=["list","of","colors"]|cmap` - specify colour list or colour map
- `show_legend=Bool`

<img src="./images/profile2.png" height="200" alt="Example 2">

<img src="./images/profile3.png" height="200" alt="Example 3">

See [examples/example.ipynb](examples/example.ipynb) for more explicit code

## CLI
Currently untested - probably won't work for now
```bash
python -m plotProfile --input examples/input.json --labels --format png
```



