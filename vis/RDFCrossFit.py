"""
=============================
RDF Visualization Application
=============================

This application will create an interactive Bokeh application.

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
from bokeh.models.widgets import Select, MultiSelect, CheckboxGroup
from bokeh.palettes import Category20
from bokeh.io import curdoc
# Local, relative module imports
from vis.utils import read_rdf
import collections


# From the metadata, load the desired data into pandas dataframes.
# Each dataframe has an attribute attached by the read_rdf function.
# This characteristics attribute is a dictioary of values. The entires
# for 'Inter-atom distances' are the bonds within that dataframe.
dataframes = read_rdf('../metadata.json', char_types=['Aluminate Species'])

# Since we can se all the bonds and species at this point, we can build
# the input lists options. First create an empty dictionary. A collections
# defaultdict is used to ensure uncreated values are always lists.
available_cmpds_dict = collections.defaultdict(list)

for frame in dataframes:
    # Set the new, aluminate species key
    available_cmpds_dict[frame.characteristics['Aluminate Species'][0]].extend(
        frame.characteristics['Inter-atom distances'])

"""
# CONTROLS
Define the Controls (for variable name use in the functions below.)
These need to be added to the controls list at the bottom of the file.
"""

compound_sel = MultiSelect(
    title="Compound",
    options=available_cmpds_dict.keys(),
)

bonds_grp = CheckboxGroup(
    title="Bond",
    options=available_cmpds_dict[compound_sel.value]
)

stack_sel = Select(
    title="Plot Arrangement",
    options=['Overlap', 'Separate'],
    value='Overlap'
)


# Define the dataframe selection function.
def select_RDFs():
    """
    Examines the input(s) and loads the appropriate dataframes.
    """
    # Create an empty list of dataframes that will be displayed:
    displayed_df_l = list()
    # Set the list of compounds to those selected in the input.
    compounds = compound_sel.value
    for frame in dataframes:
        if any(compounds) in frame.characteristics['Aluminate Species']:
            displayed_df_l.append(frame)

    return displayed_df_l


# Define the plotting function
def create_figures():

    # Get the active dataframes to be plotted:
    active_frames = select_RDFs()

    # Declare the figure:
    fig = figure()

    # Add the hover tool:
    fig.add_tools(HoverTool(tooltips=[
        ("Radius", "@r"),
        ("Probability", "@{RDF_Al-Oh}"),
        ("Connectivity", "@{RCN_Al-Oh}")
    ]))

    # Declare the colors to be used:
    colors = Category20[len(dataframes)]

    # Iterate through the data frames to be used.
    for (df, df_color) in zip(active_frames, colors):
        fig_source = ColumnDataSource(df)
        fig.line(
            source=fig_source,
            x='r',
            y='RDF_Al-Oh',
            legend=df.characteristics['Aluminate Species'][0],
            color=df_color,
            line_width=1.5
        )

    return fig


# Define the metadata detail div
def create_info_div():
    pass


# Define the update function
def update():
    pass


# Add the controls
controls = [
    compound_sel,
    bonds_grp,
    stack_sel,
]


# Create a widget box for the inputs to be carried in.
sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)


# Create the layout
def create_layout():
    my_layout = layout([
            [info_div],
            [inputs, fig],
        ],
        sizing_mode=sizing_mode)
    return my_layout


# Run update to load the default dataset
update()

# Add the laout to the current document and set it up
curdoc().add_root(create_layout())
curdoc().title = "RDV Viewer"
