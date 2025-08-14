Data Input
===========

This outlines the data types that are required for plotting with ``plotProfile``.

Energies 
-----------
The energies can be provided in the following formats:

.. code-block:: python

    dict[str, list[float | None]]

A dictionary where the keys are pathway names and the values are lists of energies. 

.. code-block:: python

    list[list[float | None]]

A list of lists, where each inner list represents a pathway's energies. A legend will not be plotted as there are no pathway names or labels.

.. code-block:: python

    list[float | None]

A single list of energies, which will be plotted as a single pathway. Again, no legend will be plotted.
