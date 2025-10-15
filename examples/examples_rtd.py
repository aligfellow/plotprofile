from plotprofile import ReactionProfilePlotter

# -------------------------------
# Behaviour Examples
# -------------------------------
# 1. Point repeated for spacing
energy_sets = {
    "Pathway A": [0.0, 5.0, 5.0, 2.0],
    "Pathway B": [0.0, 3.0, 1.0, 4.0],
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/behaviour1")

# 2. Skipping an index
energy_sets = {
    "Pathway A": [0.0, 5.0, 2.0, 3.0],  
    "Pathway B": [1.0, None, 4.0, 6.0],
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/behaviour2")

# 3. Starting later
energy_sets = {
    "Pathway A": [0.0, -2.0, 5.0, 4.0],
    "Pathway B": [None, None, 3.0, 6.0],
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/behaviour3")

# 4. Finishing earlier
energy_sets = {
    "Pathway A": [0.0, -2.0, 5.0, 4.0],
    "Pathway B": [0.0, 2.0, 3.0],
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/behaviour4")

# 5. Single isolated points
energy_sets = {
    "Pathway A": [0.0, 5.0, -2.0, 4.0],
    "TS1": [None, 7.0],
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/behaviour5")


# -------------------------------
# Plotting Examples
# -------------------------------
energy_sets = {
    "Pathway A": [0.0, -2.0, 10.0, 1.5, -1.5, 2.0, -7.0],
    "Pathway B": [None, -2.0, 6.0, 4.0, 5.0, 2.0, None]
}

plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, filename="../images/profile10")

# Presentation style
plotter = ReactionProfilePlotter(style="presentation")
plotter.plot(energy_sets, filename="../images/profile11")

# Straight lines style
plotter = ReactionProfilePlotter(style="straight")
plotter.plot(energy_sets, filename="../images/profile12")

# Axes display example
plotter = ReactionProfilePlotter(axes='y')
plotter.plot(energy_sets, filename="../images/profile13")

# Axis labels and units
plotter = ReactionProfilePlotter(
    energy='E',
    units='kcal',
    x_label='Reaction'
)
plotter.plot(energy_sets, filename="../images/profile14")

# Point type example
plotter = ReactionProfilePlotter(point_type='dot')
plotter.plot(energy_sets, filename="../images/profile16")

# Bar plot example
plotter = ReactionProfilePlotter(
    point_type='bar',
    bar_width = 3.0,
    bar_length = 0.3,
    connect_bar_ends = True
)
plotter.plot(energy_sets, filename="../images/profile17")

# Dashed lines
plotter = ReactionProfilePlotter(dashed=['Pathway A'])
plotter.plot(energy_sets, filename="../images/profile18")

# Curviness
plotter = ReactionProfilePlotter(curviness=0.7)
plotter.plot(energy_sets, filename="../images/profile19")

# Colors
plotter = ReactionProfilePlotter(colors='Reds_r', desaturate=False)
plotter.plot(energy_sets, filename="../images/profile20")

# Saturation
plotter = ReactionProfilePlotter(desaturate=False)
plotter.plot(energy_sets, filename="../images/profile21")

# Annotations
annotations = {
    "Part 1": (0, 2),
    "Part 2": (2, 4),
    "Part\n 3": (4, 6)
}
plotter = ReactionProfilePlotter()
plotter.plot(energy_sets, annotations=annotations, filename="../images/profile22")

# Labels
point_labels = {
    "Pathway A": ["Int1", "Int2", "TS1", "Int3"],
    "Pathway B": [None, None, "TS2" ]
}
plotter = ReactionProfilePlotter(point_labels=point_labels)
plotter.plot(energy_sets, point_labels=point_labels, filename="../images/profile23")


# Legend example
energy_sets = {
    "Pathway A": [0.0, -2.0, 10.0, 1.5, -1.5, 2.0, -7.0],
    "Pathway B": [None, -2.0, 6.0, 4.0, 5.0, 2.0, None],
    "Pathway C": [0.0, 3.0, 5.0, 2.0, 4.0, 1.0, -3.0],
}
plotter = ReactionProfilePlotter(show_legend=True)
plotter.plot(
    energy_sets,
    exclude_from_legend=['Pathway A'],
    include_keys=['Pathway A', 'Pathway C'],
    filename="../images/profile15"
)
