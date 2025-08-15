.. plotProfile documentation master file, created by
   sphinx-quickstart on Thu Aug 14 13:11:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

plotProfile documentation
=========================

Welcome to the **plotProfile** documentation! This package provides tools for visualizing reaction profile energies. 


.. image:: https://static.pepy.tech/badge/plotprofile
   :target: https://pepy.tech/projects/plotprofile



Features
-------------------

🎯 **Professional Publication-Ready Plots**
   Generate high-quality reaction profiles suitable for journals and presentations

🔧 **Extensive Customization** 
   Colors, line styles, annotations, units, and layout options

📊 **Flexible Data Input**
   Support for multiple reaction pathways, diastereomers, and individual transition states

🚀 **Easy Integration**
   Works seamlessly with Jupyter notebooks and Python scripts


Quick Example
--------------

.. code-block:: python

    from plotProfile import ReactionProfilePlotter

    energy_sets = {
        "Pathway A": [0.00, -2.0, 10.2, 1.4, -1.5, 2.0, -7.2],
        "Pathway B": [None, -2.0, 6.2, 4.3, 5.8, 2.0],
    }

    plotter = ReactionProfilePlotter()
    plotter.plot(energy_sets, filename="../images/profile0")

.. image:: ./images/profile0.png
   :height: 300
   :alt: Example 0


.. toctree::
   :maxdepth: 4
   :caption: Getting Started
   :hidden:

   installation
   quickstart

.. toctree::
   :maxdepth: 4
   :caption: User Guide
   :hidden:

   usage/data-input
   usage/styles
   usage/behaviour
   usage/customisation

.. toctree::
   :maxdepth: 4
   :caption: Reference
   :hidden:

   json_styles
   cli
   modules
   