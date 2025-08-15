Plotting Examples
====================================

Plotting Data
-------------

All examples use these data unless specified otherwise:

.. code-block:: python

    from plotProfile import ReactionProfilePlotter

    energy_sets = {
        "Pathway A": [0.0, -2.0, 10.0, 1.5, -1.5, 2.0, -7.0],
        "Pathway B": [None, -2.0, 6.0, 4.0, 5.0, 2.0, None]
    }

Plotting Behaviour 
------------------

This section demonstrates how to manipulate the reaction profile plotting
beyond aesthetics: controlling x-axis positions, skipping points, starting
later, finishing earlier, or placing individual points between indices.



1. Point repeated for spacing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you want a point placed **between two x-indices**. This can
be done by repeating the same energy value in consecutive positions.

Example:

.. code-block:: python

    from plotProfile import ReactionProfilePlotter

    energy_sets = {
        "Pathway A": [0.0, 5.0, 5.0, 2.0],  # repeated 5.0 creates midpoint
        "Pathway B": [0.0, 3.0, 1.0, 4.0],
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="images/behaviour1")

.. image:: images/behaviour1.png
   :height: 300
   :alt: Behaviour Example 1

2. Skipping an index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


You can skip an index by inserting `None` in the energy list.
The line will connect non-None values automatically.

Example:

.. code-block:: python

    energy_sets = {
        "Pathway A": [0.0, 5.0, 2.0, 3.0],  
        "Pathway B": [1.0, None, 4.0, 6.0],
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="images/behaviour2")

.. image:: images/behaviour2.png
   :height: 300
   :alt: Behaviour Example 2

3. Starting later
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


A secondary curve can start after the first point. Place `None` in
all preceding positions.

Example:

.. code-block:: python

    energy_sets = {
        "Pathway A": [0.0, -2.0, 5.0, 4.0],
        "Pathway B": [None, None, 3.0, 6.0],
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="images/behaviour3")

.. image:: images/behaviour3.png
   :height: 300
   :alt: Behaviour Example 3

4. Finishing earlier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


If you want a curve to finish before the last index, just end the list
before the other series.

Example:

.. code-block:: python

    energy_sets = {
        "Pathway A": [0.0, -2.0, 5.0, 4.0],
        "Pathway B": [0.0, 2.0, 3.0],  # ends earlier
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="images/behaviour4")

.. image:: images/behaviour4.png
   :height: 300
   :alt: Behaviour Example 4

5. Single isolated points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Individual points can be placed by providing a list with only one
energy value or surrounding ``None``.

Example:

.. code-block:: python

    energy_sets = {
        "Pathway A": [0.0, 5.0, -2.0, 4.0],
        "TS1": [None, 7.0],
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="images/behaviour5")

.. image:: images/behaviour5.png
   :height: 300
   :alt: Behaviour Example 5


Plotting Customisation
-----------------------

This table summarizes the main plotting style parameters.


+-------------------+-------------------+--------------------------------------------------+
| Parameter         | Default           | Description                                      |
+===================+===================+==================================================+
| figsize           | [5, 4.5]          | Figure size in inches (width, height)            |
+-------------------+-------------------+--------------------------------------------------+
| point_type        | hollow            | Marker type for points (hollow, dot, bar, etc.)  |
+-------------------+-------------------+--------------------------------------------------+
| curviness         | 0.42              | Controls how curved the lines are                |
+-------------------+-------------------+--------------------------------------------------+
| desaturate        | True              | Whether to desaturate colors                     |
+-------------------+-------------------+--------------------------------------------------+
| dashed            | []                | List of lines to render as dashed                |
+-------------------+-------------------+--------------------------------------------------+
| line_width        | 2.5               | Width of line plots                              |
+-------------------+-------------------+--------------------------------------------------+
| bar_width         | 3.0               | Width of bars if using bar points                |
+-------------------+-------------------+--------------------------------------------------+
| show_legend       | True              | Display the legend                               |
+-------------------+-------------------+--------------------------------------------------+
| colors            | ["darkcyan", ...] | List of colors for lines                         |
+-------------------+-------------------+--------------------------------------------------+
| annotation_color  | maroon            | Color for annotations                            |
+-------------------+-------------------+--------------------------------------------------+
| energy            | G                 | Type of energy plotted (G, H, E, etc.)           |
+-------------------+-------------------+--------------------------------------------------+
| units             | kcal              | Units of energy                                  |
+-------------------+-------------------+--------------------------------------------------+


A. Default Style
~~~~~~~~~~~~~~~~
The default style is applied automatically when you create a ``ReactionProfilePlotter`` instance without specifying a style.

.. code-block:: python

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="../images/profile10")

.. image:: images/profile10.png
   :height: 300px
   :alt: Example 1

B. Presentation Style
~~~~~~~~~~~~~~~~~~~~~~~
This style is designed to increase the size of the plot, font size and line width, making it more suitable for presentations. 

.. code-block:: python

    plotter = ReactionProfilePlotter(style=presentation)
    plotter.plot(energy_sets, filename="../images/profile11")

.. image:: images/profile11.png
   :height: 300px
   :alt: Example 1

C. Straight Lines Style
~~~~~~~~~~~~~~~~~~~~~~~~~
This style inherits the default style but with straight lines instead of curved.

.. code-block:: python

    plotter = ReactionProfilePlotter(style=straight)
    plotter.plot(energy_sets, filename="../images/profile12")

.. image:: images/profile12.png
   :height: 300px
   :alt: Example 1


1. Axes Display
~~~~~~~~~~~~~~~~~~~~~~~~

Axes can be shown selectively using the ``axes`` parameter:

- ``axes='y'`` shows only the y-axis.

- ``axes='x'`` shows only the x-axis.

- ``axes='both'`` shows both axes.

- ``axes='box'`` shows 4 axes.

- ``axes=None`` hides both axes.

.. code-block:: python

    plotter = ReactionProfilePlotter(axes='y')
    plotter.plot(energy_sets, filename="../images/profile13")

+-----------+------+
| Parameter | Value|
+===========+======+
| axes      | y    |
+-----------+------+

.. image:: images/profile13.png
   :height: 300px
   :alt: Axes example

2. Axis Labels and Units
~~~~~~~~~~~~~~~~~~~~~~~~~

Axis labels can be fully customized:

- ``x_label`` and ``y_label``, which override the labels completely.

- ``energy`` can be `e|electronic|g|gibbs|h|enthalpy|s|entropy` to automatically label the y-axis.

- ``units`` sets the y-axis units: 'kcal' or 'kj'.

.. code-block:: python

    plotter = ReactionProfilePlotter(
        energy='E',
        units='kcal',
        x_label='Reaction',
    )
    plotter.plot(energy_sets, filename="../images/profile14")

+-----------+-------------------------------+
| Parameter | Value                         |
+===========+===============================+
| x_label   | Reaction                      |
+-----------+-------------------------------+
| energy    | E                             |
+-----------+-------------------------------+
| units     | kcal                          |
+-----------+-------------------------------+

.. image:: images/profile14.png
   :height: 300px
   :alt: Axis labels example

3. Legend Options
~~~~~~~~~~~~~~~~~~~

The legend can be turned on/off, and specific lines can be included or excluded:

- ``show_legend`` toggles visibility. Default is `True`. This is controlled in the class as a global parameter. 

- ``exclude_from_legend`` hides specific lines. This is a plot function parameter.

- ``include_keys`` ensures certain keys are plotted even if not in the energy list. This is also a plot function parameter.

.. code-block:: python

    energy_sets = {
        "Pathway A": [0.0, -2.0, 10.0, 1.5, -1.5, 2.0, -7.0],
        "Pathway B": [None, -2.0, 6.0, 4.0, 5.0, 2.0, None],
        "Pathway C": [None, None, 3.0, 5.0, 6.0, 1.0, -2.0],
    }
    plotter = ReactionProfilePlotter(
        show_legend=True,
    )
    plotter.plot(energy_sets, exclude_from_legend=['Pathway A'], include_keys=["Pathway A", "Pathway C"], filename="../images/profile15")

+------------------------+----------------------------+
| Parameter              | Value                      |
+========================+============================+
| show_legend            | True                       |
+------------------------+----------------------------+
| exclude_from_legend    | ['Pathway B']              |
+------------------------+----------------------------+
| include_keys           | ['Pathway A', 'Pathway C'] |
+------------------------+----------------------------+

.. image:: images/profile15.png
   :height: 300px
   :alt: Legend example

4. Point Types
~~~~~~~~~~~~~~~~~~~~~~~

Point styles can be selected with ``point_type``:

- Options: 'hollow', 'dot', 'bar'.

.. code-block:: python

    plotter = ReactionProfilePlotter(point_type='dot')
    plotter.plot(energy_sets, filename="../images/profile16")

+------------+---------+
| Parameter  | Value   |
+============+=========+
| point_type | dot     |
+------------+---------+

.. image:: images/profile16.png
   :height: 300px
   :alt: Point type example

5. Bar Plot Customization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bars have additional options:

- ``bar_length`` and ``bar_width`` control size.

- ``connect_bar_ends`` determines if lines connect to the bar center or ends.

  - Default is `True`

.. code-block:: python

    plotter = ReactionProfilePlotter(
        point_type='bar',
        bar_length=0.8,
        bar_width=0.3,
        connect_bar_ends=True
    )
    plotter.plot(energy_sets, filename="../images/profile17")

+-------------------+--------+
| Parameter         | Value  |
+===================+========+
| point_type        | bar    |
+-------------------+--------+
| bar_length        | 0.8    |
+-------------------+--------+
| bar_width         | 0.3    |
+-------------------+--------+
| connect_bar_ends  | True   |
+-------------------+--------+

.. image:: images/profile17.png
   :height: 300px
   :alt: Bar plot example

6. Dashed Lines
~~~~~~~~~~~~~~~~~~~~~~~~

Lines can be dashed selectively with the ``dashed`` parameter

- Pass a list of keys to make those lines dashed.

- dash spacing can be controlled with ``dash_spacing`` (default is 2.5).

.. code-block:: python

    plotter = ReactionProfilePlotter(dashed=['Pathway A'])
    plotter.plot(energy_sets, filename="../images/profile18")

+--------------+---------------+
| Parameter    | Value         |
+==============+===============+
| dashed       | ['Pathway A'] |
+--------------+---------------+
| dash_spacing | 2.5           |
+--------------+---------------+

.. image:: images/profile18.png
   :height: 300px
   :alt: Dashed lines example

7. Line Curviness
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``curviness`` parameter uses Bezier curves to control line curvature:

- 0.0 → straight lines

- 0.0–1.0 → increasing curvature

.. code-block:: python

    plotter = ReactionProfilePlotter(curviness=0.7)
    plotter.plot(energy_sets, filename="../images/profile19")

+------------+-------+
| Parameter  | Value |
+============+=======+
| curviness  | 0.7   |
+------------+-------+

.. image:: images/profile19.png
   :height: 300px
   :alt: Curved lines example

8. Colors
~~~~~~~~~~~~~~~~~~

Colors can be customized:

- Pass a list of named colors (will cycle if fewer than energy sets, truncate if longer).  

- Alternatively, pass a string of a colormap *i.e.* 'viridis', 'plasma', 'blues', 'reds_r', etc.

.. code-block:: python

    plotter = ReactionProfilePlotter(
        .. colors=['red','green','blue'],
        colors='Reds_r'
    )
    plotter.plot(energy_sets, filename="../images/profile20")

+------------+-----------------+
| Parameter  | Value           |
+============+=================+
| colors      | Reds_r         |
+------------+-----------------+

.. image:: images/profile20.png
   :height: 300px
   :alt: Colors example

9. Saturation
~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the color of the lines are desaturated slightly relative to the points. This can be turned off with the ``desaturate`` parameter.

- This can also be controlled with ``desaturate-factor`` which is a float from 1.0 where this is the original increasing to increase desaturation. 

  - default is 1.2

.. code-block:: python

    plotter = ReactionProfilePlotter(desaturate=False)
    plotter.plot(energy_sets, filename="../images/profile21")

+----------------+-------+
| Parameter      | Value |
+================+=======+
| desaturate     | False |
+----------------+-------+

.. image:: images/profile21.png
   :height: 300px
   :alt: Saturation example


10. Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~

Annotations can be added to the plot using the ``annotations`` parameter in the format:

dict{
'Annotation': (start_index, end_index)
}

This adds an arrow at the bottom, with the text centered on the arrow. 

- The arrow color can be set with ``arrow_color``.

- The annotation text color can be set with ``annotation_color``.

- The annotation text size can be set with ``annotation_size``.

- Additional options include ``annotation_below_arrow`` to place the text below the arrow instead on on the arrow. 

.. code-block:: python

    annotations = {
        "A": (0, 1),
        "B": (2, 3),
        "C": (4, 5)
    }
    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, annotations=annotations, filename="../images/profile22")

+---------------------+-----------------+
| Parameter           | Value           |
+=====================+=================+
| annotations         | {'A': (0, 1),   |
|                     | 'B': (2, 3),    |
|                     | 'C': (4, 5)}    |
+---------------------+-----------------+
| arrow_color         | xkcd:dark grey  |
+---------------------+-----------------+
| annotation_color    | maroon          |
+---------------------+-----------------+
| annotation_size     | 11              |
+---------------------+-----------------+

.. image:: images/profile22.png
   :height: 300px
   :alt: Annotations example


11. Labels
~~~~~~~~~~~~~~~~~~~~~~~~~~
Labels of points can be added in the following way:

- Pass a dict(list) of strings to the ``point_labels`` parameter.

- The keys are the energy set names, and the values are lists of labels for each point.

.. code-block:: python

    point_labels = {
        "Pathway A": ["Int1", "Int2", "TS1", "Int3"],
        "Pathway B": [None, None, "TS2" ]
    }
    plotter = ReactionProfilePlotter(point_labels=point_labels)
    plotter.plot(energy_sets, point_labels=point_labels, filename="../images/profile23")

+------------------+-----------------+
| Parameter        | Value           |
+==================+=================+
| point_labels     | {'Pathway A':   |
|                  | [None, 'TS1',   |
|                  | 'Int1', 'TS2']} |
+------------------+-----------------+ 

.. image:: images/profile23.png
   :height: 300px
   :alt: Labels example