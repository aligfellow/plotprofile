Getting Started
===============

Python code for quick plotting of professional looking reaction profiles with various customisation options available

.. image:: https://static.pepy.tech/badge/plotprofile
   :target: https://pepy.tech/projects/plotprofile

Installation
------------

Google Colab
^^^^^^^^^^^^

Can be used with ``colab.ipynb`` without a local install.

.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/aligfellow/plotProfile/blob/main/examples/colab.ipynb

Pip
^^^

Simplest installation:

.. code-block:: bash

    pip install plotprofile

or from the latest version:

.. code-block:: bash

    pip install git+https://github.com/aligfellow/plotprofile.git

Local installation
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    git clone git@github.com:aligfellow/plotProfile.git
    cd plotProfile
    pip install .

Minimal Python Usage
---------------------

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

