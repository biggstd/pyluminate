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

# Bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool
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
    Returns a list of pandas dataframes.
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
def create_figures(active_frames):

    # Get the active dataframes to be plotted:
    active_frames = select_RDFs()

    # Declare the figure:
    fig = figure()

    # Declare the colors to be used:
    # TODO: look for a more robust way to handle colors
    colors = Category20[len(dataframes)]

    # Iterate through the data frames to be used.
    for (df, df_color) in zip(active_frames, colors):

        # Declare the source from the current frame:
        fig_source = ColumnDataSource(df)

        # Add the hover tool:
        # TODO: needs to take from the characteristics metadata dict.
        fig.add_tools(HoverTool(tooltips=[
            ("Radius", "@r"),
        ]))

        # Iterate over the bonds selected.
        for bond in df.characteristics['Inter-atom distances']:

            # Draw a line plot
            fig.line(
                source=fig_source,
                x='r',
                y=bond,
                legend=df.characteristics['Aluminate Species'][0],
                color=df_color,
                line_width=1.5
            )

    return fig


# TODO: Define the metadata detail div


# Define the update function
def update():
    """Function that runs upon initialization and whenever the user
    interacts with an input."""

    # Get the list of active data frames based on user input.
    active_frame_list = select_RDFs()

    # Create the figures based on the retrieved dataframe list.
    new_fig = create_figures(active_frame_list)

    # Clear the current document.
    curdoc().clear()

    # Add the new layout to the curdoc() function.
    curdoc().add_root(create_layout(new_fig))

    return


# Add the controls
controls = [
    compound_sel,
    bonds_grp,
    stack_sel,
]


# Create a widget box for the inputs to be carried in.
sizing_mode = 'fixed'
inputs = widgetbox(*controls, sizing_mode=sizing_mode)

# Add the controls on_change() function
for control in controls:
    control.on_change('value', lambda attr, old, new: update())


# Create the layout
def create_layout(fig):
    my_layout = layout([
        [inputs, fig],
    ], sizing_mode=sizing_mode)
    return my_layout


# Run update to load the default dataset
update()

# Add the laout to the current document and set it up
curdoc().add_root(create_layout())
curdoc().title = "RDV Viewer"
