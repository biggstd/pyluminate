"""
=============================
RDF Visualization Application
=============================

This application will create an interactive Bokeh application.

## Introduction


## Display

It can show a variable number of plots, based on the options.



## Options

+ Select a **compound**.
+ Within each **compound** there will be a list of available bonds.
+ There should be an overlap and a grid option.
+ There should be a stacked selection view.?

"""

# Basic data science imports
import pandas as pd
# Bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
# Local, relative module imports
from vis.utils import read_rdf


# From the metadata, load the desired data into pandas dataframes.
dataframes = read_rdf('../metadata.json', char_types=['Aluminate Species'])

"""
# CONTROLS
Define the Controls (for variable name use in the functions below.)

These need to be added to the controls list at the bottom of the file.

"""

# The possible layout options.
stack_options_d = {
	'Bonds Overlaped': 'Overlaped',
	'Compounds Overlaped': 'Overlaped',
}

compound_sel = Select(
	title="Compound",
	options=compound_l,
)

bonds_sel = Select(
	title="Bond",
	options=bond_l  # This probably needs to call a function? It
					# depends on the compound selected.
)

stack_sel = Select(
	title="Plot Arrangement",
	options=stack_options_d.keys(),
)


# Define the plotting function
def create_figures():
	pass


# Define the metadata detail div
def create_info_div():
	pass


# Define the update function
def update():
	pass


# Add the controls
controls = [
	compound,
]


# Create a widget box for the inputs to be carried in.
sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)


# Create the layout
def create_layout():
	my_layout = layout([
			[info_div],
			[inputs, plot],
		],
		sizing_mode=sizing_mode)
	return my_layout


# Run update to load the default dataset
update()

# Add the laout to the current document and set it up
curdoc().add_root(create_layout())
curdoc().title = "RDV Viewer"









