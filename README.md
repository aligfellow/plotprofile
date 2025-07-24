# plotProfile
Python code for plotting professional looking reaction profiles with various customisation options available

## Installation
### From pypi
Simplest installation
```bash
pip install plotprofile
```
### Local installation
```bash
git clone git@github.com:aligfellow/plotProfile.git
cd plotProfile
pip install .
```
>[!WARNING]
>this may not respect the styles.json, if not:
>```bash
>git clone git@github.com:aligfellow/plotProfile.git
>cd plotProfile
>python -m build
>pip install dist/plotprofile-1.0.1.tar.gz
>```


## Python Usage examples
Use case for example: 
```python
from plotProfile import ReactionProfilePlotter

energy_sets = {
    "Pathway A": [0.00, -2.0, 10.2, 1.4, -1.5, 2.0, -7.2],
    "Pathway B": [None, -2.0, 6.2, 4.3, 5.8, 2.0],
    "Pathway C": [None, -2.0, -6.8,-6.8],
}

annotations = {
    'Step 1': (0,3),
    'Step 2': (3,5),
    'Step 3': (5,6),
}

plotter = ReactionProfilePlotter(dashed=["Pathway C"])
plotter.plot(energy_sets, annotations=annotations, filename="../images/profile1")
```
Pass in `annotations` for labelling of the reaction profile:
- this is done in the plotting function rather than the class
- using dictionary with keys of labels and a tuple of the start and end x-indices
- allowing for multiple plots of the same style with different annotations

<img src="./images/profile1.png" height="300" alt="Example 1">

A variety of paremters can be tuned for the plotting, including:
- `axes="box|y|x|both|None"` 
- `curviness=0.42` - reduce for less curve and vice versa
- `colors=["list","of","colors"]|cmap` - specify colour list or colour map
- `show_legend=Bool`
- `units="kj|kcal"`
- `energy="e|electronic|g|gibbs|h|enthalpy|s|entropy|"`

For example:
```python
plotter = ReactionProfilePlotter(style="presentation", dashed=["Pathway B"], point_type='bar', desaturate=False, colors='Blues_r', show_legend=False, curviness=0.5)
plotter.plot(energy_sets, filename="../images/profile2")
```
- Using `style="presentation"` which sets a larger `figsize=(X,X)`, thicker lines, larger font size:

<img src="./images/profile2.png" height="300" alt="Example 2">

For example:
```python
plotter = ReactionProfilePlotter(style="straight", figsize=(6,4), dashed=["Pathway C"], point_type='dot', annotation_color='black', axes='y', colors=['darkseagreen', 'slateblue', 'darksalmon'], energy='electronic', units='kj')
plotter.plot(energy_sets,annotations=annotations, filename="../images/profile3")
```
- Straight lines set in a style, which can also be done by passing in `curviness=0`:

<img src="./images/profile3.png" height="300" alt="Example 3">

See [examples/example.ipynb](examples/example.ipynb) for more explicit code

### Further details
>[!IMPORTANT]
>- Secondary curves can begin from after the 1st point, just need to have a `None` entry in the list of energies *e.g.* `[None, 0.0, 1.0]`
>- Individual points can be placed if this is a list with only one energy value (*e.g.* uncluttered diastereomeric TS for example, see examples)
>    - labels of theses are not added to the legend
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
python -m plotProfile --input examples/input.json --labels --format png
```

## To Do
>[!TIP]
>- label placement is primitive and could be improved
>   - for now these can be tweaked with postprocessing 
>- check cli options


